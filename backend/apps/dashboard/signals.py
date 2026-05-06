"""
apps/dashboard/signals.py
--------------------------
Migré depuis SmartSaha/signals/dashboard_cache.py.
Invalide le cache dashboard à chaque modification des données clés.
Connecté au démarrage via DashboardConfig.ready().
"""
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.parcels.models import Parcel
from apps.crops.models import ParcelCrop       # ParcelCrop est dans apps.crops, pas apps.parcels
from apps.tasks.models import Task
from apps.weather.models import SoilData, ClimateData
from apps.yields.models import YieldRecord, YieldForecast


def _invalidate(user_id):
    cache.delete(f'dashboard_full_{user_id}')
    cache.delete(f'dashboard_{user_id}')
    cache.delete(f'dashboard_{user_id}_parcels')
    cache.delete(f'dashboard_{user_id}_soil')
    cache.delete(f'dashboard_{user_id}_weather')
    cache.delete(f'dashboard_{user_id}_enhanced_weather')
    cache.delete(f'dashboard_{user_id}_weather_overview')
    cache.delete(f'dashboard_{user_id}_yield')
    cache.delete(f'dashboard_{user_id}_task')


@receiver([post_save, post_delete], sender=Parcel)
def clear_on_parcel(sender, instance, **kwargs):
    if instance.owner_id:
        _invalidate(instance.owner_id)


@receiver([post_save, post_delete], sender=ParcelCrop)
def clear_on_parcelcrop(sender, instance, **kwargs):
    try:
        if instance.parcel and instance.parcel.owner_id:
            _invalidate(instance.parcel.owner_id)
    except Exception:
        pass


@receiver([post_save, post_delete], sender=YieldRecord)
@receiver([post_save, post_delete], sender=YieldForecast)
def clear_on_yield(sender, instance, **kwargs):
    try:
        user_id = instance.parcelCrop.parcel.owner_id
        if user_id:
            _invalidate(user_id)
    except Exception:
        pass


@receiver([post_save, post_delete], sender=Task)
def clear_on_task(sender, instance, **kwargs):
    try:
        user_id = instance.parcelCrop.parcel.owner_id
        if user_id:
            _invalidate(user_id)
    except Exception:
        pass


@receiver([post_save, post_delete], sender=SoilData)
@receiver([post_save, post_delete], sender=ClimateData)
def clear_on_external_data(sender, instance, **kwargs):
    try:
        user_id = instance.parcel.owner_id
        if user_id:
            _invalidate(user_id)
    except Exception:
        pass
