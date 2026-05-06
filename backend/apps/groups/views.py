"""
apps/groups/views.py
--------------------
5 ViewSets pour Organisation, GroupType, Group, GroupRole, MemberGroup.
"""
from django.utils.decorators import method_decorator
from django.db.models import Prefetch, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.core.mixins import CacheInvalidationMixin, BaseModelViewSet
from apps.groups.models import Organisation, GroupType, Group, GroupRole, MemberGroup
from apps.groups.permissions import IsAdminOrReadOnly, IsGroupLeader, IsOwnerOrAdmin, CanAssignRole
from apps.groups.serializers import (
    OrganisationSerializer, GroupTypeSerializer, GroupSerializer,
    GroupRoleSerializer, MemberGroupSerializer,
)


# ────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────

SWAGGER_TAGS = ['Groupes & Organisations']

def swagger_crud(cls):
    """Applique les tags Swagger sur les 6 actions CRUD standard."""
    return extend_schema_view(
        list=extend_schema(tags=SWAGGER_TAGS),
        retrieve=extend_schema(tags=SWAGGER_TAGS),
        create=extend_schema(tags=SWAGGER_TAGS),
        update=extend_schema(tags=SWAGGER_TAGS),
        partial_update=extend_schema(tags=SWAGGER_TAGS),
        destroy=extend_schema(tags=SWAGGER_TAGS),
    )(cls)

def member_group_base_queryset():
    return (
        MemberGroup.objects
        .select_related('user', 'group', 'role')
        .order_by('-joined_at')
    )

def group_base_queryset():
    return (
        Group.objects
        .select_related('organisation', 'type', 'created_by', 'updated_by')
        .prefetch_related(
            Prefetch('members', queryset=MemberGroup.objects.filter(status='ACTIVE'))
        )
        .order_by('-created_at')
    )


def get_or_create_role(role_type: str, name: str) -> GroupRole:
    """
    Récupère ou crée un GroupRole par role_type.
    ✅ Sûr grâce à unique=True sur role_type dans le modèle.
    """
    role, _ = GroupRole.objects.get_or_create(
        role_type=role_type,
        defaults={'name': name},
    )
    return role


# ────────────────────────────────────────────────
# Organisation
# ────────────────────────────────────────────────

@swagger_crud
class OrganisationViewSet(CacheInvalidationMixin, BaseModelViewSet):
    """Organisations — création/suppression réservée aux propriétaires et admins."""
    cache_prefix      = 'organisation'
    queryset          = Organisation.objects.all().order_by('-created_at')
    serializer_class  = OrganisationSerializer
    filter_backends   = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields  = ['org_type']
    search_fields     = ['name', 'description']
    ordering_fields   = ['created_at', 'name']
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Organisation.objects.none()
        qs = Organisation.objects.all().order_by('-created_at')
        if self.request.user.is_staff:
            return qs
        if self.request.query_params.get('discovery') == 'true':
            return qs
        return qs.filter(
            Q(created_by=self.request.user) |
            Q(groups__members__user=self.request.user, groups__members__status='ACTIVE')
        ).distinct()

    def perform_create(self, serializer):
        organisation = serializer.save(created_by=self.request.user)

        # Création automatique du groupe Direction + rôle Leader pour le créateur
        group_type, _ = GroupType.objects.get_or_create(
            name="Direction",
            defaults={'description': 'Groupe administratif par défaut'}
        )
        group = Group.objects.create(
            name=f"Admin - {organisation.name}",
            organisation=organisation,
            type=group_type,
            created_by=self.request.user,
        )

        # ✅ FIX : get_or_create sûr via le helper (role_type est unique)
        leader_role = get_or_create_role(
            role_type=GroupRole.RoleType.LEADER,
            name='Chef de groupe',
        )

        MemberGroup.objects.get_or_create(
            user=self.request.user,
            group=group,
            defaults={
                'role': leader_role,
                'status': 'ACTIVE',
                'initiated_by': MemberGroup.InitiatedBy.ORGANISATION,
            }
        )


# ────────────────────────────────────────────────
# GroupType
# ────────────────────────────────────────────────

@swagger_crud
class GroupTypeViewSet(CacheInvalidationMixin, BaseModelViewSet):
    """Types de groupe — lecture libre, écriture admin."""
    cache_prefix       = 'group-types'
    queryset           = GroupType.objects.all().order_by('name')
    serializer_class   = GroupTypeSerializer
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name']
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ────────────────────────────────────────────────
# Group
# ────────────────────────────────────────────────

