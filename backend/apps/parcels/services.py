"""
apps/parcels/services.py
------------------------
Services métier pour les parcelles.
ParcelService     → opérations simples sur une parcelle
ParcelDataService → agrégation données sol + météo + cultures + tâches
"""
import requests
from django.utils import timezone

from apps.parcels.models import Parcel, ParcelPoint
from apps.weather.models import WeatherData, SoilData
from apps.yields.models import YieldRecord
from apps.tasks.models import Task
from apps.weather.services import WeatherDataCollector, AgriculturalAnalyzer


class ParcelService:
    """Opérations simples sur une parcelle."""
    def __init__(self, parcel: Parcel):
        self.parcel = parcel

    def add_points_bulk(self, points_list: list) -> Parcel:
        """Ajoute une liste de points GPS [{lat, lng}] à la parcelle."""
        for idx, p in enumerate(points_list):
            self.parcel.add_point(p['lat'], p['lng'], idx)
        return self.parcel


class ParcelDataService:
    """
    Agrégation de toutes les données d'une parcelle.
    Orchestre les appels SoilGrids, WeatherAPI et les requêtes BDD.
    """

    @staticmethod
    def get_first_point(parcel: Parcel) -> dict:
        if not parcel.points or len(parcel.points) == 0:
            raise ValueError("La parcelle n'a pas de points GPS")
        return parcel.points[0]

    @staticmethod
    def fetch_soil(parcel: Parcel, force_refresh=False):
        """Récupère les données sol via SoilGrids avec cache 30 jours."""
        if not force_refresh:
            recent = SoilData.objects.filter(
                parcel=parcel,
                created_at__gte=timezone.now() - timezone.timedelta(days=30)
            ).order_by('-created_at').first()
            if recent and ParcelDataService.has_valid_soil_data(recent):
                return recent

        point = ParcelDataService.get_first_point(parcel)
        lat, lon = point['lat'], point['lng']
        url = (
            f"https://rest.isric.org/soilgrids/v2.0/properties/query?"
            f"lon={lon}&lat={lat}&property=phh2o&property=soc&property=nitrogen"
            f"&property=sand&property=clay&property=silt&depth=0-5cm&value=mean"
        )
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if ParcelDataService.is_soil_data_valid(data):
                    return SoilData.objects.create(parcel=parcel, data=data)
                return ParcelDataService.create_default_soil_data(parcel, lat, lon)
            return ParcelDataService.get_fallback_soil_data(parcel)
        except Exception:
            return ParcelDataService.get_fallback_soil_data(parcel)

    @staticmethod
    def has_valid_soil_data(soil_obj) -> bool:
        if not soil_obj or not soil_obj.data:
            return False
        layers = soil_obj.data.get('properties', {}).get('layers', [])
        return any(
            d.get('values', {}).get('mean') is not None
            for layer in layers for d in layer.get('depths', [])
        )

    @staticmethod
    def is_soil_data_valid(data) -> bool:
        if not data:
            return False
        layers = data.get('properties', {}).get('layers', [])
        valid = sum(
            1 for layer in layers
            if any(d.get('values', {}).get('mean') is not None for d in layer.get('depths', []))
        )
        return valid >= len(layers) * 0.5

    @staticmethod
    def create_default_soil_data(parcel, lat, lon):
        """Données sol par défaut pour Madagascar (sols tropicaux)."""
        default = {
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
            'properties': {'layers': [
                {'name': 'clay',     'depths': [{'label': '0-5cm', 'values': {'mean': 25.0}}]},
                {'name': 'nitrogen', 'depths': [{'label': '0-5cm', 'values': {'mean': 1.2}}]},
                {'name': 'phh2o',    'depths': [{'label': '0-5cm', 'values': {'mean': 6.5}}]},
                {'name': 'sand',     'depths': [{'label': '0-5cm', 'values': {'mean': 40.0}}]},
                {'name': 'silt',     'depths': [{'label': '0-5cm', 'values': {'mean': 35.0}}]},
                {'name': 'soc',      'depths': [{'label': '0-5cm', 'values': {'mean': 2.0}}]},
            ]},
            'metadata': {'source': 'default_values', 'region': 'Madagascar'}
        }
        return SoilData.objects.create(parcel=parcel, data=default)

    @staticmethod
    def get_fallback_soil_data(parcel):
        existing = SoilData.objects.filter(parcel=parcel).order_by('-created_at').first()
        if existing:
            return existing
        point = ParcelDataService.get_first_point(parcel)
        return ParcelDataService.create_default_soil_data(parcel, point['lat'], point['lng'])

    @staticmethod
    def refresh_soil_data(parcel: Parcel):
        return ParcelDataService.fetch_soil(parcel, force_refresh=True)

    @staticmethod
    def fetch_weather(parcel: Parcel, required_days=3):
        """Récupère les données météo avec cache 24h."""
        recent = WeatherData.objects.filter(
            parcel=parcel,
            created_at__gte=timezone.now() - timezone.timedelta(hours=24)
        ).order_by('-created_at').first()
        if recent and ParcelDataService.has_enough_forecast_days(recent, required_days):
            return recent
        collector = WeatherDataCollector()
        result = collector.collect_and_save_weather_data(parcel, forecast_days=required_days)
        if result['success']:
            return result['weather_data']
        return recent

    @staticmethod
    def has_enough_forecast_days(weather_data, required_days=3) -> bool:
        if not weather_data or not weather_data.data:
            return False
        return len(weather_data.data.get('forecast', {}).get('forecastday', [])) >= required_days

    @staticmethod
    def get_complete_parcel_data(parcel_uuid: str) -> dict | None:
        """Agrège toutes les données d'une parcelle (sol + météo + cultures + tâches)."""
        try:
            parcel = Parcel.objects.get(uuid=parcel_uuid)
            return {
                'parcel':        {'uuid': str(parcel.uuid), 'name': parcel.parcel_name, 'points': parcel.points, 'created_at': parcel.created_at},
                'soil_data':     ParcelDataService.fetch_soil(parcel),
                'weather_data':  ParcelDataService.get_weather_analysis(parcel),
                'crops':         ParcelDataService.build_parcel_crops(parcel),
                'yield_records': ParcelDataService.build_yield_records(parcel),
                'tasks':         ParcelDataService.build_parcel_tasks(parcel),
                'tasks_summary': ParcelDataService.get_tasks_summary(parcel),
            }
        except Parcel.DoesNotExist:
            return None

    @staticmethod
    def get_weather_analysis(parcel: Parcel):
        weather_data = ParcelDataService.fetch_weather(parcel)
        if not weather_data:
            return None
        analyzer = AgriculturalAnalyzer()
        from apps.weather.services import AlertService
        return {
            'weather_data': weather_data,
            'analysis':     analyzer.analyze_weather_data(weather_data),
            'alerts':       AlertService.generate_all_alerts(parcel),
            'summary':      weather_data.get_weather_summary(),
        }

    @staticmethod
    def build_parcel_crops(parcel) -> list:
        return [
            {
                'parcel_crop_id': pc.id,
                'crop':          {'id': pc.crop.id, 'name': pc.crop.name},
                'planting_date': pc.planting_date,
                'harvest_date':  pc.harvest_date,
                'area':          pc.area,
                'status':        pc.status.name if pc.status else None,
            }
            for pc in parcel.parcel_crops.select_related('crop', 'status').all()
        ]

    @staticmethod
    def build_yield_records(parcel) -> list:
        # Optimisation : On récupère tous les records de rendement de la parcelle en UNE SEULE requête
        records = YieldRecord.objects.filter(parcelCrop__parcel=parcel).select_related('parcelCrop')
        
        # On regroupe par ParcelCrop ID pour faciliter l'accès si besoin, 
        # mais la structure demandée est une liste simple
        return [
            {
                'parcel_crop_id': yr.parcelCrop.id if yr.parcelCrop else None,
                'date':           yr.date,
                'yield':          yr.yield_amount,
                'notes':          yr.notes,
            }
            for yr in records
        ]

    @staticmethod
    def _safe_date(value):
        """Retourne une date pure (date) depuis un DateField ou DateTimeField."""
        if value is None:
            return None
        return value.date() if hasattr(value, 'date') and callable(value.date) else value

    @staticmethod
    def build_parcel_tasks(parcel) -> dict:
        tasks = (
            Task.objects
            .filter(parcelCrop__parcel=parcel)
            .select_related('parcelCrop', 'status', 'priority')
            .order_by('due_date')
        )
        return {
            'tasks': [
                {
                    'id':       t.id,
                    'name':     t.name,
                    # ✅ Normalise en date pure quelle que soit le type du champ
                    'due_date': ParcelDataService._safe_date(t.due_date),
                    'status':   t.status.name if t.status else None,
                    'priority': t.priority.name if t.priority else None,
                }
                for t in tasks
            ],
            'statistics': {
                'total':     tasks.count(),
                'completed': tasks.filter(completed_at__isnull=False).count(),
                'pending':   tasks.filter(completed_at__isnull=True).count(),
            },
        }

    @staticmethod
    def get_tasks_summary(parcel) -> dict:
        tasks = Task.objects.filter(parcelCrop__parcel=parcel)
        now_date  = timezone.now().date()                           # date ✅
        in_3_days = now_date + timezone.timedelta(days=3)          # date ✅

        urgent = tasks.filter(
            completed_at__isnull=True,
            due_date__lte=in_3_days,                               # date vs date ✅
        ).order_by('due_date')[:5]

        return {
            'urgent_tasks': [
                {
                    'id':         t.id,
                    'name':       t.name,
                    'due_date':   ParcelDataService._safe_date(t.due_date),
                    # ✅ _safe_date retourne une date pure → comparaison date vs date
                    'is_overdue': ParcelDataService._safe_date(t.due_date) < now_date,
                }
                for t in urgent
            ],
            'total_pending': tasks.filter(completed_at__isnull=True).count(),
        }

    @staticmethod
    def serialize_soil_data(soil_obj) -> dict | None:
        if not soil_obj or not soil_obj.data:
            return None
        return {
            'data':     soil_obj.data,
            'metadata': {
                'created_at': soil_obj.created_at.isoformat(),
                'source':     soil_obj.data.get('metadata', {}).get('source', 'soilgrids_api'),
            },
        }

    @staticmethod
    def serialize_weather_data(weather_dict) -> dict | None:
        if not weather_dict:
            return None
        weather_obj = weather_dict.get('weather_data')
        return {
            # ✅ On ne retourne que le JSON brut de l'API, pas l'objet Django
            'data':     weather_obj.data if weather_obj else None,
            'analysis': weather_dict.get('analysis'),
            'alerts':   weather_dict.get('alerts'),
            'summary':  weather_dict.get('summary'),
            'metadata': {
                'location_name': weather_obj.location_name if weather_obj else None,
                'risk_level':    weather_obj.risk_level    if weather_obj else None,
                'start':         weather_obj.start.isoformat() if weather_obj and weather_obj.start else None,
                'end':           weather_obj.end.isoformat()   if weather_obj and weather_obj.end   else None,
            },
        }