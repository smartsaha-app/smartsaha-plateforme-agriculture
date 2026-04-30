"""
apps/core/models.py
-------------------
Modèles abstraits partagés par toutes les apps.
Ne définit AUCUNE table concrète en base de données.
"""
import uuid
from django.db import models
from django.conf import settings


class TimestampedModel(models.Model):
    """
    Ajoute created_at et updated_at à tout modèle qui en hérite.
    Utilisé pour les modèles simples sans propriétaire (Crop, Variety…).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # ← Aucune table créée


class UUIDModel(models.Model):
    """
    Ajoute un UUID comme clé primaire.
    Plus sécurisé qu'un entier auto-incrémenté pour les APIs publiques.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimestampedModel):
    """
    Modèle de base complet pour tous les modèles principaux de SmartSaha.
    Fournit :
      - uuid       → clé primaire UUID
      - created_at → date de création (auto)
      - updated_at → date de modification (auto)
      - created_by → utilisateur créateur (FK vers User)
      - updated_by → dernier utilisateur modificateur (FK vers User)

    Utilisation :
        class Organisation(BaseModel):
            name = models.CharField(max_length=150)
            # uuid, created_at, updated_at, created_by, updated_by
            # sont hérités automatiquement
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='%(app_label)s_%(class)s_created',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='%(app_label)s_%(class)s_updated',
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']