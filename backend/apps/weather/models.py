# """
# apps/weather/models.py
# ----------------------
# 5 proxy models depuis SmartSaha/models/externalData.py et alerts.py.
# Tables BDD inchangées — zéro migration destructive.

# Méthodes héritées automatiquement par WeatherData (proxy) :
#     @property current_temperature     → temp actuelle °C
#     @property total_precipitation     → mm sur la période
#     @property agricultural_alerts     → liste d'alertes générées
#     @property optimal_planting_days   → jours optimaux semis
#     @property irrigation_recommendation → recommandation irrigation
#     @property crop_specific_advice    → conseils par culture
#     get_weather_summary()             → résumé dashboard
#     calculate_growing_degree_days()   → degrés-jours de croissance
#     save()                            → auto-remplit location_name + risk_level
#     get_latest_for_parcel()           → classmethod, dernière donnée pour parcelle
# """
# Proxy models depuis SmartSaha/models/externalData.py et alerts.py retirés.


# class SoilData(_SoilData):
#     """
#     Proxy → table 'SmartSaha_soildata'.
#     Champs : parcel (FK), data (JSONField), created_at
#     """
#     class Meta:
#         proxy = True
#         app_label = 'weather'
#         verbose_name = 'Données sol'
#         verbose_name_plural = 'Données sol'


# class ClimateData(_ClimateData):
#     """
#     Proxy → table 'SmartSaha_climatedata'.
#     Champs : parcel (FK), data (JSONField), start, end, created_at
#     """
#     class Meta:
#         proxy = True
#         app_label = 'weather'
#         verbose_name = 'Données climatiques'
#         verbose_name_plural = 'Données climatiques'


# class WeatherData(_WeatherData):
#     """
#     Proxy → table 'SmartSaha_weatherdata'.
#     Hérite de BaseWeatherModel (abstract) via _WeatherData.
#     Toutes les méthodes de domaine sont héritées automatiquement.
#     Champs clés : parcel, data (JSON), start, end, data_type,
#                   risk_level, location_name
#     """
#     class Meta:
#         proxy = True
#         app_label = 'weather'
#         verbose_name = 'Données météo'
#         verbose_name_plural = 'Données météo'


# class AgriculturalAlert(_AgriculturalAlert):
#     """
#     Proxy → table 'SmartSaha_agriculturalalert'.
#     Hérite AgriculturalAlertManager (high_priority(), for_parcel()).
#     Champs : weather_data (FK), alert_type, message, recommendation,
#              severity, alert_date, is_active
#     """
#     class Meta:
#         proxy = True
#         app_label = 'weather'
#         verbose_name = 'Alerte agricole'
#         verbose_name_plural = 'Alertes agricoles'


# class Alert(_Alert):
#     """
#     Proxy → table 'SmartSaha_alert'.
#     Alertes agronomiques générées pour une parcelle.
#     Champs : parcel (FK), type, message, severity, action,
#              is_read, created_at, alert_date
#     Choix severity : LOW, MEDIUM, HIGH, CRITICAL
#     """
#     class Meta:
#         proxy = True
#         app_label = 'weather'
#         verbose_name = 'Alerte'
#         verbose_name_plural = 'Alertes'

#     def is_critical(self) -> bool:
#         """Retourne True si l'alerte est critique ou haute priorité."""
#         return self.severity in ('HIGH', 'CRITICAL')


from django.db import models

