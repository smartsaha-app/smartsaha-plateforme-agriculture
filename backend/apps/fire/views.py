"""
apps/fire/views.py
------------------
Endpoints REST pour l'alerte feu :

  GET  /api/fire/alerts/                  → liste des alertes actives
  GET  /api/fire/alerts/summary/          → stats globales
  GET  /api/fire/alerts/my_parcels/       → alertes feu pour MES parcelles (auth)
  POST /api/fire/alerts/refresh/          → déclenche manuellement le pipeline FIRMS
  POST /api/fire/alerts/{uuid}/dismiss/   → désactiver une alerte
"""
import logging
from datetime import date, timedelta

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from apps.fire.models import FireAlert
from apps.fire.serializers import FireAlertSerializer, FireAlertSummarySerializer
from apps.fire.services import FireAlertService

logger = logging.getLogger(__name__)


class FireAlertViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints alerte feu — lecture publique, refresh admin only.
    """
    serializer_class   = FireAlertSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = FireAlert.objects.filter(is_active=True).select_related('parcel', 'parcel__owner')

        # Filtres optionnels via query params
        severity  = self.request.query_params.get('severity')
        parcel_id = self.request.query_params.get('parcel_id')
        days      = self.request.query_params.get('days')        # ex: ?days=7
        lat_min   = self.request.query_params.get('lat_min')
        lat_max   = self.request.query_params.get('lat_max')
        lon_min   = self.request.query_params.get('lon_min')
        lon_max   = self.request.query_params.get('lon_max')

        if severity:
            qs = qs.filter(severity=severity)
        if parcel_id:
            qs = qs.filter(parcel__uuid=parcel_id)
        if days:
            try:
                since = date.today() - timedelta(days=int(days))
                qs = qs.filter(acq_date__gte=since)
            except ValueError:
                pass
        if lat_min:
            qs = qs.filter(latitude__gte=float(lat_min))
        if lat_max:
            qs = qs.filter(latitude__lte=float(lat_max))
        if lon_min:
            qs = qs.filter(longitude__gte=float(lon_min))
        if lon_max:
            qs = qs.filter(longitude__lte=float(lon_max))

        return qs.order_by('-acq_date', '-brightness')

    # ── GET /api/fire/alerts/summary/ ─────────────────────────────────────────

    @swagger_auto_schema(
        operation_summary="Résumé statistique des alertes feu actives",
        tags=['🔥 Alertes Feu'],
        responses={200: FireAlertSummarySerializer()},
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def summary(self, request):
        qs = FireAlert.objects.filter(is_active=True)

        recent = qs.order_by('-acq_date', '-brightness')[:10]
        last_alert = qs.order_by('-acq_date').values_list('acq_date', flat=True).first()

        data = {
            'total_active':          qs.count(),
            'critical_count':        qs.filter(severity='CRITICAL').count(),
            'high_count':            qs.filter(severity='HIGH').count(),
            'medium_count':          qs.filter(severity='MEDIUM').count(),
            'parcels_at_risk_count': qs.filter(parcel__isnull=False).values('parcel').distinct().count(),
            'last_update':           last_alert or date.today(),
            'recent_alerts':         FireAlertSerializer(recent, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    # ── GET /api/fire/alerts/my_parcels/ ─────────────────────────────────────

    @swagger_auto_schema(
        operation_summary="Alertes feu pour mes parcelles",
        tags=['🔥 Alertes Feu'],
        manual_parameters=[
            openapi.Parameter('days', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Nombre de jours en arrière (défaut: 7)'),
        ],
        responses={200: FireAlertSerializer(many=True)},
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_parcels(self, request):
        days = int(request.query_params.get('days', 7))
        since = date.today() - timedelta(days=days)

        qs = FireAlert.objects.filter(
            is_active=True,
            parcel__owner=request.user,
            acq_date__gte=since,
        ).select_related('parcel').order_by('-acq_date', '-brightness')

        serializer = FireAlertSerializer(qs, many=True)
        return Response({
            'count':  qs.count(),
            'days':   days,
            'alerts': serializer.data,
        }, status=status.HTTP_200_OK)

    # ── POST /api/fire/alerts/refresh/ ────────────────────────────────────────

    @swagger_auto_schema(
        operation_summary="Déclencher la mise à jour FIRMS (Admin uniquement)",
        tags=['🔥 Alertes Feu'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'radius_km': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Rayon en km autour des parcelles (défaut: 15)',
                    default=15,
                )
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success':                      openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'total_hotspots_madagascar':    openapi.Schema(type=openapi.TYPE_INTEGER),
                    'near_parcel_count':            openapi.Schema(type=openapi.TYPE_INTEGER),
                    'alerts_created':               openapi.Schema(type=openapi.TYPE_INTEGER),
                    'alerts_skipped_duplicates':    openapi.Schema(type=openapi.TYPE_INTEGER),
                    'notifications_sent':           openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        },
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def refresh(self, request):
        radius_km = float(request.data.get('radius_km', 15.0))
        try:
            service = FireAlertService()
            report  = service.run(radius_km=radius_km)
            return Response({'success': True, **report}, status=status.HTTP_200_OK)
        except Exception as exc:
            logger.error(f"FireAlertService.run() error: {exc}", exc_info=True)
            return Response(
                {'success': False, 'error': str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # ── POST /api/fire/alerts/{uuid}/dismiss/ ────────────────────────────────

    @swagger_auto_schema(
        operation_summary="Désactiver (ignorer) une alerte feu",
        tags=['🔥 Alertes Feu'],
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}
        )},
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def dismiss(self, request, pk=None):
        alert = self.get_object()
        # Seul le propriétaire de la parcelle ou un admin peut ignorer
        if alert.parcel and alert.parcel.owner != request.user and not request.user.is_staff:
            return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
        alert.is_active = False
        alert.save(update_fields=['is_active'])
        return Response(
            {'message': f'Alerte {alert.uuid} désactivée'},
            status=status.HTTP_200_OK,
        )
