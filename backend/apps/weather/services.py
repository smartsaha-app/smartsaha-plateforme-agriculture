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
        # (connect_timeout, read_timeout) — connexion rapide, lecture plus généreuse
        self.timeout = (5, 30)
        self.max_retries = 2

    def get_forecast(self, latitude: float, longitude: float, days: int = 31) -> Optional[Dict]:
        import datetime as dt

        api_days = min(days, 16)
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,surface_pressure,wind_speed_10m,uv_index',
            # relative_humidity_2m_max ajouté → humidité réelle par jour de prévision
            'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,relative_humidity_2m_max,uv_index_max',
            'timezone': 'auto',
            'forecast_days': api_days,
        }

        # ── Appel HTTP avec retry ──────────────────────────────────────────────
        raw = None
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = http_requests.get(self.base_url, params=params, timeout=self.timeout)
                resp.raise_for_status()
                raw = resp.json()
                break
            except Exception as exc:
                last_error = exc
                print(f"Open-Meteo tentative {attempt}/{self.max_retries} échouée : {exc}")

        if raw is None:
            print(f"Open-Meteo indisponible après {self.max_retries} tentatives : {last_error}")
            return None

        # ── Adaptation format Open-Meteo → WeatherAPI ─────────────────────────
        try:
            current = raw.get('current', {}) or {}
            daily   = raw.get('daily',   {}) or {}

            time_list = daily.get('time', []) or []
            daily_len = len(time_list)

            if daily_len > 0:
                base_date = dt.datetime.strptime(time_list[0], '%Y-%m-%d').date()
            else:
                base_date = dt.date.today()

            def _daily_val(key, idx, default=0):
                arr = daily.get(key) or []
                return arr[idx] if idx < len(arr) else default

            fetched_at = dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M')

            forecastdays = []
            for i in range(days):
                idx          = i if i < daily_len else (i % daily_len) if daily_len else 0
                current_date = (base_date + dt.timedelta(days=i)).isoformat()
                max_t = _daily_val('temperature_2m_max', idx) or 0
                min_t = _daily_val('temperature_2m_min', idx) or 0
                # Humidité réelle par jour (relative_humidity_2m_max demandé dans params)
                # Si non disponible (ancien cache), fallback sur current
                daily_humidity = (_daily_val('relative_humidity_2m_max', idx)
                                  or current.get('relative_humidity_2m') or 70)
                daily_uv = _daily_val('uv_index_max', idx) or current.get('uv_index') or 5.0
                forecastdays.append({
                    'date': current_date,
                    'day': {
                        'maxtemp_c':            max_t,
                        'mintemp_c':            min_t,
                        'avgtemp_c':            (max_t + min_t) / 2,
                        'totalprecip_mm':       _daily_val('precipitation_sum',             idx) or 0,
                        'daily_chance_of_rain': _daily_val('precipitation_probability_max', idx) or 0,
                        'maxwind_kph':          _daily_val('wind_speed_10m_max',            idx) or 0,
                        'avghumidity':          daily_humidity,
                        'daily_will_it_rain':   1 if (_daily_val('precipitation_sum', idx) or 0) > 0 else 0,
                        'daily_will_it_snow':   0,
                        'uv':                   daily_uv,
                        'condition': {
                            'text': self._wmo_code_to_text(_daily_val('weather_code', idx) or 0)
                        },
                    },
                })

            return {
                'location':   {'name': f"{latitude:.2f}, {longitude:.2f}"},
                'fetched_at': fetched_at,   # horodatage UTC du fetch réel
                'current': {
                    'last_updated': fetched_at,
                    'temp_c':       current.get('temperature_2m')       or 0,
                    'humidity':     current.get('relative_humidity_2m') or 0,
                    'precip_mm':    current.get('precipitation')        or 0,
                    'wind_kph':     current.get('wind_speed_10m')       or 0,
                    'feelslike_c':  current.get('apparent_temperature') or 0,
                    'pressure_mb':  current.get('surface_pressure')     or 0,
                    'uv_index':     current.get('uv_index')             or 0,
                    'vis_km':       10.0,
                    'condition': {
                        'text': self._wmo_code_to_text(current.get('weather_code') or 0)
                    },
                },
                'forecast': {'forecastday': forecastdays},
            }
        except Exception as exc:
            print(f"Open-Meteo format error : {exc}")
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

    def collect_and_save_weather_data(self, parcel, forecast_days: int = 31) -> Dict:
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
    def generate_fire_alerts(parcel) -> List[Dict]:
        """Alertes feu FIRMS NASA pour la parcelle (depuis apps.fire)."""
        try:
            from apps.fire.services import FireAlertService
            return FireAlertService.generate_fire_alerts_for_parcel(parcel)
        except Exception:
            return []

    @staticmethod
    def generate_all_alerts(parcel, weather_data=None, soil_data=None, soil_moisture_data=None) -> List[Dict]:
        all_alerts = []
        # 🔥 Les alertes feu CRITICAL passent en premier
        all_alerts.extend(AlertService.generate_fire_alerts(parcel))
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