@swagger_crud
class GroupViewSet(CacheInvalidationMixin, BaseModelViewSet):
    """Groupes — leaders et propriétaires peuvent modifier."""
    cache_prefix       = 'groups'
    queryset           = group_base_queryset()
    serializer_class   = GroupSerializer
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['status', 'organisation', 'type']
    search_fields      = ['name', 'organisation__name']
    ordering_fields    = ['created_at', 'name']
    permission_classes = [IsAuthenticated, IsGroupLeader | IsOwnerOrAdmin]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return group_base_queryset().none()
        qs = group_base_queryset()
        if self.request.user.is_staff:
            return qs
        if self.request.query_params.get('discovery') == 'true':
            return qs
        return qs.filter(
            Q(organisation__created_by=self.request.user) |
            Q(members__user=self.request.user, members__status='ACTIVE')
        ).distinct()

    def perform_create(self, serializer):
        group = serializer.save(created_by=self.request.user)

        # ✅ FIX : get_or_create sûr via le helper (role_type est unique)
        leader_role = get_or_create_role(
            role_type=GroupRole.RoleType.LEADER,
            name='Chef de groupe',
        )

        MemberGroup.objects.get_or_create(
            user=self.request.user,
            group=group,
            defaults={
                'role': leader_role,
                'status': 'ACTIVE',
                'initiated_by': MemberGroup.InitiatedBy.ORGANISATION,
            },
        )


# ────────────────────────────────────────────────
# GroupRole
# ────────────────────────────────────────────────

@swagger_crud
class GroupRoleViewSet(CacheInvalidationMixin, BaseModelViewSet):
    """Rôles de groupe — lecture pour tous, écriture admin."""
    cache_prefix       = 'group-roles'
    queryset           = GroupRole.objects.all().order_by('name')
    serializer_class   = GroupRoleSerializer
    filter_backends    = [filters.SearchFilter]
    search_fields      = ['name', 'role_type']
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ────────────────────────────────────────────────
# MemberGroup
# ────────────────────────────────────────────────

@swagger_crud
class MemberGroupViewSet(CacheInvalidationMixin, BaseModelViewSet):
    """
    Membres de groupe.

    Actions custom :
      POST /{id}/approve/  — Leader approuve une demande agriculteur
      POST /{id}/accept/   — Agriculteur accepte une invitation
      POST /{id}/reject/   — Refus d'une demande (suppression)
      POST /{id}/cancel/   — Organisation annule une invitation (suppression)
    """
    cache_prefix       = 'member-groups'
    queryset           = member_group_base_queryset()
    serializer_class   = MemberGroupSerializer
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields   = ['status', 'group', 'role', 'user', 'initiated_by']
    search_fields      = ['user__username', 'group__name', 'role__role_type']
    permission_classes = [IsAuthenticated, CanAssignRole]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return member_group_base_queryset().none()
        qs = member_group_base_queryset()
        if self.request.user.is_staff:
            return qs
        # Un utilisateur voit ses propres adhésions + celles des groupes qu'il dirige
        return qs.filter(
            Q(user=self.request.user) |
            Q(
                group__members__user=self.request.user,
                group__members__role__role_type='LEADER',
                group__members__status='ACTIVE',
            )
        ).distinct()

    def perform_create(self, serializer):
        """Détermine automatiquement initiated_by selon qui fait la requête."""
        target_user = serializer.validated_data.get('user')
        initiated_by = (
            MemberGroup.InitiatedBy.USER
            if target_user == self.request.user
            else MemberGroup.InitiatedBy.ORGANISATION
        )
        serializer.save(status='PENDING', initiated_by=initiated_by)

    # ── Actions ──────────────────────────────────

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """Leader approuve une demande d'adhésion (initiated_by=USER)."""
        member = self.get_object()

        if member.initiated_by != MemberGroup.InitiatedBy.USER:
            return Response(
                {"error": "Cette entrée est une invitation. Utilisez /accept/ à la place."},
                status=400,
            )

        role_uuid = request.data.get('role_uuid')
        if role_uuid:
            try:
                member.role = GroupRole.objects.get(uuid=role_uuid)
            except GroupRole.DoesNotExist:
                return Response({'error': 'Rôle introuvable.'}, status=400)

        member.status = 'ACTIVE'
        member.save()
        return Response({"status": "Demande approuvée."})

    @action(detail=True, methods=['post'], url_path='accept')
    def accept(self, request, pk=None):
        """Agriculteur accepte une invitation (initiated_by=ORGANISATION)."""
        member = self.get_object()

        if member.user != request.user:
            return Response(
                {"error": "Vous ne pouvez pas accepter une invitation pour quelqu'un d'autre."},
                status=403,
            )

        member.status = 'ACTIVE'
        member.save()
        return Response({"status": "Invitation acceptée."})

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """Refus d'une demande par le leader → suppression."""
        self.get_object().delete()
        return Response({"status": "Demande refusée et supprimée."})

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Organisation annule une invitation en attente → suppression."""
        member = self.get_object()

        if member.initiated_by != MemberGroup.InitiatedBy.ORGANISATION:
            return Response(
                {"error": "Ceci est une demande agriculteur. Utilisez /reject/ à la place."},
                status=400,
            )

        is_leader = MemberGroup.objects.filter(
            user=request.user,
            group=member.group,
            role__role_type__in=['LEADER', 'ADMIN'],
            status='ACTIVE',
        ).exists()

        if not is_leader and not request.user.is_staff:
            return Response({"error": "Permission refusée."}, status=403)

        member.delete()
        return Response({"status": "Invitation annulée et supprimée."})
