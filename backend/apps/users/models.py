"""
apps/users/models.py
--------------------
Proxy du modèle User de SmartSaha.
Même table BDD, même AUTH_USER_MODEL — zéro migration destructive.
On peut ajouter ici des méthodes métier sans toucher à SmartSaha.
"""
# Obsolete SmartSaha.models imports removed.

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# class User(_SmartSahaUser):
#     """
#     Proxy du modèle User SmartSaha.
#     Utilise exactement la même table 'SmartSaha_user'.
#     Toutes les FK vers AUTH_USER_MODEL restent valides.

#     Avantages du proxy :
#     - Peut avoir ses propres managers
#     - Peut avoir des méthodes métier supplémentaires
#     - Visible dans l'admin Django séparément
#     - Importable via apps.users.User dans les nouvelles apps
#     """

#     class Meta:
#         proxy = True
#         app_label = 'users'
#         verbose_name = 'Utilisateur'
#         verbose_name_plural = 'Utilisateurs'

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('AGRICULTEUR', 'Agriculteur'),
        ('ORGANISATION', 'Organisation'),
        ('BUYER', 'Acheteur'),
        ('SELLER_PUR', 'Vendeur Pur'),
        ('AGR_SELLER', 'Agri-Vendeur'),
    ]

    KYC_STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvé'),
        ('REJECTED', 'Rejeté'),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    kyc_status = models.CharField(max_length=10, choices=KYC_STATUS_CHOICES, default='PENDING')
    profile_completeness = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} - {self.email}"

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='smartsaha_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='smartsaha_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # ── Méthodes métier ajoutées (n'existaient pas dans SmartSaha) ──

    def get_active_memberships(self):
        """Retourne tous les groupes actifs de l'utilisateur."""
        return self.group_memberships.filter(status='ACTIVE').select_related(
            'group', 'role'
        )

    def is_leader_of(self, group) -> bool:
        """Vérifie si l'utilisateur est LEADER d'un groupe donné."""
        return self.group_memberships.filter(
            group=group,
            role__name='LEADER',
            status='ACTIVE',
        ).exists()

    def get_spaces(self) -> dict:
        """
        Retourne les espaces accessibles à cet utilisateur.
        Utilisé par le frontend pour afficher la sidebar et gérer les redirections.
        """
        return {
            'agriculture': self.role in ['AGRICULTEUR', 'AGR_SELLER', 'SELLER_PUR', 'ADMIN'],
            'organisation': (
                self.role == 'ORGANISATION' or
                self.group_memberships.filter(status='ACTIVE', role__role_type='LEADER').exists() or 
                self.organisations_created.exists()
            ),
            'superviseur': self.is_staff or self.role == 'ADMIN',
        }


class BIReport(models.Model):
    """
    Stocke les rapports agrégés pour le dashboard BI.
    Permet de pré-calculer et sauvegarder des résumés pour les entreprises.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    filters = models.JSONField(null=True, blank=True)        # filtres appliqués
    data_snapshot = models.JSONField(null=True, blank=True)  # données agrégées

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"
