"""
apps/fire/models.py
-------------------
Modèle FireAlert : stocke les points chauds FIRMS (NASA) détectés
à proximité des parcelles utilisateurs.
"""
import uuid
from django.db import models


class FireAlert(models.Model):
    """
    Un point chaud FIRMS détecté par satellite (MODIS/VIIRS).
    Lié optionnellement à une parcelle si elle se trouve dans le rayon d'alerte.
    """
    SEVERITY_CHOICES = [
        ('MEDIUM',   'Moyen'),
        ('HIGH',     'Élevé'),
        ('CRITICAL', 'Critique'),
    ]

    SOURCE_CHOICES = [
        ('MODIS_NRT',  'MODIS Near Real-Time'),
        ('VIIRS_NOAA', 'VIIRS NOAA-20'),
        ('VIIRS_SNPP', 'VIIRS S-NPP'),
    ]

    # Identifiant
    uuid        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Coordonnées du point chaud
    latitude    = models.FloatField()
    longitude   = models.FloatField()

    # Données FIRMS
    brightness  = models.FloatField(help_text="Température de brillance (Kelvin)")
    confidence  = models.IntegerField(default=50, help_text="Confiance détection (%)")
    acq_date    = models.DateField(help_text="Date d'acquisition satellite")
    acq_time    = models.CharField(max_length=10, blank=True, help_text="Heure d'acquisition UTC")
    satellite   = models.CharField(max_length=10, blank=True)
    source      = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='MODIS_NRT')

    # Parcelle affectée (si dans le rayon)
    parcel      = models.ForeignKey(
        'parcels.Parcel',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='fire_alerts',
        help_text="Parcelle la plus proche dans le rayon d'alerte"
    )
    distance_km = models.FloatField(
        null=True, blank=True,
        help_text="Distance en km entre le feu et le centroïde de la parcelle"
    )

    # Sévérité calculée
    severity    = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='HIGH')

    # Statut
    is_active   = models.BooleanField(default=True)
    is_notified = models.BooleanField(default=False, help_text="Email de notification envoyé")

    # Timestamps
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering    = ['-acq_date', '-brightness']
        verbose_name        = 'Alerte Feu'
        verbose_name_plural = 'Alertes Feu'
        unique_together = [('latitude', 'longitude', 'acq_date', 'acq_time', 'satellite')]
        indexes = [
            models.Index(fields=['acq_date', 'is_active']),
            models.Index(fields=['parcel', 'is_active']),
            models.Index(fields=['severity']),
        ]

    def __str__(self):
        return (
            f"🔥 Feu [{self.severity}] lat={self.latitude:.3f} lon={self.longitude:.3f} "
            f"— {self.acq_date}"
        )

    @property
    def is_critical(self) -> bool:
        return self.severity == 'CRITICAL'
