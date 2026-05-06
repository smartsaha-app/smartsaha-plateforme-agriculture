"""
apps/yields/views.py
--------------------
Vues pour les rendements et prévisions ML.
"""
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes

from apps.core.mixins import CacheInvalidationMixin
from apps.crops.models import ParcelCrop
from apps.groups.models import MemberGroup
from apps.yields.models import YieldRecord, YieldForecast
from apps.yields.serializers import YieldRecordSerializer, YieldForecastSerializer
from apps.yields.services import YieldForecastService, YieldAnalyticsService
from django.db.models import Q


@extend_schema_view(
    list=extend_schema(tags=['Rendements & IA']),
    retrieve=extend_schema(tags=['Rendements & IA']),
    create=extend_schema(tags=['Rendements & IA']),
    update=extend_schema(tags=['Rendements & IA']),
    partial_update=extend_schema(tags=['Rendements & IA']),
    destroy=extend_schema(tags=['Rendements & IA']),
)
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


@extend_schema(tags=['Rendements & IA'])
class YieldForecastView(CacheInvalidationMixin, APIView):
    """Prévision de rendement par régression linéaire."""

    @extend_schema(
        summary="Prévision de rendement (IA)",
        description="Lance la régression linéaire et retourne la prévision J+7.",
        tags=['Rendements & IA'],
        parameters=[
            OpenApiParameter(
                name='parcel_crop_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID de la ParcelCrop pour laquelle calculer la prévision."
            )
        ],
        responses={
            200: YieldForecastSerializer,
            400: OpenApiTypes.OBJECT,
            403: OpenApiTypes.OBJECT,
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



@extend_schema(tags=['Rendements & IA'])
class YieldAnalyticsView(APIView):
    """
    GET /api/v2/analytics/yields/
    Retourne les statistiques de rendement agrégées par parcelle.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Statistiques globales des rendements",
        tags=['Rendements & IA'],
        responses={200: OpenApiTypes.OBJECT}
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
