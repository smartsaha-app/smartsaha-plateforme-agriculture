"""
apps/parcels/views.py
"""
import logging
import math
from django.db import models
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, status
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


def _compute_area_ha(points: list) -> float:
    """Calcule la superficie en ha depuis les données brutes parcel_points.
    Supporte {lat, lng} (JSONField) et {latitude, longitude} (serializer input).
    Réplique la formule de Parcel.area_ha pour valider avant sauvegarde.
    """
    if not points or len(points) < 3:
        return 0.0
    try:
        area = 0.0
        n = len(points)
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            x1 = float(p1.get('lat', p1.get('latitude', 0)))
            y1 = float(p1.get('lng', p1.get('longitude', 0)))
            x2 = float(p2.get('lat', p2.get('latitude', 0)))
            y2 = float(p2.get('lng', p2.get('longitude', 0)))
            area += x1 * y2 - x2 * y1
        area = abs(area / 2.0)
        avg_lat = sum(float(p.get('lat', p.get('latitude', 0))) for p in points) / n
        area_m2 = area * 111000.0 * 111000.0 * math.cos(math.radians(avg_lat))
        return round(area_m2 / 10000.0, 4)
    except Exception:
        return 0.0


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
            
        return queryset.select_related('owner').prefetch_related('parcel_points', 'parcel_crops')

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_pro_active():
            # Plan GRATUIT — max 3 parcelles
            if Parcel.objects.filter(owner=user).count() >= 3:
                return Response(
                    {'code': 'PLAN_LIMIT_PARCELS',
                     'detail': 'Limite de 3 parcelles atteinte (offre Gratuite). Passez à Pro pour en créer plus.'},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # Plan GRATUIT — surface max 0.2 ha (2 000 m²)
            raw_points = request.data.get('parcel_points', [])
            if raw_points and len(raw_points) >= 3:
                area = _compute_area_ha(raw_points)
                if area > 0.2:
                    return Response(
                        {'code': 'PLAN_LIMIT_SURFACE',
                         'detail': f'La surface calculée ({area:.2f} ha) dépasse 2 000 m². Réservé à l\'offre Pro.'},
                        status=status.HTTP_403_FORBIDDEN,
                    )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        user = request.user
        # Si le plan FREE est actif et que la requête contient de nouveaux points, vérifier la surface
        if not user.is_pro_active() and 'parcel_points' in request.data:
            raw_points = request.data.get('parcel_points', [])
            if raw_points and len(raw_points) >= 3:
                area = _compute_area_ha(raw_points)
                if area > 0.2:
                    return Response(
                        {'code': 'PLAN_LIMIT_SURFACE',
                         'detail': f'La surface calculée ({area:.2f} ha) dépasse 2 000 m². Réservé à l\'offre Pro.'},
                        status=status.HTTP_403_FORBIDDEN,
                    )
        return super().update(request, *args, **kwargs)

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
