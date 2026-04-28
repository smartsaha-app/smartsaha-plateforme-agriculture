from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.core.mixins import CacheInvalidationMixin
from apps.parcels.models import Parcel
from apps.weather.models import WeatherData, AgriculturalAlert, Alert
from apps.weather.serializers import WeatherDataSerializer, AgriculturalAlertSerializer, AlertSerializer
from apps.weather.services import WeatherDataService, AgriculturalAnalyzer, WeatherDataCollector, AlertService


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
class WeatherDataViewSet(CacheInvalidationMixin, viewsets.ModelViewSet):
    serializer_class = WeatherDataSerializer
    queryset = WeatherData.objects.all()
    cache_prefix = 'weather_data'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weather_service = WeatherDataService()
        self.analyzer = AgriculturalAnalyzer()

    @swagger_auto_schema(
        operation_summary="Traiter les données météo",
        tags=['Météo & Alertes'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['post'])
    def process_weather_data(self, request):
        try:
            parcel = get_object_or_404(Parcel, uuid=request.data.get('parcel_id'))
            result = self.weather_service.process_weather_data(request.data.get('weather_data'), parcel)
            return Response({'success': True, 'weather_data_id': result['weather_data'].id,
                              'alerts_generated': result['alerts_count'], 'risk_level': result['risk_level']})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Analyse agricole",
        tags=['Météo & Alertes'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=True, methods=['get'])
    def agricultural_analysis(self, request, pk=None):
        weather_data = self.get_object()
        return Response({'success': True, 'analysis': self.analyzer.analyze_weather_data(weather_data)})

    @swagger_auto_schema(
        operation_summary="Météo actuelle de la parcelle",
        tags=['Météo & Alertes'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['get'])
    def parcel_weather(self, request):
        parcel_id = request.query_params.get('parcel_id')
        if not parcel_id:
            return Response({'error': 'parcel_id requis'}, status=status.HTTP_400_BAD_REQUEST)
        latest = WeatherData.objects.filter(parcel_id=parcel_id).order_by('-created_at').first()
        if not latest:
            return Response({'success': False, 'message': 'Aucune donnée météo'})
        return Response({'success': True, 'weather_data': self.get_serializer(latest).data})


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
class AgriculturalAlertViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AgriculturalAlertSerializer

    def get_queryset(self):
        qs = AgriculturalAlert.objects.filter(is_active=True)
        parcel_id = self.request.query_params.get('parcel_id')
        severity  = self.request.query_params.get('severity')
        if parcel_id: qs = qs.filter(weather_data__parcel_id=parcel_id)
        if severity:  qs = qs.filter(severity=severity)
        return qs.order_by('-alert_date')

    @action(detail=False, methods=['get'])
    def active_alerts(self, request):
        qs = self.get_queryset()
        return Response({
            'total_alerts':         qs.count(),
            'high_priority_count':  qs.filter(severity='HIGH').count(),
            'medium_priority_count':qs.filter(severity='MEDIUM').count(),
            'recent_alerts':        AgriculturalAlertSerializer(qs[:10], many=True).data,
        })


class WeatherCollectionViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weather_collector = WeatherDataCollector()

    @action(detail=False, methods=['post'])
    def collect_parcel_weather(self, request):
        parcel_uuid = request.data.get('parcel_uuid')
        if not parcel_uuid:
            return Response({'error': 'parcel_uuid requis'}, status=status.HTTP_400_BAD_REQUEST)
        parcel = get_object_or_404(Parcel, uuid=parcel_uuid)
        if not parcel.points:
            return Response({'error': 'Points GPS non définis'}, status=status.HTTP_400_BAD_REQUEST)
        result = self.weather_collector.collect_and_save_weather_data(parcel)
        st = status.HTTP_200_OK if result['success'] else status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(result, status=st)

    @action(detail=False, methods=['post'])
    def collect_all_parcels_weather(self, request):
        parcels = Parcel.objects.filter(points__isnull=False).exclude(points=[])
        results, total_ok = [], 0
        for parcel in parcels:
            r = self.weather_collector.collect_and_save_weather_data(parcel)
            results.append({'parcel_uuid': str(parcel.uuid), 'parcel_name': parcel.parcel_name, **r})
            if r['success']: total_ok += 1
        return Response({'success': True, 'message': f'{total_ok}/{len(parcels)} réussites', 'results': results})


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Météo & Alertes']))
class AlertViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AlertSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Alert.objects.none()
        return Alert.objects.filter(parcel__owner=self.request.user).select_related('parcel').order_by('-created_at')

    @action(detail=False, methods=['get'])
    def generate_parcel_alerts(self, request):
        parcel_uuid = request.query_params.get('parcel_uuid')
        if not parcel_uuid:
            return Response({'error': 'parcel_uuid requis'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            parcel = Parcel.objects.get(uuid=parcel_uuid, owner=request.user)
            all_alerts = AlertService.generate_all_alerts(parcel)
            saved = 0
            for a in all_alerts:
                _, created = Alert.objects.get_or_create(
                    parcel=parcel, type=a['type'], severity=a['severity'], alert_date=a['date'],
                    defaults={'message': a['message'], 'action': a.get('action', ''), 'is_read': False})
                if created: saved += 1
            stats = AlertService.get_alert_statistics(all_alerts)
            return Response({**stats, 'alerts': all_alerts, 'saved_count': saved,
                              'parcel_uuid': str(parcel.uuid), 'generated_at': timezone.now().isoformat()})
        except Parcel.DoesNotExist:
            return Response({'error': 'Parcelle non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        alert = self.get_object()
        alert.is_read = True
        alert.save()
        return Response({'message': 'Alerte marquée comme lue', 'is_read': True})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        updated = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'updated_count': updated})


@swagger_auto_schema(tags=['Météo & Alertes'])
class SoilDataView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Données du sol (ISRIC)",
        tags=['Météo & Alertes'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    def get(self, request):
        import requests as req
        lon = request.query_params.get('lon')
        lat = request.query_params.get('lat')
        if not (lon and lat):
            return Response({'error': 'lon et lat requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        cache_key = f"soil_data_{lat}_{lon}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        try:
            url = (
                f"https://rest.isric.org/soilgrids/v2.0/properties/query?"
                f"lon={lon}&lat={lat}"
                "&property=phh2o&property=soc&property=nitrogen"
                "&property=sand&property=clay&property=silt"
                "&depth=0-5cm&value=mean"
            )
            resp = req.get(url, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            # Cache de 7 jours pour les données de sol (changent très peu)
            cache.set(cache_key, data, timeout=60*60*24*7)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(tags=['Météo & Alertes'])
class ClimateDataView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        operation_summary="Données climatiques historique (NASA)",
        tags=['Météo & Alertes'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    def get(self, request):
        import requests as req
        lon   = request.query_params.get('lon')
        lat   = request.query_params.get('lat')
        start = request.query_params.get('start')
        end   = request.query_params.get('end')
        if not all([lon, lat, start, end]):
            return Response({'error': 'lon, lat, start, end requis'}, status=status.HTTP_400_BAD_REQUEST)
        
        cache_key = f"climate_data_{lat}_{lon}_{start}_{end}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        try:
            url = (
                f"https://power.larc.nasa.gov/api/temporal/daily/point?"
                "parameters=T2M,T2MDEW,T2MWET,TS,T2M_RANGE,T2M_MAX,T2M_MIN,"
                "PRECTOTCORR,EVLAND,GWETPROF"
                f"&community=RE&longitude={lon}&latitude={lat}"
                f"&start={start}&end={end}&format=JSON"
            )
            resp = req.get(url, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            # Cache de 24h pour les données climatiques historiques/actuelles
            cache.set(cache_key, data, timeout=60*60*24)
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)