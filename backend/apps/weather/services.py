"""
apps/weather/services.py
------------------------
4 services déplacés depuis SmartSaha/services/.

WeatherDataService    → traitement données météo brutes
AgriculturalAnalyzer  → analyse agricole + détection risques
WeatherDataCollector  → collecte WeatherAPI + sauvegarde
AlertService          → génération statique d'alertes par catégorie
"""
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from django.conf import settings
from django.utils import timezone
import requests as http_requests  # ← alias pour éviter conflit avec DRF

from apps.weather.models import WeatherData, AgriculturalAlert


class WeatherDataService:
    """Traitement et stockage des données météo brutes."""

    def process_weather_data(self, raw_data: Dict, parcel) -> Dict:
        metadata = self._extract_metadata(raw_data)
        weather_data = self._create_weather_data(parcel, raw_data, metadata)
        alerts_count = self._generate_agricultural_alerts(weather_data)
        return {
            'weather_data': weather_data,
            'alerts_count': alerts_count,
            'risk_level': weather_data.risk_level,
        }

    def _extract_metadata(self, raw_data: Dict) -> Dict:
        location = raw_data.get('location', {})
        current  = raw_data.get('current', {})
        forecast_days = raw_data.get('forecast', {}).get('forecastday', [])

        # ✅ FIX : last_updated = "2026-03-13 09:15" (datetime string)
        # → on parse et on tronque à la date seule pour le DateField
        last_updated_raw = current.get('last_updated', '')
        try:
            start = datetime.strptime(last_updated_raw, '%Y-%m-%d %H:%M').date()
        except (ValueError, TypeError):
            start = datetime.now().date()

        return {
            'location_name': location.get('name', ''),
            'data_type': 'FORECAST' if forecast_days else 'CURRENT',
            'start': start,
            'end': self._calculate_end_date(raw_data),
        }

    def _calculate_end_date(self, raw_data: Dict):
        forecast_days = raw_data.get('forecast', {}).get('forecastday', [])
        if forecast_days:
            # forecast_days[-1]['date'] est déjà au format "YYYY-MM-DD" ✅
            return forecast_days[-1]['date']
        return datetime.now().date()

    def _create_weather_data(self, parcel, raw_data, metadata) -> WeatherData:
        return WeatherData.objects.create(
            parcel=parcel,
            data=raw_data,
            start=metadata['start'],
            end=metadata['end'],
            data_type=metadata['data_type'],
            location_name=metadata['location_name'],
        )

    def _generate_agricultural_alerts(self, weather_data: WeatherData) -> int:
        alerts_data = weather_data.agricultural_alerts  # property héritée
        created = 0
        for alert in alerts_data:
            AgriculturalAlert.objects.get_or_create(
                weather_data=weather_data,
                alert_type=alert['type'],
                alert_date=alert['date'],
                defaults={
                    'message':        alert['message'],
                    'recommendation': alert.get('action', ''),
                    'severity':       alert['severity'],
                    'is_active':      True,
                },
            )
            created += 1
        return created


class AgriculturalAnalyzer:
    """Analyse agricole enrichie depuis les données météo."""

    def analyze_weather_data(self, weather_data: WeatherData) -> Dict:
        return {
            'optimal_planting_days':     weather_data.optimal_planting_days,
            'irrigation_recommendation': weather_data.irrigation_recommendation,
            'overall_risk':             self._assess_overall_risk(weather_data),
            'crop_advice':              weather_data.crop_specific_advice,
        }

    def analyze_risks(self, weather_data: Dict) -> List[Dict]:
        """Analyse les risques jour par jour depuis les données JSON brutes."""
        risks = []
        forecast_days = weather_data.get('forecast', {}).get('forecastday', [])
        for day in forecast_days:
            risks.extend(self._analyze_day_risks(day['day']))
        return risks

    def _analyze_day_risks(self, day_data: Dict) -> List[Dict]:
        risks = []
        if day_data.get('totalprecip_mm', 0) > 20:
            risks.append({'type': 'HEAVY_RAIN', 'severity': 'HIGH'})
        if day_data.get('mintemp_c', 20) < 5:
            risks.append({'type': 'FROST_RISK', 'severity': 'HIGH'})
        if day_data.get('avghumidity', 0) > 85:
            risks.append({'type': 'HIGH_HUMIDITY', 'severity': 'MEDIUM'})
        if day_data.get('maxwind_kph', 0) > 30:
            risks.append({'type': 'STRONG_WIND', 'severity': 'MEDIUM'})
        return risks

    def _assess_overall_risk(self, weather_data: WeatherData) -> str:
        alerts = weather_data.agricultural_alerts
        high = sum(1 for a in alerts if a['severity'] == 'HIGH')
        if high >= 2: return 'HIGH'
        if high >= 1: return 'MEDIUM'
        return 'LOW'


