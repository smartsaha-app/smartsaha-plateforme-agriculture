"""
apps/yields/views.py
--------------------
Vues pour les rendements et prévisions ML.
"""
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.core.mixins import CacheInvalidationMixin
from apps.crops.models import ParcelCrop
from apps.groups.models import MemberGroup
from apps.yields.models import YieldRecord, YieldForecast
from apps.yields.serializers import YieldRecordSerializer, YieldForecastSerializer
from apps.yields.services import YieldForecastService, YieldAnalyticsService
from django.db.models import Q


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Rendements & IA']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Rendements & IA']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Rendements & IA']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Rendements & IA']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Rendements & IA']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Rendements & IA']))
class YieldRecordViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    """Records de récolte — accès restreint au propriétaire."""
    serializer_class = YieldRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    cache_prefix = 'yield_record'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return YieldRecord.objects.none()
        
        user = self.request.user
        queryset = YieldRecord.objects.filter(parcelCrop__parcel__owner=user)
        
        # Extension aux membres pour les leaders
        led_groups = MemberGroup.objects.filter(
            user=user, role__role_type='LEADER', status='ACTIVE'
        ).values_list('group_id', flat=True)
        
        if led_groups.exists():
            member_ids = MemberGroup.objects.filter(
                group_id__in=led_groups, status='ACTIVE'
            ).values_list('user_id', flat=True)
            
            queryset = YieldRecord.objects.filter(
                Q(parcelCrop__parcel__owner=user) | 
                Q(parcelCrop__parcel__owner_id__in=member_ids)
            ).distinct()

        return queryset.select_related('parcelCrop', 'parcelCrop__parcel')


@swagger_auto_schema(tags=['Rendements & IA'])
class YieldForecastView(CacheInvalidationMixin, APIView):
    """Prévision de rendement par régression linéaire."""

    @swagger_auto_schema(
        operation_summary="Prévision de rendement (IA)",
        operation_description="Lance la régression linéaire et retourne la prévision J+7.",
        tags=['Rendements & IA'],
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT),
            400: "Pas assez de données pour prévoir",
            403: "Parcelle invalide"
        }
    )
    def get(self, request, parcel_crop_id):
        try:
            parcel_crop = ParcelCrop.objects.get(
                id=parcel_crop_id,
                parcel__owner=request.user,
            )
        except ParcelCrop.DoesNotExist:
            return Response(
                {'error': "Cette parcelle n'existe pas ou ne vous appartient pas"},
                status=status.HTTP_403_FORBIDDEN,
            )

        service = YieldForecastService(parcel_crop)
        forecast = service.save_forecast(days_ahead=7)

        if not forecast:
            return Response(
                {'error': 'Pas assez de données pour prévoir (minimum 1 relevé requis)'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        
        return Response(YieldForecastSerializer(forecast).data)  # ← serializer propre



@swagger_auto_schema(tags=['Rendements & IA'])
class YieldAnalyticsView(APIView):
    """
    GET /api/v2/analytics/yields/
    Retourne les statistiques de rendement agrégées par parcelle.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Statistiques globales des rendements",
        tags=['Rendements & IA'],
        responses={200: openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))}
    )
    def get(self, request):
        service = YieldAnalyticsService(user=request.user)
        stats = service.get_user_stats()
        if not stats:
            return Response(
                {'detail': 'Aucune donnée de rendement disponible.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(stats)