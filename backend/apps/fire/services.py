"""
apps/fire/services.py
---------------------
FireAlertService : Récupère les données FIRMS NASA, filtre sur Madagascar,
croise avec les parcelles GPS et génère des alertes CRITICAL/HIGH.

Source NASA FIRMS (sans clé API) :
  https://firms.modaps.eosdis.nasa.gov/api/area/csv/{MAP_KEY}/MODIS_NRT/{area}/{days}

Fallback sans clé : fichier CSV local fires_madagascar.csv
"""
from __future__ import annotations

import csv
import io
import logging
import math
import os
import threading
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

import requests as http
from django.conf import settings
from django.core.mail import send_mail

from apps.fire.models import FireAlert
from apps.parcels.models import Parcel

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────
# Bounding-box Madagascar
MADA_LAT_MIN, MADA_LAT_MAX = -25.0, -12.0
MADA_LON_MIN, MADA_LON_MAX = 43.0,  51.0

# Rayon d'alerte autour d'une parcelle (km)
FIRE_ALERT_RADIUS_KM = 15.0

# Seuil brightness (Kelvin) pour sévérité CRITICAL
BRIGHTNESS_CRITICAL = 370.0
BRIGHTNESS_HIGH     = 330.0

# URL NASA FIRMS (mode public, MAP_KEY optionnel)
FIRMS_CSV_URL = (
    "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/"
    "MODIS_C6_1_Global_24h.csv"
)

# Chemin vers le CSV local de fallback
FIRE_DIR      = os.path.join(settings.BASE_DIR, 'fire')
LOCAL_CSV     = os.path.join(FIRE_DIR, 'fires_madagascar.csv')


# ── Utilitaires ──────────────────────────────────────────────────────────────

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcule la distance en km entre deux points GPS (formule haversine)."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi  = math.radians(lat2 - lat1)
    dlam  = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _brightness_to_severity(brightness: float) -> str:
    if brightness >= BRIGHTNESS_CRITICAL:
        return 'CRITICAL'
    if brightness >= BRIGHTNESS_HIGH:
        return 'HIGH'
    return 'MEDIUM'


# ── Service principal ─────────────────────────────────────────────────────────

