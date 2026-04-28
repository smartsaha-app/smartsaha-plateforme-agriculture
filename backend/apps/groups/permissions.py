"""
apps/groups/permissions.py
--------------------------
Permissions spécifiques aux groupes.
Déplacées depuis SmartSaha/permissions.py.

NOTE : IsAdminOrReadOnly, IsGroupLeader, IsOwnerOrAdmin sont copiées ici
car elles sont fortement couplées aux modèles groups/.
Les permissions génériques (IsAuthenticated etc.) viennent de DRF.
"""
import logging
from rest_framework import permissions

logger = logging.getLogger(__name__)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Lecture publique, écriture réservée aux admins (is_staff)."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsGroupLeader(permissions.BasePermission):
    """Seuls les membres avec rôle 'leader' ou 'admin' dans le groupe peuvent modifier."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Si l'objet est un MemberGroup, on vérifie l'accès au groupe parent
        from apps.groups.models import MemberGroup
        group = obj.group if isinstance(obj, MemberGroup) else obj
        
        return MemberGroup.objects.filter(
            user=request.user,
            group=group,
            role__role_type__in=["ADMIN", "LEADER"],
            status="ACTIVE"
        ).exists()


class IsOwnerOrAdmin(permissions.BasePermission):
    """Le créateur (created_by) ou un admin global peut modifier."""
    def has_object_permission(self, request, view, obj):
        return (
            obj.created_by == request.user
            or (request.user and request.user.is_staff)
        )


class IsMemberOwner(permissions.BasePermission):
    """L'utilisateur concerné par l'entrée MemberGroup (lui-même)."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CanAssignRole(permissions.BasePermission):
    """
    Vérifie que l'utilisateur est leader actif du groupe concerné,
    ou superuser.
    Permet aussi l'autocréation (demande d'adhésion) par l'utilisateur lui-même.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        # Le membre lui-même peut lire/modifier son statut (Accept/Reject)
        if hasattr(obj, 'user') and obj.user == request.user:
            return True

        from apps.groups.models import MemberGroup
        group = obj.group if hasattr(obj, 'group') else obj
        
        return MemberGroup.objects.filter(
            user=request.user,
            group=group,
            role__role_type__in=["ADMIN", "LEADER"],
            status="ACTIVE",
        ).exists()