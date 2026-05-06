"""
apps/parcels/views.py
"""
import logging
from django.db import models
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiTypes

from apps.core.mixins import CacheInvalidationMixin
from apps.parcels.models import Parcel, ParcelPoint
from apps.groups.models import MemberGroup
from apps.parcels.serializers import ParcelSerializer, ParcelPointSerializer, ParcelWeatherSerializer
from apps.parcels.services import ParcelDataService

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(tags=['Parcelles']),
    retrieve=extend_schema(tags=['Parcelles']),
    create=extend_schema(tags=['Parcelles']),
    update=extend_schema(tags=['Parcelles']),
    partial_update=extend_schema(tags=['Parcelles']),
    destroy=extend_schema(tags=['Parcelles']),
)
class ParcelViewSet(viewsets.ModelViewSet):
    """CRUD parcelles — accès restreint au propriétaire uniquement."""
    serializer_class = ParcelSerializer
    lookup_field = 'uuid'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Parcel.objects.none()
        
        user = self.request.user
        # Parcelles possédées en propre
        queryset = Parcel.objects.filter(owner=user)
        
        # S'il est leader d'un groupe, il voit les parcelles des membres
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
            
            queryset = Parcel.objects.filter(
                models.Q(owner=user) | models.Q(owner_id__in=member_ids)
            ).distinct()
            
        return queryset.select_related('owner').prefetch_related('parcel_points')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("Vous ne pouvez pas modifier cette parcelle")
        serializer.save()

    # ─── Actions GPS / Météo ────────────────────────────────────────────────

    @extend_schema(
        summary="Lister avec points GPS",
        tags=['Parcelles'],
    )
    @action(detail=False, methods=['get'])
    def with_gps(self, request):
        parcels = self.get_queryset().exclude(points=[])
        return Response({
            'success': True,
            'count': parcels.count(),
            'parcels': ParcelWeatherSerializer(parcels, many=True).data
        })

    @extend_schema(
        summary="Informations Météo",
        tags=['Parcelles'],
    )
    @action(detail=True, methods=['get'])
    def weather_info(self, request, uuid=None):
        parcel = self.get_object()
        return Response({
            'success': True,
            'parcel': ParcelWeatherSerializer(parcel).data,
            'can_collect_weather': parcel.has_gps_points()
        })

    # ─── Full data (anciennement ParcelFullDataViewSet) ─────────────────────

    @extend_schema(
        summary="Agrégation complète des données de la parcelle",
        description="Rassemble les données analytiques (Culture, Tâches, Rendement, Météo...)",
        tags=['Parcelles'],
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=True, methods=['get'], url_path='full_data')
    def full_data(self, request, uuid=None):
        try:
            parcel = self.get_object()  # déjà filtré par owner via get_queryset
            data = ParcelDataService.get_complete_parcel_data(str(parcel.uuid))
            if not data:
                return Response({'error': 'Parcel data not found'}, status=404)
            return Response({
                'parcel':        data['parcel'],
                'soil_data':     ParcelDataService.serialize_soil_data(data['soil_data']),
                'weather_data':  ParcelDataService.serialize_weather_data(data['weather_data']),
                'parcel_crops':  data['crops'],
                'yield_records': data['yield_records'],
                'tasks':         data['tasks'],
                'tasks_summary': data['tasks_summary'],
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"full_data error: {e}")
            return Response({'error': 'Internal server error'}, status=500)

    @extend_schema(
        summary="Liste des tâches de la parcelle",
        tags=['Parcelles'],
    )
    @action(detail=True, methods=['get'], url_path='tasks')
    def parcel_tasks(self, request, uuid=None):
        try:
            parcel = self.get_object()
            return Response(ParcelDataService.build_parcel_tasks(parcel))
        except Exception as e:
            logger.error(f"parcel_tasks error: {e}")
            return Response({'error': 'Internal server error'}, status=500)

    @extend_schema(
        summary="Rafraîchir les données du sol",
        tags=['Parcelles'],
    )
    @action(detail=True, methods=['post'], url_path='refresh_soil_data')
    def refresh_soil_data(self, request, uuid=None):
        try:
            parcel = self.get_object()
            soil = ParcelDataService.refresh_soil_data(parcel)
            return Response({
                'status': 'success',
                'soil_data': ParcelDataService.serialize_soil_data(soil)
            })
        except Exception as e:
            logger.error(f"refresh_soil_data error: {e}")
            return Response({'error': 'Internal server error'}, status=500)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

@method_decorator(name='list',           decorator=extend_schema(tags=['Parcelles']))
@method_decorator(name='retrieve',       decorator=extend_schema(tags=['Parcelles']))
@method_decorator(name='create',         decorator=extend_schema(tags=['Parcelles']))
@method_decorator(name='update',         decorator=extend_schema(tags=['Parcelles']))
@method_decorator(name='partial_update', decorator=extend_schema(tags=['Parcelles']))
@method_decorator(name='destroy',        decorator=extend_schema(tags=['Parcelles']))
class ParcelPointViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = ParcelPoint.objects.all().select_related('parcel')
    serializer_class = ParcelPointSerializer
    pagination_class = LargeResultsSetPagination
    cache_prefix = 'parcel_point'
    cache_prefix = 'parcel_point'
    use_object_cache = True

    def perform_create(self, serializer):
        instance = serializer.save()
        self.invalidate_cache(getattr(instance, 'parcel', instance))
        return instance
