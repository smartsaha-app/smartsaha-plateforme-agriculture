"""
apps/groups/models.py
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Organisation(models.Model):
    class OrganisationType(models.TextChoices):
        GOVERNMENT = "GOVERNMENT", "Gouvernementale"
        NGO = "NGO", "ONG"
        PRIVATE = "PRIVATE", "Privée"
        COOP = "COOP", "Coopérative"
        OTHER = "OTHER", "Autre"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    org_type = models.CharField(max_length=50, choices=OrganisationType.choices, default=OrganisationType.OTHER)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="organisations_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="organisations_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GroupType(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    class GroupStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Actif"
        INACTIVE = "INACTIVE", "Inactif"
        SUSPENDED = "SUSPENDED", "Suspendu"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    type = models.ForeignKey(GroupType, models.CASCADE, null=False, blank=False, related_name="groups")
    organisation = models.ForeignKey(Organisation, models.CASCADE, null=False, related_name="groups")
    status = models.CharField(max_length=20, choices=GroupStatus.choices, default=GroupStatus.ACTIVE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="groups_created")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="groups_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_active_members_count(self) -> int:
        return self.members.filter(status='ACTIVE').count()

    def get_leader(self):
        return self.members.filter(
            role__role_type='LEADER', status='ACTIVE'
        ).select_related('user').first()

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["organisation"]),
            models.Index(fields=['organisation', 'status']),
            models.Index(fields=['type', 'status']),
            models.Index(fields=["type"]),
        ]


class GroupRole(models.Model):
    class RoleType(models.TextChoices):
        LEADER    = "LEADER",    "Chef de groupe"
        SECRETARY = "SECRETARY", "Secrétaire"
        MEMBER    = "MEMBER",    "Membre"
        AUDITOR   = "AUDITOR",   "Auditeur interne"
        OTHER     = "OTHER",     "Autre"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ✅ FIX : unique=True garantit un seul GroupRole par role_type
    role_type = models.CharField(
        max_length=50,
        choices=RoleType.choices,
        default=RoleType.MEMBER,
        unique=True,
    )

    # name n'est plus unique car role_type l'est déjà
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class MemberGroup(models.Model):
    class MembershipStatus(models.TextChoices):
        ACTIVE   = "ACTIVE",   "Actif"
        INACTIVE = "INACTIVE", "Inactif"
        PENDING  = "PENDING",  "En attente"

    class InitiatedBy(models.TextChoices):
        USER         = "USER",         "Demande par l'agriculteur"
        ORGANISATION = "ORGANISATION", "Invitation par l'organisation"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_memberships")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    role = models.ForeignKey(GroupRole, models.CASCADE, null=False, related_name="members_with_role")
    status = models.CharField(max_length=20, choices=MembershipStatus.choices, default=MembershipStatus.ACTIVE)

    initiated_by = models.CharField(
        max_length=20,
        choices=InitiatedBy.choices,
        default=InitiatedBy.ORGANISATION,
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"

    def is_leader(self) -> bool:
        return self.role.role_type == 'LEADER'

    def is_active(self) -> bool:
        return self.status == 'ACTIVE'

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["group"]),
            models.Index(fields=["role"]),
            models.Index(fields=["initiated_by"]),
            models.Index(fields=['group', 'status']),
            models.Index(fields=['role', 'status']),
        ]
        unique_together = ("user", "group")