"""
apps/dashboard/services.py
--------------------------
Fusion de :
    SmartSaha/services/Dashboard.py   → DashboardService
    SmartSaha/services/parcelData.py  → ParcelDataService
"""
import requests as http_requests

from django.core.cache import cache
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone

from apps.parcels.models import Parcel
from apps.crops.models import ParcelCrop
from apps.yields.models import YieldRecord
from apps.tasks.models import Task
from apps.weather.models import SoilData, WeatherData


# ══════════════════════════════════════════════════════════════════════════════
# DashboardService
# ══════════════════════════════════════════════════════════════════════════════
class DashboardService:
    """
    Dashboard optimisé : agrégations SQL, mise en cache par bloc (15 min).
    """
    CACHE_TIMEOUT = 60 * 15  # 15 min

    def __init__(self, user):
        self.user = user

    # ── Parcelles ─────────────────────────────────────────────────────────────
    def get_parcels_data(self):
        cache_key = f'dashboard_{self.user.pk}_parcels'
        data = cache.get(cache_key)
        if data:
            return data

        parcels = Parcel.objects.filter(owner=self.user)
        data = [
            {'id': str(p.uuid), 'name': p.parcel_name, 'points': p.points}
            for p in parcels
        ]
        cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return data

    # ── Sols ──────────────────────────────────────────────────────────────────
    def get_soil_summary(self):
        cache_key = f'dashboard_{self.user.pk}_soil'
        data = cache.get(cache_key)
        if data:
            return data

        # Optimisation : On récupère tous les records SoilData d'un coup
        # On utilise une liste de parcelles déjà filtrée
        parcels = Parcel.objects.filter(owner=self.user)
        parcel_ids = [p.pk for p in parcels]
        
        # Récupérer tous les records de sol pour ces parcelles
        soil_records_map = {}
        for s in SoilData.objects.filter(parcel_id__in=parcel_ids):
            soil_records_map.setdefault(str(s.parcel_id), []).append(s)

        soil_summary = []
        for parcel in parcels:
            p_uuid = str(parcel.uuid)
            records = soil_records_map.get(p_uuid, [])
            layer_agg = {}

            for soil in records:
                layers = soil.data.get('properties', {}).get('layers', [])
                for layer in layers:
                    name = layer.get('name')
                    for depth in layer.get('depths', []):
                        val = depth.get('values', {}).get('mean')
                        if val is not None:
                            layer_agg.setdefault(name, []).append(val)

            summary = (
                {k: sum(v) / len(v) for k, v in layer_agg.items()}
                if layer_agg else None
            )
            soil_summary.append({
                'parcel_id':    p_uuid,
                'soil_summary': summary,
            })

        cache.set(cache_key, soil_summary, timeout=self.CACHE_TIMEOUT)
        return soil_summary

    # ── Météo ─────────────────────────────────────────────────────────────────
    def get_weather_summary(self):
        cache_key = f'dashboard_{self.user.pk}_weather'
        data = cache.get(cache_key)
        if data:
            return data

        parcels = Parcel.objects.filter(owner=self.user)
        # Optimisation : On pourrait utiliser une sous-requête, mais ici on va juste
        # récupérer les derniers WeatherData pour toutes les parcelles d'un coup.
        # Pour faire simple et efficace, on prend les records récents.
        latest_weather = {
            str(w.parcel_id): w 
            for w in WeatherData.objects.filter(parcel__owner=self.user).order_by('created_at')
        }

        weather_summary = []
        for parcel in parcels:
            latest = latest_weather.get(str(parcel.uuid))
            summary = None
            if latest:
                summary = {
                    'current_temperature':       latest.current_temperature,
                    'total_precipitation':       latest.total_precipitation,
                    'risk_level':                latest.risk_level,
                    'location':                  latest.location_name,
                    'alerts_count':              len(latest.agricultural_alerts),
                    'optimal_planting_days':     latest.optimal_planting_days,
                    'irrigation_recommendation': latest.irrigation_recommendation,
                    'weather_summary':           latest.get_weather_summary(),
                }

            weather_summary.append({
                'parcel_id':       str(parcel.uuid),
                'parcel_name':     parcel.parcel_name,
                'weather_summary': summary,
            })

        cache.set(cache_key, weather_summary, timeout=self.CACHE_TIMEOUT)
        return weather_summary

    def get_enhanced_weather_summary(self):
        """Version enrichie avec analyse agricole complète."""
        cache_key = f'dashboard_{self.user.pk}_enhanced_weather'
        data = cache.get(cache_key)
        if data:
            return data

        from apps.weather.services import AgriculturalAnalyzer
        analyzer = AgriculturalAnalyzer()

        # FIX : prefetch_related supprimé → filtre direct
        parcels = Parcel.objects.filter(owner=self.user)
        enhanced = []

        for parcel in parcels:
            latest = WeatherData.objects.filter(parcel=parcel).order_by('-created_at').first()
            if latest:
                analysis = analyzer.analyze_weather_data(latest)
                summary = {
                    'current_temperature':       latest.current_temperature,
                    'total_precipitation':       latest.total_precipitation,
                    'risk_level':                latest.risk_level,
                    'location':                  latest.location_name,
                    'alerts':                    latest.agricultural_alerts,
                    'high_priority_alerts':      [a for a in latest.agricultural_alerts if a['severity'] == 'HIGH'],
                    'risk_assessment':           analysis.get('risk_assessment'),
                    'optimal_planting_days':     analysis.get('optimal_planting_days'),
                    'irrigation_recommendation': analysis.get('irrigation_recommendation'),
                    'growing_degree_days':       latest.calculate_growing_degree_days(),
                    'weather_conditions':        latest.get_weather_summary(),
                    'data_type':                 latest.data_type,
                    'last_updated':              latest.created_at,
                }
            else:
                summary = {'status': 'no_data', 'message': 'Aucune donnée météo disponible'}

            enhanced.append({
                'parcel_id':   str(parcel.uuid),
                'parcel_name': parcel.parcel_name,
                'weather_data': summary,
            })

        cache.set(cache_key, enhanced, timeout=self.CACHE_TIMEOUT)
        return enhanced

    def get_dashboard_weather_overview(self):
        """Version compacte pour le dashboard principal."""
        cache_key = f'dashboard_{self.user.pk}_weather_overview'
        data = cache.get(cache_key)
        if data:
            return data

        parcels = Parcel.objects.filter(owner=self.user)
        overview = {
            'total_parcels':             parcels.count(),
            'parcels_with_weather_data': 0,
            'high_risk_parcels':         0,
            'total_alerts':              0,
            'parcel_details':            [],
        }

        for parcel in parcels:
            latest = WeatherData.objects.filter(parcel=parcel).order_by('-created_at').first()
            if latest:
                overview['parcels_with_weather_data'] += 1
                alerts   = latest.agricultural_alerts
                high_risk = [a for a in alerts if a['severity'] == 'HIGH']
                if latest.risk_level == 'HIGH' or len(high_risk) > 0:
                    overview['high_risk_parcels'] += 1
                overview['total_alerts'] += len(alerts)
                parcel_info = {
                    'parcel_id':            str(parcel.uuid),
                    'parcel_name':          parcel.parcel_name,
                    'current_temperature':  latest.current_temperature,
                    'risk_level':           latest.risk_level,
                    'alerts_count':         len(alerts),
                    'high_priority_alerts': len(high_risk),
                    'location':             latest.location_name,
                }
            else:
                parcel_info = {
                    'parcel_id':   str(parcel.uuid),
                    'parcel_name': parcel.parcel_name,
                    'status':      'no_data',
                }
            overview['parcel_details'].append(parcel_info)

        cache.set(cache_key, overview, timeout=self.CACHE_TIMEOUT)
        return overview

    def refresh_weather_data(self):
        """Force le rafraîchissement météo pour toutes les parcelles."""
        from apps.weather.services import WeatherDataCollector
        collector = WeatherDataCollector()
        parcels   = Parcel.objects.filter(owner=self.user)
        results   = []

        for parcel in parcels:
            if parcel.points:
                result = collector.collect_and_save_weather_data(parcel)
                results.append({
                    'parcel_name':      parcel.parcel_name,
                    'success':          result['success'],
                    'alerts_generated': result.get('alerts_generated', 0),
                    'error':            result.get('error'),
                })

        for key in [
            f'dashboard_{self.user.pk}_weather',
            f'dashboard_{self.user.pk}_enhanced_weather',
            f'dashboard_{self.user.pk}_weather_overview',
        ]:
            cache.delete(key)

        return results

    # ── Rendements ────────────────────────────────────────────────────────────
    def get_yield_summary(self):
        cache_key = f'dashboard_{self.user.pk}_yield'
        data = cache.get(cache_key)
        if data:
            return data

        from django.db.models import F
        parcel_crops = (
            ParcelCrop.objects.filter(parcel__owner=self.user)
            .annotate(
                total_yield=Sum('yield_records__yield_amount'),
                avg_yield=Avg('yield_records__yield_amount'),
                parcel_name=F('parcel__parcel_name'),
                crop_name=F('crop__name'),
            )
        )
        data = [
            {
                'parcel_crop_id': pc.id,
                'parcel_name':    pc.parcel_name,
                'crop_name':      pc.crop_name,
                'summary': {
                    'total_yield': pc.total_yield,
                    'avg_yield':   pc.avg_yield,
                } if pc.total_yield is not None else None,
            }
            for pc in parcel_crops
        ]
        cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return data

    # ── Tâches ────────────────────────────────────────────────────────────────
    def get_task_summary(self):
        cache_key = f'dashboard_{self.user.pk}_task'
        data = cache.get(cache_key)
        if data:
            return data

        # Optimisations : Agrégation globale regroupée par parcelle
        stats = (
            Task.objects.filter(parcelCrop__parcel__owner=self.user)
            .values('parcelCrop__parcel__uuid')
            .annotate(
                total=Count('id'),
                done=Count('id', filter=Q(status__name='Done'))
            )
        )
        stats_map = {str(s['parcelCrop__parcel__uuid']): s for s in stats}

        parcels = Parcel.objects.filter(owner=self.user)
        data = []
        for parcel in parcels:
            p_uuid = str(parcel.uuid)
            p_stats = stats_map.get(p_uuid, {'total': 0, 'done': 0})
            data.append({
                'parcel_id': p_uuid,
                'task_summary': {
                    'total_tasks':     p_stats['total'],
                    'completed_tasks': p_stats['done'],
                },
            })

        cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return data

    # ── Dashboard complet ─────────────────────────────────────────────────────
    def get_full_dashboard(self):
        """Assemble tous les blocs (depuis cache ou recalcul)."""
        return {
            'parcels':         self.get_parcels_data(),
            'soil_summary':    self.get_soil_summary(),
            'climate_summary': self.get_dashboard_weather_overview(),
            'yield_summary':   self.get_yield_summary(),
            'task_summary':    self.get_task_summary(),
        }

    # ── BI Dashboard (Organisation) ───────────────────────────────────────────
    def get_bi_dashboard_data(self, timeframe='annee'):
        """Données réelles pour l'espace organisation.
        
        Args:
            timeframe: 'annee' pour l'année en cours, 'mois' pour le mois en cours.
        """
        from apps.groups.models import Organisation, Group, MemberGroup
        from django.db.models.functions import ExtractMonth

        org = Organisation.objects.filter(
            Q(created_by=self.user) | Q(groups__members__user=self.user)
        ).distinct().first()

        if not org:
            return {
                'kpis': [],
                'production_chart': {'labels': [], 'datasets': []},
                'regions': [],
                'impact': {'chart_data': {'labels': [], 'datasets': []}, 'metrics': []},
                'ai_insights': [],
                'org_name': "Aucune organisation"
            }

        now = timezone.now()
        groups = Group.objects.filter(organisation=org)
        groups_count = groups.count()
        members_count = MemberGroup.objects.filter(group__organisation=org, status='ACTIVE').count()
        
        # Base queryset des rendements de toute l'org
        all_yield_records = YieldRecord.objects.filter(
            parcelCrop__parcel__owner__group_memberships__group__organisation=org,
            parcelCrop__parcel__owner__group_memberships__status='ACTIVE'
        ).distinct()
        
        # Filtrage selon le timeframe
        if timeframe == 'mois':
            yield_records = all_yield_records.filter(
                date__year=now.year,
                date__month=now.month,
            )
        else:  # 'annee' par défaut
            yield_records = all_yield_records.filter(date__year=now.year)
        
        total_yield = yield_records.aggregate(s=Sum('yield_amount'))['s'] or 0
        revenue_est = float(total_yield) * 1.5

        # ── Calcul du trend (mois précédent vs mois actuel)
        prev_month = (now.month - 2) % 12 + 1
        prev_year = now.year if now.month > 1 else now.year - 1
        prev_month_yield = all_yield_records.filter(
            date__year=prev_year, date__month=prev_month
        ).aggregate(s=Sum('yield_amount'))['s'] or 0
        curr_month_yield = all_yield_records.filter(
            date__year=now.year, date__month=now.month
        ).aggregate(s=Sum('yield_amount'))['s'] or 0
        
        if prev_month_yield > 0:
            trend_pct = ((float(curr_month_yield) - float(prev_month_yield)) / float(prev_month_yield)) * 100
            trend_str = f"{trend_pct:+.0f}%"
            trend_up = trend_pct >= 0
        else:
            trend_str = 'N/A'
            trend_up = True

        bi_kpis = [
            { 'label': 'Volume Total', 'value': f"{total_yield:,.0f} kg", 'trend': trend_str, 'trendUp': trend_up, 'progress': min(int((float(total_yield) / 10000) * 100), 100), 'icon': 'bx bx-package', 'bg': 'bg-emerald-500', 'bgLight': 'bg-emerald-400', 'text': 'text-white', 'barColor': 'bg-emerald-500' },
            { 'label': 'Revenu Estimé', 'value': f"{revenue_est:,.0f} Ar", 'trend': trend_str, 'trendUp': trend_up, 'progress': 62, 'icon': 'bx bx-money', 'bg': 'bg-blue-500', 'bgLight': 'bg-blue-400', 'text': 'text-white', 'barColor': 'bg-blue-500' },
            { 'label': 'Groupes Opérationnels', 'value': str(groups_count), 'trend': '+', 'trendUp': True, 'progress': 100, 'icon': 'bx bx-buildings', 'bg': 'bg-amber-500', 'bgLight': 'bg-amber-400', 'text': 'text-white', 'barColor': 'bg-amber-500' },
            { 'label': 'Membres Actifs', 'value': str(members_count), 'trend': '+', 'trendUp': True, 'progress': 100, 'icon': 'bx bx-user', 'bg': 'bg-[#10b481]', 'bgLight': 'bg-[#10b481]', 'text': 'text-white', 'barColor': 'bg-[#10b481]' },
        ]

        # ── Production par mois (pour le graphique)
        yields_by_month = yield_records.annotate(
            month=ExtractMonth('date')
        ).values('month').annotate(total=Sum('yield_amount')).order_by('month')
        
        if timeframe == 'mois':
            # Données journalières si vue mensuelle
            from django.db.models.functions import ExtractDay
            import calendar
            days_in_month = calendar.monthrange(now.year, now.month)[1]
            daily_data = {}
            yields_by_day = yield_records.annotate(
                day=ExtractDay('date')
            ).values('day').annotate(total=Sum('yield_amount')).order_by('day')
            for y in yields_by_day:
                if y['day']:
                    daily_data[y['day']] = float(y['total'] or 0)
            chart_labels = [str(d) for d in range(1, days_in_month + 1)]
            chart_data_values = [daily_data.get(d, 0) for d in range(1, days_in_month + 1)]
        else:
            monthly_data = [0.0] * 12
            for y in yields_by_month:
                if y['month']:
                    monthly_data[y['month'] - 1] = float(y['total'] or 0)
            chart_labels = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
            chart_data_values = monthly_data

        # ── Régions
        try:
            from django.db.models import F
            regions_data = yield_records.annotate(
                region_name=F('parcelCrop__parcel__owner__profile__region')
            ).values('region_name').annotate(total=Sum('yield_amount')).order_by('-total')[:5]
            
            regions_formatted = []
            for r in regions_data:
                name = r['region_name'] or 'Inconnue'
                tot = float(r['total'] or 0)
                pct = (tot / float(total_yield)) * 100 if total_yield > 0 else 0
                regions_formatted.append({ 'name': name, 'total': round(tot, 1), 'pct': round(pct, 1) })
            if not regions_formatted:
                regions_formatted = [{ 'name': 'Données en attente', 'total': 0, 'pct': 0 }]
        except Exception:
            regions_formatted = [{ 'name': 'Madagascar', 'total': float(total_yield), 'pct': 100 }]

        # ── Focus Impact : Répartition par culture (top 4)
        IMPACT_COLORS = ['#10b481', '#112830', '#219ebc', '#fb8500']
        BG_COLORS = ['bg-[#10b481]', 'bg-[#112830]', 'bg-[#219ebc]', 'bg-[#fb8500]']
        try:
            from django.db.models import F as Fmod
            crops_data = yield_records.annotate(
                crop_name=Fmod('parcelCrop__crop__name')
            ).values('crop_name').annotate(total=Sum('yield_amount')).order_by('-total')[:4]
            
            impact_labels, impact_data, impact_metrics = [], [], []
            for i, c in enumerate(crops_data):
                cname = c['crop_name'] or 'Autre'
                ctot = float(c['total'] or 0)
                cpct = round((ctot / float(total_yield)) * 100, 1) if total_yield > 0 else 0
                impact_labels.append(cname)
                impact_data.append(ctot)
                impact_metrics.append({
                    'label': cname,
                    'pct': cpct,
                    'color': BG_COLORS[i % len(BG_COLORS)]
                })
            
            if not impact_labels:
                impact_labels = ['Aucune donnée']
                impact_data = [1]
                impact_metrics = [{'label': 'Aucune donnée', 'pct': 100, 'color': BG_COLORS[0]}]
                
            impact_chart_data = {
                'labels': impact_labels,
                'datasets': [{
                    'data': impact_data,
                    'backgroundColor': IMPACT_COLORS[:len(impact_labels)],
                    'borderWidth': 0,
                    'hoverOffset': 20
                }]
            }
        except Exception:
            impact_chart_data = {'labels': ['Aucune donnée'], 'datasets': [{'data': [1], 'backgroundColor': ['#10b481'], 'borderWidth': 0, 'hoverOffset': 20}]}
            impact_metrics = [{'label': 'Aucune donnée', 'pct': 100, 'color': 'bg-[#10b481]'}]

        # ── IA Insights : Recommandations dynamiques
        ai_insights = []
        
        # Insight 1 : Tendance production
        if prev_month_yield > 0:
            if trend_up and trend_pct > 0:
                ai_insights.append({
                    'id': 1,
                    'title': 'Tendance Positive de Production',
                    'text': f"La production du mois en cours est en hausse de {trend_pct:.0f}% par rapport au mois précédent. Bonne dynamique à maintenir.",
                    'icon': 'bx-trending-up',
                    'iconColor': 'text-[#10b481]'
                })
            else:
                ai_insights.append({
                    'id': 1,
                    'title': 'Attention : Baisse de Production',
                    'text': f"La production du mois en cours est en baisse de {abs(trend_pct):.0f}% par rapport au mois précédent. Une analyse des causes est recommandée.",
                    'icon': 'bx-trending-down',
                    'iconColor': 'text-rose-500'
                })
        else:
            ai_insights.append({
                'id': 1,
                'title': 'Démarrage Enregistré',
                'text': f"L'organisation {org.name} a enregistré {total_yield:,.0f} kg de production depuis le début de l'année.",
                'icon': 'bx-leaf',
                'iconColor': 'text-[#10b481]'
            })

        # Insight 2 : Vitalité de l'organisation (membres et groupes)
        if members_count > 0:
            ai_insights.append({
                'id': 2,
                'title': 'Structure Organisationnelle',
                'text': f"{members_count} membres actifs répartis dans {groups_count} groupe(s). Votre réseau coopératif est {'solide' if members_count >= 10 else 'en croissance'}.",
                'icon': 'bx-group',
                'iconColor': 'text-amber-500'
            })
        else:
             ai_insights.append({
                'id': 2,
                'title': 'Développement du Réseau',
                'text': f"L'organisation compte {groups_count} groupe(s). Invitez plus de membres pour maximiser la production collective.",
                'icon': 'bx-group',
                'iconColor': 'text-amber-500'
            })
        
        # Insight 3 : Meilleure culture
        if impact_metrics and impact_metrics[0]['label'] != 'Aucune donnée':
            top_crop = impact_metrics[0]
            ai_insights.append({
                'id': 3,
                'title': f"Culture Principale : {top_crop['label']}",
                'text': f"{top_crop['label']} représente {top_crop['pct']}% de la production totale. Assurez un suivi prioritaire de cette filière.",
                'icon': 'bx-star',
                'iconColor': 'text-blue-500'
            })
        else:
            ai_insights.append({
                'id': 3,
                'title': 'Enregistrez vos Productions',
                'text': "Aucune donnée de production disponible. Commencez à enregistrer les rendements de vos parcelles pour obtenir des recommandations.",
                'icon': 'bx-info-circle',
                'iconColor': 'text-blue-500'
            })

        return {
            'org_name': org.name,
            'kpis': bi_kpis,
            'production_chart': {
                'labels': chart_labels,
                'datasets': [
                    { 'label': 'Production (kg)', 'data': chart_data_values, 'backgroundColor': '#10b481', 'borderRadius': 12 },
                ]
            },
            'regions': regions_formatted,
            'impact': {
                'chart_data': impact_chart_data,
                'metrics': impact_metrics,
            },
            'ai_insights': ai_insights,
        }

    
    # ── Admin Dashboard (Superviseur) ──────────────────────────────────────────
    def get_admin_dashboard_data(self):
        """Données globales pour l'administrateur système."""
        from apps.users.models import User
        from apps.groups.models import Organisation, Group
        from apps.crops.models import Crop, ParcelCrop
        from apps.tasks.models import Task
        
        total_users = User.objects.count()
        total_orgs = Organisation.objects.count()
        total_groups = Group.objects.count()
        
        # Agriculteurs : non-staff, pas de création d'org, pas leader actif de groupe
        total_farmers = (
            User.objects.filter(is_staff=False)
            .exclude(organisations_created__isnull=False)
            .exclude(
                group_memberships__role__role_type='LEADER',
                group_memberships__status='ACTIVE',
            )
            .distinct()
            .count()
        )
        
        total_parcels = Parcel.objects.count()
        total_crops = Crop.objects.count()
        total_parcel_crops = ParcelCrop.objects.count()
        total_tasks = Task.objects.count()
        
        return {
            'metrics': [
                { 'title': 'Utilisateurs Totaux', 'value': str(total_users), 'icon': 'bx bx-user', 'color': 'text-blue-600', 'bg': 'bg-blue-50' },
                { 'title': 'Organisations', 'value': str(total_orgs), 'icon': 'bx bx-buildings', 'color': 'text-red-600', 'bg': 'bg-red-50' },
                { 'title': 'Groupes', 'value': str(total_groups), 'icon': 'bx bx-group', 'color': 'text-amber-600', 'bg': 'bg-amber-50' },
                { 'title': 'Agriculteurs', 'value': str(total_farmers), 'icon': 'bx bx-group', 'color': 'text-emerald-600', 'bg': 'bg-emerald-50' },
                { 'title': 'Parcelles', 'value': str(total_parcels), 'icon': 'bx bx-map', 'color': 'text-purple-600', 'bg': 'bg-purple-50' },
                { 'title': 'Cultures', 'value': str(total_crops), 'icon': 'bx bx-leaf', 'color': 'text-orange-600', 'bg': 'bg-orange-50' },
                { 'title': 'Parcelles-Cultures', 'value': str(total_parcel_crops), 'icon': 'bx bx-collection', 'color': 'text-cyan-600', 'bg': 'bg-cyan-50' },
                { 'title': 'Tâches', 'value': str(total_tasks), 'icon': 'bx bx-check-square', 'color': 'text-rose-600', 'bg': 'bg-rose-50' },
            ],
            'recent_alerts': [
                { 'id': 1, 'type': 'SECURITY', 'message': 'Tentatives de connexion suspectes détectées', 'time': 'Il y a 10 min', 'severity': 'high' },
                { 'id': 2, 'type': 'SYSTEM', 'message': 'Synchronisation météo terminée pour toutes les régions', 'time': 'Il y a 1h', 'severity': 'low' },
            ]
        }