class FireAlertService:
    """
    Orchestre :
      1. Récupération données FIRMS (NASA) ou fallback CSV local
      2. Filtrage sur Madagascar
      3. Croisement géographique avec les parcelles
      4. Sauvegarde des FireAlert en BDD
      5. Envoi email de notification à l'agriculteur
    """

    # ── Étape 1 : récupération données FIRMS ──────────────────────────────────

    def fetch_firms_rows(self) -> List[Dict]:
        """
        Télécharge le CSV FIRMS global et filtre sur Madagascar.
        Si le téléchargement échoue, utilise le fichier local.
        Retourne une liste de dicts avec keys: latitude, longitude,
        brightness, confidence, acq_date, acq_time, satellite.
        """
        try:
            logger.info("FireAlertService: téléchargement CSV FIRMS NASA …")
            resp = http.get(FIRMS_CSV_URL, timeout=30)
            resp.raise_for_status()
            rows = self._parse_csv(resp.text)
            logger.info(f"FIRMS: {len(rows)} lignes brutes téléchargées")
        except Exception as exc:
            logger.warning(f"FIRMS téléchargement échoué ({exc}), fallback CSV local")
            rows = self._load_local_csv()

        filtered = self._filter_madagascar(rows)
        logger.info(f"FIRMS: {len(filtered)} points chauds sur Madagascar")
        return filtered

    def _parse_csv(self, text: str) -> List[Dict]:
        rows = []
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            try:
                rows.append({
                    'latitude':   float(row.get('latitude', 0)),
                    'longitude':  float(row.get('longitude', 0)),
                    'brightness': float(row.get('brightness', 0)),
                    'confidence': int(row.get('confidence', 50)),
                    'acq_date':   row.get('acq_date', ''),
                    'acq_time':   row.get('acq_time', ''),
                    'satellite':  row.get('satellite', ''),
                })
            except (ValueError, KeyError):
                continue
        return rows

    def _load_local_csv(self) -> List[Dict]:
        if not os.path.exists(LOCAL_CSV):
            logger.error("Fichier CSV local introuvable : %s", LOCAL_CSV)
            return []
        with open(LOCAL_CSV, 'r', encoding='utf-8') as f:
            return self._parse_csv(f.read())

    def _filter_madagascar(self, rows: List[Dict]) -> List[Dict]:
        return [
            r for r in rows
            if MADA_LAT_MIN <= r['latitude'] <= MADA_LAT_MAX
            and MADA_LON_MIN <= r['longitude'] <= MADA_LON_MAX
        ]

    # ── Étape 2 : croisement avec les parcelles ───────────────────────────────

    def match_fires_to_parcels(
        self, fire_rows: List[Dict], radius_km: float = FIRE_ALERT_RADIUS_KM
    ) -> List[Dict]:
        """
        Pour chaque point chaud, cherche la parcelle la plus proche.
        Si elle est dans le rayon, enrichit le dict avec parcel + distance_km.
        """
        parcels = list(Parcel.objects.prefetch_related('owner').all())
        matched = []

        for fire in fire_rows:
            nearest_parcel: Optional[Parcel] = None
            nearest_dist   = float('inf')

            for parcel in parcels:
                center = parcel.get_center()
                if not center:
                    continue
                dist = haversine_km(
                    fire['latitude'],  fire['longitude'],
                    center['lat'],     center['lng']
                )
                if dist < nearest_dist:
                    nearest_dist   = dist
                    nearest_parcel = parcel

            fire['parcel']      = nearest_parcel if nearest_dist <= radius_km else None
            fire['distance_km'] = round(nearest_dist, 2) if nearest_parcel else None
            matched.append(fire)

        return matched

    # ── Étape 3 : sauvegarde en BDD ──────────────────────────────────────────

    def save_fire_alerts(self, fire_rows: List[Dict]) -> Tuple[int, int]:
        """
        Insère les nouvelles alertes (ignore les doublons par unique_together).
        Retourne (created_count, skipped_count).
        """
        created, skipped = 0, 0

        for fire in fire_rows:
            # Parser la date
            try:
                acq_date = datetime.strptime(fire['acq_date'], '%Y-%m-%d').date()
            except ValueError:
                acq_date = date.today()

            severity = _brightness_to_severity(fire['brightness'])

            obj, new = FireAlert.objects.get_or_create(
                latitude  = round(fire['latitude'],  4),
                longitude = round(fire['longitude'], 4),
                acq_date  = acq_date,
                acq_time  = fire.get('acq_time', ''),
                satellite = fire.get('satellite', ''),
                defaults={
                    'brightness':  fire['brightness'],
                    'confidence':  fire.get('confidence', 50),
                    'parcel':      fire.get('parcel'),
                    'distance_km': fire.get('distance_km'),
                    'severity':    severity,
                    'is_active':   True,
                    'is_notified': False,
                }
            )
            if new:
                created += 1
            else:
                skipped += 1

        return created, skipped

    # ── Étape 4 : notifications email ─────────────────────────────────────────

    def send_notifications(self) -> int:
        """
        Envoie un email à chaque agriculteur pour les alertes non notifiées
        liées à sa parcelle. Asynchrone via threading.
        """
        pending = FireAlert.objects.filter(
            is_notified=False,
            is_active=True,
            parcel__isnull=False,
        ).select_related('parcel', 'parcel__owner')

        notified = 0
        for alert in pending:
            owner = alert.parcel.owner
            if not owner.email:
                continue
            self._send_email_async(alert, owner)
            alert.is_notified = True
            alert.save(update_fields=['is_notified'])
            notified += 1

        return notified

    def _send_email_async(self, alert: FireAlert, owner) -> None:
        parcel_name = alert.parcel.parcel_name
        severity_label = {'CRITICAL': '🔴 CRITIQUE', 'HIGH': '🟠 ÉLEVÉ', 'MEDIUM': '🟡 MOYEN'}.get(
            alert.severity, alert.severity
        )
        subject = f"⚠️ Alerte Feu {severity_label} — Parcelle « {parcel_name} »"
        message = (
            f"Bonjour {owner.first_name or owner.username},\n\n"
            f"Un incendie a été détecté à proximité de votre parcelle "
            f"« {parcel_name} » !\n\n"
            f"  📍 Position du feu : {alert.latitude:.4f}°N, {alert.longitude:.4f}°E\n"
            f"  📏 Distance à votre parcelle : {alert.distance_km:.1f} km\n"
            f"  🌡️ Intensité : {alert.brightness:.0f} K (brightness)\n"
            f"  📅 Détecté le : {alert.acq_date.strftime('%d/%m/%Y')}\n"
            f"  🛰️ Satellite : {alert.satellite or 'MODIS'}\n"
            f"  ⚠️ Sévérité : {severity_label}\n\n"
            f"Veuillez prendre les mesures de protection nécessaires :\n"
            f"  • Éloigner les récoltes et équipements sensibles\n"
            f"  • Contacter les autorités locales si nécessaire\n"
            f"  • Surveiller l'évolution du feu via l'application SmartSaha\n\n"
            f"Cette alerte est générée automatiquement depuis les données "
            f"satellitaires NASA FIRMS (MODIS/VIIRS).\n\n"
            f"L'équipe SmartSaha"
        )

        def _send():
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[owner.email],
                    fail_silently=False,
                )
                logger.info(f"Email alerte feu envoyé à {owner.email} pour parcelle {parcel_name}")
            except Exception as exc:
                logger.error(f"Erreur envoi email alerte feu à {owner.email}: {exc}")

        threading.Thread(target=_send, daemon=True).start()

    # ── Pipeline complet ──────────────────────────────────────────────────────

    def run(self, radius_km: float = FIRE_ALERT_RADIUS_KM) -> Dict:
        """
        Exécute le pipeline complet :
        fetch → filter → match → save → notify.
        Retourne un rapport d'exécution.
        """
        fire_rows = self.fetch_firms_rows()
        matched   = self.match_fires_to_parcels(fire_rows, radius_km)
        created, skipped = self.save_fire_alerts(matched)
        notified  = self.send_notifications()

        near_parcel = sum(1 for f in matched if f['parcel'] is not None)
        report = {
            'total_hotspots_madagascar': len(fire_rows),
            'near_parcel_count':         near_parcel,
            'alerts_created':            created,
            'alerts_skipped_duplicates': skipped,
            'notifications_sent':        notified,
        }
        logger.info(f"FireAlertService.run() → {report}")
        return report

    # ── Méthode helper pour AlertService (intégration existante) ─────────────

    @staticmethod
    def generate_fire_alerts_for_parcel(parcel) -> List[Dict]:
        """
        Retourne les alertes feu ACTIVE liées à une parcelle,
        dans le même format que les autres alertes de AlertService.
        """
        alerts = []
        fire_qs = FireAlert.objects.filter(
            parcel=parcel,
            is_active=True,
        ).order_by('-acq_date')[:5]  # 5 plus récentes

        for fire in fire_qs:
            alerts.append({
                'type':     '🔥 FEU DÉTECTÉ',
                'message':  (
                    f"Incendie à {fire.distance_km:.1f} km de « {parcel.parcel_name} » "
                    f"— Intensité {fire.brightness:.0f} K ({fire.satellite or 'MODIS'})"
                ),
                'severity': fire.severity,
                'action':   (
                    "Protéger les récoltes et contacter les autorités locales. "
                    "Surveiller l'évolution via SmartSaha."
                ),
                'date':     fire.acq_date.isoformat(),
                'distance_km':  fire.distance_km,
                'latitude':     fire.latitude,
                'longitude':    fire.longitude,
            })
        return alerts
