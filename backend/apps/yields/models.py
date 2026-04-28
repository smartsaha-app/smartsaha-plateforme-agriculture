"""
apps/yields/models.py
---------------------
Modèles pour les rendements et prévisions de rendement.
"""
from django.db import models


class YieldRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    parcelCrop = models.ForeignKey(
        'crops.ParcelCrop',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='yield_records'
    )
    date = models.DateField()
    yield_amount = models.FloatField()
    area = models.FloatField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Relevé de rendement'
        verbose_name_plural = 'Relevés de rendement'
        ordering = ['-date']

    def __str__(self):
        parcel_name = self.parcelCrop.parcel.parcel_name if self.parcelCrop else 'N/A'
        return f"{parcel_name} - {self.date} - {self.yield_amount} kg - {self.area} m²"

    def yield_per_area(self) -> float | None:
        """Calcule le rendement par m². Retourne None si area est 0."""
        if not self.area:
            return None
        return round(self.yield_amount / self.area, 4)


class YieldForecast(models.Model):
    parcelCrop = models.ForeignKey(
        'crops.ParcelCrop',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='yield_forecasts'
    )
    forecast_date = models.DateField()
    predicted_yield = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Prévision de rendement'
        verbose_name_plural = 'Prévisions de rendement'
        unique_together = ("parcelCrop", "forecast_date")
        ordering = ['forecast_date']

    def __str__(self):
        parcel_name = self.parcelCrop.parcel.parcel_name if self.parcelCrop else 'N/A'
        return f"{parcel_name} - {self.forecast_date} - {self.predicted_yield:.2f} kg/ha"