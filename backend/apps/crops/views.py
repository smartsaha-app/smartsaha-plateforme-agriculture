"""
apps/crops/views.py
-------------------
ViewSets pour Crop, Variety, StatusCrop, ParcelCrop.
"""
from django.db import models
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.core.mixins import CacheInvalidationMixin, BaseModelViewSet
from apps.crops.models import Crop, StatusCrop, Variety, ParcelCrop
from apps.groups.models import MemberGroup
from apps.crops.serializers import (
    CropSerializer, StatusCropSerializer, VarietySerializer, ParcelCropSerializer
)


@method_decorator(name='list', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='retrieve', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='create', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='update', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='partial_update', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='destroy', decorator=extend_schema(tags=['Cultures & Variétés']))
class VarietyViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    """Variétés de cultures — lecture publique."""
    queryset = Variety.objects.all()
    serializer_class = VarietySerializer
    permission_classes = [permissions.AllowAny]
    cache_prefix = 'variety'


@method_decorator(name='list', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='retrieve', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='create', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='update', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='partial_update', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='destroy', decorator=extend_schema(tags=['Cultures & Variétés']))
class StatusCropViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    """Statuts de culture — lecture publique."""
    queryset = StatusCrop.objects.all()
    serializer_class = StatusCropSerializer
    permission_classes = [permissions.AllowAny]
    cache_prefix = 'status_crop'


@method_decorator(name='list', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='retrieve', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='create', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='update', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='partial_update', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='destroy', decorator=extend_schema(tags=['Cultures & Variétés']))
class CropViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    """Cultures disponibles — lecture publique."""
    queryset = Crop.objects.all().select_related('variety')
    serializer_class = CropSerializer
    permission_classes = [permissions.AllowAny]
    cache_prefix = 'crop'


@method_decorator(name='list', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='retrieve', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='create', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='update', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='partial_update', decorator=extend_schema(tags=['Cultures & Variétés']))
@method_decorator(name='destroy', decorator=extend_schema(tags=['Cultures & Variétés']))
class ParcelCropViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    """Cultures d'une parcelle — accès restreint au propriétaire."""
    serializer_class = ParcelCropSerializer
    permission_classes = [permissions.IsAuthenticated]
    cache_prefix = 'parcel_crop'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ParcelCrop.objects.none()
        
        user = self.request.user
        # Cultures possédées en propre
        queryset = ParcelCrop.objects.filter(parcel__owner=user)
        
        # S'il est leader d'un groupe, il voit les cultures des membres
        led_groups = MemberGroup.objects.filter(
            user=user, 
            role__role_type='LEADER', 
            status='ACTIVE'
        ).values_list('group_id', flat=True)
        
        if led_groups.exists():
            member_ids = MemberGroup.objects.filter(
                group_id__in=led_groups, 
                status='ACTIVE'
            ).values_list('user_id', flat=True)
            
            queryset = ParcelCrop.objects.filter(
                models.Q(parcel__owner=user) | models.Q(parcel__owner_id__in=member_ids)
            ).distinct()

        return (
            queryset
            .select_related('parcel', 'crop', 'crop__variety', 'status')
        )

    def perform_create(self, serializer):
        parcel = serializer.validated_data['parcel']
        if parcel.owner != self.request.user:
            raise PermissionDenied("Vous ne pouvez pas ajouter de culture à cette parcelle")
        serializer.save()

    def perform_update(self, serializer):
        parcel = serializer.validated_data.get('parcel', serializer.instance.parcel)
        if parcel.owner != self.request.user:
            raise PermissionDenied("Vous ne pouvez pas modifier cette culture")
        serializer.save()