class SoilData(models.Model):
    parcel = models.ForeignKey('parcels.Parcel', on_delete=models.CASCADE, related_name='soil_data')
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class ClimateData(models.Model):
    parcel = models.ForeignKey('parcels.Parcel', on_delete=models.CASCADE, related_name='climate_data')
    data = models.JSONField()
    start = models.DateField()
    end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class BaseWeatherModel(models.Model):
    """Classe abstraite de base pour tous les modèles météo"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class WeatherData(BaseWeatherModel):
    parcel = models.ForeignKey('parcels.Parcel', on_delete=models.CASCADE, related_name='weather_data')
    data = models.JSONField()
    start = models.DateField()
    end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Nouvelles métadonnées pour requêtes performantes
    location_name = models.CharField(max_length=100, blank=True)
    data_type = models.CharField(max_length=50, choices=[
        ('FORECAST', 'Prévision'),
        ('HISTORICAL', 'Historique'),
        ('CURRENT', 'Actuel')
    ])
    risk_level = models.CharField(max_length=20, blank=True)  # Bas, Moyen, Élevé

    class Meta:
        indexes = [
            models.Index(fields=['parcel', 'start']),
            models.Index(fields=['data_type', 'risk_level']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-start']

    @property
    def current_temperature(self):
        """Température actuelle en °C"""
        return self.data.get('current', {}).get('temp_c')

    @property
    def total_precipitation(self):
        """Précipitations totales sur la période"""
        forecast_days = self.data.get('forecast', {}).get('forecastday', [])
        return sum(day['day']['totalprecip_mm'] for day in forecast_days)

    @property
    def agricultural_alerts(self):
        """Génère les alertes agricoles depuis les données JSON"""
        return self._generate_alerts()

    def _generate_alerts(self):
        alerts = []
        forecast_days = self.data.get('forecast', {}).get('forecastday', [])

        for day in forecast_days:
            day_data = day['day']
            date = day['date']

            # Alerte pluie intense
            if day_data['totalprecip_mm'] > 20:
                alerts.append({
                    'date': date,
                    'type': 'HEAVY_RAIN',
                    'message': f"🌧️ Pluie intense prévue: {day_data['totalprecip_mm']}mm",
                    'severity': 'HIGH',
                    'action': 'Reporter travaux drainage'
                })

            # Alerte sécheresse
            if day_data['totalprecip_mm'] == 0 and day_data['avgtemp_c'] > 30:
                alerts.append({
                    'date': date,
                    'type': 'DROUGHT_RISK',
                    'message': "🌵 Risque de stress hydrique",
                    'severity': 'MEDIUM',
                    'action': 'Irrigation recommandée'
                })

            # Alerte gel (pour cultures sensibles)
            if day_data['mintemp_c'] < 5:
                alerts.append({
                    'date': date,
                    'type': 'FROST_RISK',
                    'message': f"❄️ Risque de gel: {day_data['mintemp_c']}°C",
                    'severity': 'HIGH',
                    'action': 'Protéger cultures sensibles'
                })

            # Alerte vent fort
            if day_data['maxwind_kph'] > 30:
                alerts.append({
                    'date': date,
                    'type': 'STRONG_WIND',
                    'message': f"💨 Vent fort: {day_data['maxwind_kph']} km/h",
                    'severity': 'MEDIUM',
                    'action': 'Éviter traitements phytosanitaires'
                })

            # Alerte humidité élevée (maladies fongiques)
            if day_data['avghumidity'] > 85:
                alerts.append({
                    'date': date,
                    'type': 'HIGH_HUMIDITY',
                    'message': f"💧 Humidité élevée: {day_data['avghumidity']}%",
                    'severity': 'MEDIUM',
                    'action': 'Surveiller maladies fongiques'
                })

        return alerts

    @property
    def optimal_planting_days(self):
        """Jours optimaux pour les semis"""
        optimal_days = []
        forecast_days = self.data.get('forecast', {}).get('forecastday', [])

        for day in forecast_days:
            day_data = day['day']
            # Conditions optimales: pas de pluie forte, températures modérées
            if (day_data['daily_chance_of_rain'] < 30 and
                    15 <= day_data['avgtemp_c'] <= 25 and
                    day_data['maxwind_kph'] < 20):
                optimal_days.append({
                    'date': day['date'],
                    'score': 85,  # Score de pertinence
                    'reason': 'Conditions climatiques optimales'
                })

        return sorted(optimal_days, key=lambda x: x['score'], reverse=True)

    @property
    def irrigation_recommendation(self):
        """Recommandations d'irrigation"""
        forecast_days = self.data.get('forecast', {}).get('forecastday', [])
        total_rain = sum(day['day']['totalprecip_mm'] for day in forecast_days)

        if total_rain > 40:
            return {"irrigation": "Non nécessaire", "reason": "Pluies suffisantes"}
        elif total_rain > 20:
            return {"irrigation": "Légère", "reason": "Pluies modérées"}
        else:
            return {"irrigation": "Nécessaire", "reason": "Faibles précipitations"}

    @property
    def crop_specific_advice(self):
        """Conseils par type de culture"""
        advice = {}
        current_temp = self.current_temperature

        if current_temp < 10:
            advice['general'] = "🌱 Semis sous abri recommandé"
        elif current_temp > 35:
            advice['general'] = "🌞 Protection contre la chaleur nécessaire"

        # Conseils spécifiques selon les données
        if self.total_precipitation > 50:
            advice['drainage'] = "Vérifier le drainage des parcelles"

        return advice

    def get_weather_summary(self):
        """Résumé météo pour dashboard"""
        current = self.data.get('current', {})
        forecast_days = self.data.get('forecast', {}).get('forecastday', [])

        return {
            'current_conditions': {
                'temperature': current.get('temp_c'),
                'humidity': current.get('humidity'),
                'condition': current.get('condition', {}).get('text'),
                'precipitation': current.get('precip_mm')
            },
            'forecast_stats': {
                'max_temp': max(day['day']['maxtemp_c'] for day in forecast_days),
                'min_temp': min(day['day']['mintemp_c'] for day in forecast_days),
                'total_rain': self.total_precipitation,
                'rainy_days': sum(1 for day in forecast_days if day['day']['totalprecip_mm'] > 0)
            }
        }

    def calculate_growing_degree_days(self, base_temp=10):
        """Calcul des degrés-jours de croissance"""
        forecast_days = self.data.get('forecast', {}).get('forecastday', [])
        gdd = 0

        for day in forecast_days:
            day_data = day['day']
            avg_temp = day_data['avgtemp_c']
            if avg_temp > base_temp:
                gdd += (avg_temp - base_temp)

        return gdd

    def save(self, *args, **kwargs):
        """Auto-remplissage des métadonnées à la sauvegarde"""
        if not self.location_name and 'location' in self.data:
            self.location_name = self.data['location']['name']

        if not self.risk_level:
            self.risk_level = self._calculate_risk_level()

        super().save(*args, **kwargs)

    def _calculate_risk_level(self):
        """Calcule automatiquement le niveau de risque"""
        alerts = self.agricultural_alerts
        high_risk_count = sum(1 for alert in alerts if alert['severity'] == 'HIGH')

        if high_risk_count >= 2:
            return 'HIGH'
        elif high_risk_count >= 1:
            return 'MEDIUM'
        else:
            return 'LOW'

    @classmethod
    def get_latest_for_parcel(cls, parcel):
        """Récupère les dernières données pour une parcelle"""
        return cls.objects.filter(parcel=parcel).latest('created_at')

    pass


