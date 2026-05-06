"""
apps/crops/models.py
--------------------
Modèles pour les cultures, variétés, statuts et associations parcelle-culture.
"""
from django.db import models


class Variety(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Variété'
        verbose_name_plural = 'Variétés'
        ordering = ['name']

    def __str__(self):
        return self.name


class StatusCrop(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Statut de culture'
        verbose_name_plural = 'Statuts de culture'
        ordering = ['name']

    def __str__(self):
        return self.name


class Crop(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    variety = models.ForeignKey(
        'Variety',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='crops'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Culture'
        verbose_name_plural = 'Cultures'
        ordering = ['-created_at']

    def __str__(self):
        return self.get_display_name()

    def get_display_name(self) -> str:
        """Retourne 'Nom (Variété)' ou juste 'Nom' si pas de variété."""
        if self.variety:
            return f"{self.name} ({self.variety.name})"
        return self.name


class ParcelCrop(models.Model):
    parcel = models.ForeignKey(
        'parcels.Parcel',
        on_delete=models.CASCADE,
        related_name='parcel_crops'
    )
    crop = models.ForeignKey(
        'crops.Crop',
        on_delete=models.CASCADE,
        related_name='parcel_crops'
    )
    planting_date = models.DateField()
    harvest_date = models.DateField(null=True, blank=True)
    area = models.FloatField()
    status = models.ForeignKey(
        'StatusCrop',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parcel_crops'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Culture de parcelle'
        verbose_name_plural = 'Cultures de parcelle'
        ordering = ['-created_at']

    def __str__(self):
        status_name = self.status.name if self.status else 'Aucun statut'
        return f"{self.parcel.parcel_name} - {self.crop.name} - {status_name}"

    def is_active(self) -> bool:
        """Retourne True si la culture est encore en cours (pas récoltée)."""
        return self.status is None or self.status.name.lower() != 'harvested'

    def days_until_harvest(self) -> int | None:
        """Retourne le nombre de jours avant la récolte prévue, ou None."""
        from django.utils import timezone
        if not self.harvest_date:
            return None
        return (self.harvest_date - timezone.now().date()).days