# ══════════════════════════════════════════════════════════════════════════════
# ParcelDataService
# ══════════════════════════════════════════════════════════════════════════════
class ParcelDataService:
    """
    Service de collecte et sérialisation des données d'une parcelle.
    """

    # ── GPS ───────────────────────────────────────────────────────────────────
    @staticmethod
    def get_first_point(parcel: Parcel):
        if not parcel.points or len(parcel.points) == 0:
            raise ValueError('Parcel has no points')
        return parcel.points[0]

    # ── Sol ───────────────────────────────────────────────────────────────────
    @staticmethod
    def fetch_soil(parcel: Parcel, force_refresh=False):
        """Récupère les données sol avec cache 30 jours et fallback."""
        if not force_refresh:
            recent = SoilData.objects.filter(
                parcel=parcel,
                created_at__gte=timezone.now() - timezone.timedelta(days=30),
            ).order_by('-created_at').first()
            if recent and ParcelDataService.has_valid_soil_data(recent):
                print('✅ Utilisation des données sol existantes valides')
                return recent

        print('🔄 Appel API SoilGrids pour nouvelles données...')
        point = ParcelDataService.get_first_point(parcel)
        lat, lon = point['lat'], point['lng']

        url = (
            f'https://rest.isric.org/soilgrids/v2.0/properties/query?'
            f'lon={lon}&lat={lat}&property=phh2o&property=soc&property=nitrogen'
            f'&property=sand&property=clay&property=silt&depth=0-5cm&value=mean'
        )

        try:
            resp = http_requests.get(url, timeout=10)
            if resp.status_code == 200:
                soil_data = resp.json()
                if ParcelDataService.is_soil_data_valid(soil_data):
                    return SoilData.objects.create(parcel=parcel, data=soil_data)
                print('⚠️ Données sol invalides, utilisation des valeurs par défaut')
                return ParcelDataService.create_default_soil_data(parcel, lat, lon)
            print(f'❌ Erreur API SoilGrids: {resp.status_code}')
            return ParcelDataService.get_fallback_soil_data(parcel)
        except http_requests.exceptions.Timeout:
            print('❌ Timeout API SoilGrids')
            return ParcelDataService.get_fallback_soil_data(parcel)
        except Exception as e:
            print(f'❌ Erreur API SoilGrids: {str(e)}')
            return ParcelDataService.get_fallback_soil_data(parcel)

    @staticmethod
    def has_valid_soil_data(soil_data_obj) -> bool:
        if not soil_data_obj or not soil_data_obj.data:
            return False
        for layer in soil_data_obj.data.get('properties', {}).get('layers', []):
            for depth in layer.get('depths', []):
                if depth.get('values', {}).get('mean') is not None:
                    return True
        return False

    @staticmethod
    def is_soil_data_valid(soil_data) -> bool:
        if not soil_data:
            return False
        layers = soil_data.get('properties', {}).get('layers', [])
        valid = sum(
            1 for layer in layers
            for depth in layer.get('depths', [])
            if depth.get('values', {}).get('mean') is not None
        )
        return valid >= len(layers) * 0.5

    @staticmethod
    def create_default_soil_data(parcel, lat, lon):
        default_data = {
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
            'properties': {
                'layers': [
                    {'name': 'clay',     'depths': [{'label': '0-5cm', 'values': {'mean': 25.0}}], 'unit_measure': {'target_units': '%'}},
                    {'name': 'nitrogen', 'depths': [{'label': '0-5cm', 'values': {'mean': 1.2}}],  'unit_measure': {'target_units': 'g/kg'}},
                    {'name': 'phh2o',   'depths': [{'label': '0-5cm', 'values': {'mean': 6.5}}],  'unit_measure': {'target_units': '-'}},
                    {'name': 'sand',    'depths': [{'label': '0-5cm', 'values': {'mean': 40.0}}], 'unit_measure': {'target_units': '%'}},
                    {'name': 'silt',    'depths': [{'label': '0-5cm', 'values': {'mean': 35.0}}], 'unit_measure': {'target_units': '%'}},
                    {'name': 'soc',     'depths': [{'label': '0-5cm', 'values': {'mean': 2.0}}],  'unit_measure': {'target_units': 'g/kg'}},
                ]
            },
            'metadata': {'source': 'default_values', 'region': 'Madagascar'},
        }
        return SoilData.objects.create(parcel=parcel, data=default_data)

    @staticmethod
    def get_fallback_soil_data(parcel):
        existing = SoilData.objects.filter(parcel=parcel).order_by('-created_at').first()
        if existing:
            print('⚠️ Utilisation des données sol existantes (fallback)')
            return existing
        point = ParcelDataService.get_first_point(parcel)
        lat, lon = point['lat'], point['lng']
        print('⚠️ Création de données sol par défaut (fallback)')
        return ParcelDataService.create_default_soil_data(parcel, lat, lon)

    @staticmethod
    def refresh_soil_data(parcel: Parcel):
        return ParcelDataService.fetch_soil(parcel, force_refresh=True)

    # ── Météo ─────────────────────────────────────────────────────────────────
    @staticmethod
    def fetch_weather(parcel: Parcel, required_days: int = 3):
        recent = WeatherData.objects.filter(
            parcel=parcel,
            created_at__gte=timezone.now() - timezone.timedelta(hours=24),
        ).order_by('-created_at').first()

        if recent and ParcelDataService.has_enough_forecast_days(recent, required_days):
            print(f'✅ Données météo existantes ({ParcelDataService.get_forecast_days_count(recent)} jours)')
            return recent

        print('🔄 Appel API météo...')
        from apps.weather.services import WeatherDataCollector
        collector = WeatherDataCollector()
        result = collector.collect_and_save_weather_data(parcel, forecast_days=required_days)

        if result['success']:
            return result.get('weather_data') or WeatherData.objects.filter(parcel=parcel).order_by('-created_at').first()

        print(f'⚠️ Erreur API météo, fallback: {result.get("error")}')
        return recent or WeatherData.objects.create(
            parcel=parcel,
            data={'error': result.get('error', 'unknown')},
            start=timezone.now().date(),
            end=timezone.now().date() + timezone.timedelta(days=required_days - 1),
            location_name='Erreur de collecte',
            data_type='FORECAST',
            risk_level='LOW',
        )

    @staticmethod
    def has_enough_forecast_days(weather_data, required_days: int = 3) -> bool:
        if not weather_data or not weather_data.data:
            return False
        days = weather_data.data.get('forecast', {}).get('forecastday', [])
        return len(days) >= required_days

    @staticmethod
    def get_forecast_days_count(weather_data) -> int:
        if not weather_data or not weather_data.data:
            return 0
        return len(weather_data.data.get('forecast', {}).get('forecastday', []))

    @staticmethod
    def get_weather_analysis(parcel: Parcel):
        weather_data = ParcelDataService.fetch_weather(parcel)
        if not weather_data:
            return None
        from apps.weather.services import AgriculturalAnalyzer
        analyzer = AgriculturalAnalyzer()
        return {
            'weather_data': weather_data,
            'analysis':     analyzer.analyze_weather_data(weather_data),
            'alerts':       weather_data.agricultural_alerts,
            'summary':      weather_data.get_weather_summary(),
        }

    # ── Cultures & tâches ─────────────────────────────────────────────────────
    @staticmethod
    def build_parcel_crops(parcel):
        result = []
        for pc in parcel.parcel_crops.all():
            tasks_info = [
                {
                    'id':           task.id,
                    'name':         task.name,
                    'status':       task.status.name if task.status else None,
                    'due_date':     task.due_date,
                    'priority':     task.priority.name if task.priority else None,
                    'completed_at': task.completed_at,
                }
                for task in pc.task_set.all()
            ]
            result.append({
                'parcel_crop_id': pc.id,
                'crop': {
                    'id':      pc.crop.id,
                    'name':    pc.crop.name,
                    'variety': pc.crop.variety.name if pc.crop.variety else None,
                },
                'planting_date': pc.planting_date,
                'harvest_date':  pc.harvest_date,
                'area':          pc.area,
                'status':        pc.status.name if pc.status else None,
                'tasks':         tasks_info,
            })
        return result

    @staticmethod
    def build_yield_records(parcel):
        records = []
        for pc in parcel.parcel_crops.all():
            for yr in YieldRecord.objects.filter(parcelCrop=pc):
                records.append({
                    'parcel_crop_id': pc.id,
                    'date':  yr.date,
                    'yield': yr.yield_amount,
                    'notes': yr.notes,
                })
        return records

    @staticmethod
    def build_parcel_tasks(parcel):
        tasks = (
            Task.objects.filter(parcelCrop__parcel=parcel)
            .select_related('parcelCrop', 'status', 'priority')
            .order_by('due_date')
        )
        tasks_info = [
            {
                'id':           task.id,
                'name':         task.name,
                'description':  task.description,
                'due_date':     task.due_date,
                'completed_at': task.completed_at,
                'created_at':   task.created_at,
                'updated_at':   task.updated_at,
                'status': {
                    'id':   task.status.id   if task.status   else None,
                    'name': task.status.name if task.status   else None,
                },
                'priority': {
                    'id':   task.priority.id   if task.priority else None,
                    'name': task.priority.name if task.priority else None,
                },
                'parcel_crop': {
                    'id':          task.parcelCrop.id,
                    'crop_name':   task.parcelCrop.crop.name if task.parcelCrop.crop else None,
                    'parcel_name': parcel.parcel_name,
                },
            }
            for task in tasks
        ]
        task_stats = {
            'total':     tasks.count(),
            'completed': tasks.filter(completed_at__isnull=False).count(),
            'pending':   tasks.filter(completed_at__isnull=True).count(),
            'overdue':   tasks.filter(
                completed_at__isnull=True,
                due_date__lt=timezone.now().date()
            ).count(),
            'by_priority': {
                'HIGH':   tasks.filter(priority__name='HIGH').count(),
                'MEDIUM': tasks.filter(priority__name='MEDIUM').count(),
                'LOW':    tasks.filter(priority__name='LOW').count(),
            },
        }
        return {'tasks': tasks_info, 'statistics': task_stats}

    @staticmethod
    def get_tasks_summary(parcel):
        tasks = Task.objects.filter(parcelCrop__parcel=parcel)
        urgent = (
            tasks.filter(
                completed_at__isnull=True,
                due_date__lte=timezone.now().date() + timezone.timedelta(days=3),
            )
            .select_related('parcelCrop', 'priority')
            .order_by('due_date')[:5]
        )
        return {
            'urgent_tasks': [
                {
                    'id':        task.id,
                    'name':      task.name,
                    'due_date':  task.due_date,
                    'priority':  task.priority.name if task.priority else None,
                    'crop_name': task.parcelCrop.crop.name if task.parcelCrop.crop else None,
                    'is_overdue': task.due_date < timezone.now().date(),
                }
                for task in urgent
            ],
            'total_pending': tasks.filter(completed_at__isnull=True).count(),
            'total_overdue': tasks.filter(
                completed_at__isnull=True,
                due_date__lt=timezone.now().date()
            ).count(),
        }

    @staticmethod
    def get_complete_parcel_data(parcel_uuid: str):
        try:
            parcel = Parcel.objects.get(uuid=parcel_uuid)
            return {
                'parcel': {
                    'uuid':       str(parcel.uuid),
                    'name':       parcel.parcel_name,
                    'points':     parcel.points,
                    'created_at': parcel.created_at,
                },
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
    def get_user_parcels_tasks(user):
        all_tasks = []
        for parcel in Parcel.objects.filter(owner=user):
            parcel_tasks = ParcelDataService.build_parcel_tasks(parcel)
            if parcel_tasks['tasks']:
                all_tasks.append({
                    'parcel_name': parcel.parcel_name,
                    'parcel_uuid': str(parcel.uuid),
                    'tasks':       parcel_tasks['tasks'],
                    'statistics':  parcel_tasks['statistics'],
                })
        return all_tasks

    # ── Sérialisation météo (8 jours) ─────────────────────────────────────────
    @staticmethod
    def format_weather_for_agriculture(weather_data_dict):
        if not weather_data_dict or 'weather_data' not in weather_data_dict:
            return None
        weather_obj = weather_data_dict['weather_data']
        if not weather_obj or not weather_obj.data:
            return None

        raw = weather_obj.data
        result = {
            'current': {
                'temperature': raw.get('current', {}).get('temp_c'),
                'humidity':    raw.get('current', {}).get('humidity'),
                'precipitation': raw.get('current', {}).get('precip_mm'),
                'condition':   raw.get('current', {}).get('condition', {}).get('text'),
                'wind_speed':  raw.get('current', {}).get('wind_kph'),
                'feels_like':  raw.get('current', {}).get('feelslike_c'),
                'pressure':    raw.get('current', {}).get('pressure_mb'),
                'visibility':  raw.get('current', {}).get('vis_km'),
                'uv_index':    raw.get('current', {}).get('uv'),
            },
            'daily_forecast': [],
        }
        for day in raw.get('forecast', {}).get('forecastday', [])[:8]:
            d = day.get('day', {})
            result['daily_forecast'].append({
                'date':           day.get('date'),
                'max_temp':       d.get('maxtemp_c'),
                'min_temp':       d.get('mintemp_c'),
                'avg_temp':       d.get('avgtemp_c'),
                'total_precip':   d.get('totalprecip_mm'),
                'chance_of_rain': d.get('daily_chance_of_rain'),
                'condition':      d.get('condition', {}).get('text'),
                'uv_index':       d.get('uv'),
                'max_wind':       d.get('maxwind_kph'),
                'avg_humidity':   d.get('avghumidity'),
                'will_it_rain':   d.get('daily_will_it_rain'),
                'will_it_snow':   d.get('daily_will_it_snow'),
            })
        return result

    @staticmethod
    def get_weather_summary_8_days(weather_data_dict):
        if not weather_data_dict:
            return None
        formatted = ParcelDataService.format_weather_for_agriculture(weather_data_dict)
        if not formatted:
            return None

        daily      = formatted.get('daily_forecast', [])
        max_temps  = [d['max_temp'] for d in daily if d['max_temp'] is not None]
        min_temps  = [d['min_temp'] for d in daily if d['min_temp'] is not None]
        total_rain = sum(d['total_precip'] or 0 for d in daily)
        rainy_days = sum(1 for d in daily if (d['chance_of_rain'] or 0) > 50)

        return {
            'current_conditions': formatted.get('current', {}),
            'forecast_stats': {
                'max_temp':        max(max_temps) if max_temps else None,
                'min_temp':        min(min_temps) if min_temps else None,
                'total_rain':      round(total_rain, 1),
                'rainy_days':      rainy_days,
                'forecast_period': f'{len(daily)} jours',
            },
            'period': '8_jours',
        }

    @staticmethod
    def serialize_weather_data(weather_data_dict):
        if not weather_data_dict:
            return None
        weather_obj = weather_data_dict['weather_data']
        formatted   = ParcelDataService.format_weather_for_agriculture(weather_data_dict)
        summary     = ParcelDataService.get_weather_summary_8_days(weather_data_dict)
        return {
            'data':     formatted,
            'analysis': weather_data_dict.get('analysis', {}),
            'alerts':   weather_data_dict.get('alerts', []),
            'summary':  summary,
            'metadata': {
                'location_name': weather_obj.location_name if weather_obj else None,
                'data_type':     weather_obj.data_type     if weather_obj else None,
                'risk_level':    weather_obj.risk_level    if weather_obj else None,
                'start_date':    weather_obj.start.isoformat()      if weather_obj and weather_obj.start      else None,
                'end_date':      weather_obj.end.isoformat()        if weather_obj and weather_obj.end        else None,
                'created_at':    weather_obj.created_at.isoformat() if weather_obj                            else None,
                'forecast_days': 8,
            },
        }

    @staticmethod
    def serialize_soil_data(soil_data_obj):
        if not soil_data_obj or not soil_data_obj.data:
            return None
        data   = soil_data_obj.data
        layers = data.get('properties', {}).get('layers', [])
        valid  = total = 0
        formatted_layers = []

        for layer in layers:
            for depth in layer.get('depths', []):
                total += 1
                if depth.get('values', {}).get('mean') is not None:
                    valid += 1
            formatted_layers.append({
                'name':         layer.get('name'),
                'depths':       layer.get('depths', []),
                'unit_measure': layer.get('unit_measure', {}),
            })

        pct = (valid / total * 100) if total else 0
        return {
            'data': {
                'type':     data.get('type'),
                'geometry': data.get('geometry'),
                'properties': {
                    'layers': formatted_layers,
                    'data_quality': {
                        'valid_percentage': round(pct, 1),
                        'valid_count':      valid,
                        'total_count':      total,
                        'status': 'good' if pct > 70 else 'poor' if pct > 30 else 'very_poor',
                    },
                },
                'query_time_s': data.get('query_time_s'),
            },
            'metadata': {
                'created_at':        soil_data_obj.created_at.isoformat(),
                'depth':             '0-5cm',
                'source':            data.get('metadata', {}).get('source', 'soilgrids_api'),
                'data_quality_note': ParcelDataService._soil_quality_note(pct),
            },
        }

    @staticmethod
    def _soil_quality_note(pct: float) -> str:
        if pct > 90: return 'Données complètes et fiables'
        if pct > 70: return 'Données majoritairement disponibles'
        if pct > 50: return 'Données partiellement disponibles'
        if pct > 30: return 'Données limitées — valeurs par défaut utilisées'
        return 'Données très limitées — estimations utilisées'
