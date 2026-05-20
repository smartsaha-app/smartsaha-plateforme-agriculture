"""
apps/parcels/models.py
----------------------
Modèles Parcel et ParcelPoint.
"""
from django.conf import settings
from django.db import models
import uuid
import math


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

    # ── CALCULS DYNAMIQUES ────────────────────────────────────────────────────

    @property
    def area_ha(self) -> float:
        """Calcule la superficie de la parcelle en hectares à partir des points GPS."""
        if not self.points or len(self.points) < 3:
            return 0.0
        try:
            area = 0.0
            n = len(self.points)
            for i in range(n):
                p1 = self.points[i]
                p2 = self.points[(i + 1) % n]
                x1, y1 = float(p1['lat']), float(p1['lng'])
                x2, y2 = float(p2['lat']), float(p2['lng'])
                area += x1 * y2 - x2 * y1
            area = abs(area / 2.0)
            avg_lat = sum(float(p['lat']) for p in self.points) / n
            area_m2 = area * 111000.0 * 111000.0 * math.cos(math.radians(avg_lat))
            return round(area_m2 / 10000.0, 2)
        except (KeyError, ValueError, TypeError, ZeroDivisionError):
            return 0.0

    @property
    def is_exploited(self) -> bool:
        """Indique si la parcelle est liée à au moins une culture."""
        # Utiliser .all() pour tirer parti du prefetch_related dans les vues.
        return len(self.parcel_crops.all()) > 0

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
