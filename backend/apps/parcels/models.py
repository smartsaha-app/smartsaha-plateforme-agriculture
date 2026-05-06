"""
apps/parcels/models.py
----------------------
Modèles Parcel et ParcelPoint.
"""
from django.conf import settings
from django.db import models
import uuid


# ══════════════════════════════════════════════════════════════════════════════
# Parcel
# ══════════════════════════════════════════════════════════════════════════════
class Parcel(models.Model):
    uuid       = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parcels')
    parcel_name = models.CharField(max_length=255)
    points     = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.parcel_name} - {self.owner.username}"

    # ── GPS ───────────────────────────────────────────────────────────────────

    def has_gps_points(self) -> bool:
        """Vérifie si la parcelle a des points GPS définis."""
        return bool(self.points) and len(self.points) > 0

    def get_center(self) -> dict | None:
        """Calcule le centroïde du polygone GPS.
        Retourne {'lat': float, 'lng': float} ou None si pas de points.
        """
        if not self.points or not isinstance(self.points, list):
            return None
        try:
            lats = [p['lat'] for p in self.points]
            lngs = [p['lng'] for p in self.points]
            return {
                'lat': round(sum(lats) / len(lats), 6),
                'lng': round(sum(lngs) / len(lngs), 6),
            }
        except (KeyError, TypeError, ZeroDivisionError):
            return None

    def add_point(self, lat: float, lng: float, order: int):
        """Ajoute un point GPS à la parcelle."""
        self.points.append({"lat": lat, "lng": lng, "order": order})
        self.save()

    def get_polygon(self) -> list:
        """Retourne le polygone trié par ordre [(lat, lng), ...]."""
        return [
            (p["lat"], p["lng"])
            for p in sorted(self.points or [], key=lambda x: x.get("order", 0))
        ]

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Parcelle'
        verbose_name_plural = 'Parcelles'


# ══════════════════════════════════════════════════════════════════════════════
# ParcelPoint
# ══════════════════════════════════════════════════════════════════════════════
class ParcelPoint(models.Model):
    parcel    = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='parcel_points')
    latitude  = models.FloatField()
    longitude = models.FloatField()
    order     = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parcel.parcel_name} - point {self.order}"

    class Meta:
        ordering = ['order']
        verbose_name = 'Point de parcelle'
        verbose_name_plural = 'Points de parcelle'