class WeatherAPIClient:
    """Client HTTP vers Open-Meteo API (sans clé), adapté au format existant."""
    def __init__(self):
        self.base_url = 'https://api.open-meteo.com/v1/forecast'

    def get_forecast(self, latitude: float, longitude: float, days: int = 3) -> Optional[Dict]:
        try:
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,surface_pressure,wind_speed_10m',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max',
                'timezone': 'auto',
                'forecast_days': days
            }
            resp = http_requests.get(self.base_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            # Adapt Open-Meteo format -> WeatherAPI format
            current = data.get('current', {})
            daily = data.get('daily', {})

            forecastdays = []
            for i in range(len(daily.get('time', []))):
                forecastdays.append({
                    'date': daily['time'][i],
                    'day': {
                        'maxtemp_c': daily.get('temperature_2m_max', [])[i] if i < len(daily.get('temperature_2m_max', [])) else 0,
                        'mintemp_c': daily.get('temperature_2m_min', [])[i] if i < len(daily.get('temperature_2m_min', [])) else 0,
                        'avgtemp_c': ((daily.get('temperature_2m_max', [])[i] or 0) + (daily.get('temperature_2m_min', [])[i] or 0)) / 2,
                        'totalprecip_mm': daily.get('precipitation_sum', [])[i] if i < len(daily.get('precipitation_sum', [])) else 0,
                        'daily_chance_of_rain': daily.get('precipitation_probability_max', [])[i] if i < len(daily.get('precipitation_probability_max', [])) else 0,
                        'condition': { 'text': self._wmo_code_to_text(daily.get('weather_code', [])[i] if i < len(daily.get('weather_code', [])) else 0) },
                        'uv': 5.0, # Not fetched but required by shape
                        'maxwind_kph': daily.get('wind_speed_10m_max', [])[i] if i < len(daily.get('wind_speed_10m_max', [])) else 0,
                        'avghumidity': current.get('relative_humidity_2m', 70),
                        'daily_will_it_rain': 1 if (daily.get('precipitation_sum', [])[i] or 0) > 0 else 0,
                        'daily_will_it_snow': 0
                    }
                })

            adapted = {
                'location': { 'name': f"{latitude:.2f}, {longitude:.2f}" },
                'current': {
                    'last_updated': current.get('time', '').replace('T', ' '),
                    'temp_c': current.get('temperature_2m', 0),
                    'humidity': current.get('relative_humidity_2m', 0),
                    'precip_mm': current.get('precipitation', 0),
                    'condition': { 'text': self._wmo_code_to_text(current.get('weather_code', 0)) },
                    'wind_kph': current.get('wind_speed_10m', 0),
                    'feelslike_c': current.get('apparent_temperature', 0),
                    'pressure_mb': current.get('surface_pressure', 0),
                    'vis_km': 10.0,
                    'uv': 5.0
                },
                'forecast': {
                    'forecastday': forecastdays
                }
            }
            return adapted
        except Exception as e:
            print(f"Open-Meteo API Error: {e}")
            return None

    def _wmo_code_to_text(self, code: int) -> str:
        # WMO Weather interpretation codes (ww)
        mapping = {
            0: 'Clair', 1: 'Peu nuageux', 2: 'Partiellement nuageux', 3: 'Couvert',
            45: 'Brouillard', 48: 'Brouillard givrant',
            51: 'Bruine légère', 53: 'Bruine modérée', 55: 'Bruine dense',
            61: 'Pluie faible', 63: 'Pluie modérée', 65: 'Pluie forte',
            71: 'Neige faible', 73: 'Neige modérée', 75: 'Neige forte',
            80: 'Averses légères', 81: 'Averses modérées', 82: 'Averses violentes',
            95: 'Orage', 96: 'Orage avec grêle légère', 99: 'Orage avec grêle forte',
        }
        return mapping.get(code, 'Inconnu')


class WeatherDataCollector:
    """Collecte et persiste les données météo pour une parcelle."""
    def __init__(self):
        self.api_client   = WeatherAPIClient()
        self.data_service = WeatherDataService()

    def _extract_center_from_points(self, points_data) -> Tuple[Optional[float], Optional[float]]:
        if not points_data:
            return None, None
        if isinstance(points_data, list) and points_data:
            first = points_data[0]
            if isinstance(first, dict):
                return first.get('lat'), first.get('lng')
        return None, None

    def collect_and_save_weather_data(self, parcel, forecast_days: int = 3) -> Dict:
        lat, lon = self._extract_center_from_points(parcel.points)
        if lat is None or lon is None:
            return {'success': False, 'error': 'Aucun point GPS défini sur la parcelle'}
        raw_data = self.api_client.get_forecast(lat, lon, days=forecast_days)
        if not raw_data:
            return {'success': False, 'error': 'Erreur appel WeatherAPI'}
        result = self.data_service.process_weather_data(raw_data, parcel)
        return {
            'success':           True,
            'weather_data':      result['weather_data'],
            'alerts_generated':  result['alerts_count'],
            'risk_level':        result['risk_level'],
            'coordinates_used':  {'lat': lat, 'lon': lon},
        }


class AlertService:
    """Service statique de génération d'alertes agronomiques."""

    @staticmethod
    def generate_task_alerts(parcel) -> List[Dict]:
        """Alertes tâches en retard ou urgentes."""
        alerts = []
        # ✅ Utilise datetime complet pour éviter les comparaisons datetime vs date
        now      = timezone.now()
        in_3days = now + timedelta(days=3)
        try:
            from apps.tasks.models import Task
            overdue = Task.objects.filter(
                parcelCrop__parcel=parcel,
                completed_at__isnull=True,
                due_date__lt=now,           # datetime vs datetime ✅
            )
            for task in overdue:
                due = task.due_date if hasattr(task.due_date, 'hour') else \
                      datetime.combine(task.due_date, datetime.min.time())
                days_late = (now - timezone.make_aware(due) if timezone.is_naive(due) else now - due).days
                alerts.append({
                    'type': '⏰ TÂCHE EN RETARD',
                    'message': f"{task.name} — {days_late} jour(s) de retard",
                    'severity': 'HIGH' if days_late > 7 else 'MEDIUM',
                    'action': 'Exécuter cette tâche dès que possible',
                    'date': task.due_date.isoformat() if hasattr(task.due_date, 'isoformat') else str(task.due_date),
                })
            urgent = Task.objects.filter(
                parcelCrop__parcel=parcel,
                completed_at__isnull=True,
                due_date__range=[now, in_3days],  # datetime vs datetime ✅
            )
            for task in urgent:
                alerts.append({
                    'type': '🔔 TÂCHE URGENTE',
                    'message': f"{task.name} — Échéance le {task.due_date}",
                    'severity': 'MEDIUM',
                    'action': 'Planifier cette tâche rapidement',
                    'date': task.due_date.isoformat() if hasattr(task.due_date, 'isoformat') else str(task.due_date),
                })
        except Exception:
            pass  # dégradé si apps.tasks pas encore disponible
        return alerts

    @staticmethod
    def generate_weather_alerts(parcel, weather_data) -> List[Dict]:
        """Délègue à WeatherData.agricultural_alerts si possible."""
        try:
            latest = WeatherData.get_latest_for_parcel(parcel)
            return latest.agricultural_alerts
        except Exception:
            return []

    @staticmethod
    def generate_soil_alerts(parcel, soil_data) -> List[Dict]:
        """Alertes sol — pH et azote."""
        return _soil_alerts_from_data(soil_data)

    @staticmethod
    def generate_all_alerts(parcel, weather_data=None, soil_data=None, soil_moisture_data=None) -> List[Dict]:
        all_alerts = []
        all_alerts.extend(AlertService.generate_weather_alerts(parcel, weather_data or {}))
        all_alerts.extend(AlertService.generate_soil_alerts(parcel, soil_data or {}))
        all_alerts.extend(AlertService.generate_task_alerts(parcel))
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        all_alerts.sort(key=lambda x: severity_order.get(x.get('severity', 'LOW'), 4))
        return all_alerts

    @staticmethod
    def get_alert_statistics(alerts: List[Dict]) -> Dict:
        return {
            'total':    len(alerts),
            'critical': len([a for a in alerts if a['severity'] == 'CRITICAL']),
            'high':     len([a for a in alerts if a['severity'] == 'HIGH']),
            'medium':   len([a for a in alerts if a['severity'] == 'MEDIUM']),
            'low':      len([a for a in alerts if a['severity'] == 'LOW']),
        }


def _soil_alerts_from_data(soil_data) -> List[Dict]:
    """Fonction utilitaire — analyse sol pour AlertService.generate_soil_alerts."""
    alerts = []
    if not soil_data:
        return alerts
    today = datetime.now().date().isoformat()
    soil_dict = soil_data if isinstance(soil_data, dict) else {}
    ph = soil_dict.get('phh2o', {}).get('mean') if isinstance(soil_dict.get('phh2o'), dict) else None
    if ph and ph < 5.5:
        alerts.append({
            'type': '🧪 pH ACIDE',
            'message': f"pH sol acide ({ph})",
            'severity': 'MEDIUM',
            'action': 'Appliquer chaux agricole',
            'date': today,
        })
    nitrogen = soil_dict.get('nitrogen', {}).get('mean') if isinstance(soil_dict.get('nitrogen'), dict) else None
    if nitrogen and nitrogen < 1.0:
        alerts.append({
            'type': '🌱 CARENCE AZOTE',
            'message': f"Azote faible ({nitrogen} g/kg)",
            'severity': 'HIGH',
            'action': 'Appliquer engrais azoté',
            'date': today,
        })
    return alerts