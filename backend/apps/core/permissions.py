"""
apps/core/permissions.py
------------------------
Permissions DRF partagées par toutes les apps.
"""
import logging
from rest_framework import permissions

logger = logging.getLogger(__name__)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Lecture libre pour tous les utilisateurs authentifiés.
    Écriture (POST/PUT/PATCH/DELETE) réservée aux is_staff.
    Utilisé pour : Organisation, GroupType
    """
    def has_permission(self, request, view):
        logger.info(f"User {request.user} → {request.method} {view.__class__.__name__}")
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    L'utilisateur doit être le créateur (created_by) ou un admin.
    Utilisé pour : Parcel, Task, YieldRecord
    """
    def has_object_permission(self, request, view, obj):
        logger.info(f"User {request.user} → accès objet {obj}")
        return (
            obj.created_by == request.user
            or (request.user and request.user.is_staff)
        )


class IsGroupLeader(permissions.BasePermission):
    """
    Seuls les membres LEADER ou ADMIN d'un groupe peuvent le modifier.
    Utilisé pour : Group
    """
    def has_object_permission(self, request, view, obj):
        logger.info(f"User {request.user} → accès groupe {obj}")
        if request.method in permissions.SAFE_METHODS:
            return True
        member = obj.members.filter(user=request.user).first()
        return member and member.role.name.lower() in ["admin", "leader"]


class CanAssignRole(permissions.BasePermission):
    """
    Seul le LEADER actif d'un groupe peut modifier les rôles de ce groupe.
    Utilisé pour : MemberGroup
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        # Import différé pour éviter les imports circulaires
        from django.apps import apps
        MemberGroup = apps.get_model('SmartSaha', 'MemberGroup')
        return MemberGroup.objects.filter(
            user=request.user,
            group=obj.group,
            role__name="LEADER",
            status="ACTIVE",
        ).exists()