class AgriculturalAlertManager(models.Manager):
    """Manager personnalisé pour les alertes"""

    def high_priority(self):
        return self.filter(severity='HIGH')

    def for_parcel(self, parcel):
        return self.filter(weather_data__parcel=parcel)


class AgriculturalAlert(BaseWeatherModel):
    """Modèle pour stocker les alertes générées"""
    SEVERITY_CHOICES = [
        ('LOW', 'Faible'),
        ('MEDIUM', 'Moyen'),
        ('HIGH', 'Élevé'),
    ]

    weather_data = models.ForeignKey(WeatherData, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50)
    message = models.TextField()
    recommendation = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    alert_date = models.DateField()
    is_active = models.BooleanField(default=True)

    objects = AgriculturalAlertManager()


class Alert(models.Model):
    """
    Alertes agronomiques générées pour une parcelle.
    Migré depuis SmartSaha/models/alerts.py — FK parcel pointe maintenant vers parcels.Parcel.
    """
    SEVERITY_CHOICES = [
        ('LOW',      'Faible'),
        ('MEDIUM',   'Moyenne'),
        ('HIGH',     'Haute'),
        ('CRITICAL', 'Critique'),
    ]

    parcel   = models.ForeignKey('parcels.Parcel', on_delete=models.CASCADE, related_name='alerts')
    type     = models.CharField(max_length=100)
    message  = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    action   = models.TextField(blank=True)
    is_read  = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    alert_date  = models.DateField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.severity}] {self.type} — {self.parcel.parcel_name}"

    def is_critical(self) -> bool:
        """Retourne True si l'alerte est critique ou haute priorité."""
        return self.severity in ('HIGH', 'CRITICAL')