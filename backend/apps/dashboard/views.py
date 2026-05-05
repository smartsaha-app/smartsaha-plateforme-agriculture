"""
apps/dashboard/views.py
------------------------
Migré depuis SmartSaha/views/dashboard.py.
Tous les imports pointent vers apps/ au lieu de SmartSaha/.
"""
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Avg, Sum
from django.db.models.functions import ExtractYear
from django.shortcuts import render
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import openpyxl

from apps.marketplace.models import Product, Order

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.crops.models import Crop, ParcelCrop  # ParcelCrop et Crop sont dans apps.crops
from apps.parcels.models import Parcel
from apps.weather.models import ClimateData
from apps.yields.models import YieldForecast, YieldRecord

from apps.dashboard.services import DashboardService


# ──────────────────────────────────────────────────────────────────────────────
# DashboardViewSet — API REST
# ──────────────────────────────────────────────────────────────────────────────
@swagger_auto_schema(tags=['Tableau de bord'])
class DashboardViewSet(viewsets.ViewSet):
    """
    GET /api/v2/dashboard/full_dashboard/
    Retourne le dashboard complet pour l'utilisateur connecté (cache 30 min).
    """

    @swagger_auto_schema(
        operation_summary="Dashboard complet",
        tags=['Tableau de bord'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['get'])
    def full_dashboard(self, request):
        user = request.user
        cache_key = f'dashboard_full_{user.pk}'
        data = cache.get(cache_key)
        if not data:
            data = DashboardService(user).get_full_dashboard()
            cache.set(cache_key, data, timeout=1800)
        return Response(data)

    @swagger_auto_schema(
        operation_summary="Résumé météo compact",
        tags=['Tableau de bord'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['get'])
    def weather_overview(self, request):
        """GET /api/v2/dashboard/weather_overview/ -- Vue meteo compacte."""
        from django.conf import settings
        cache_key = f'dashboard_weather_{request.user.pk}'
        data = cache.get(cache_key)
        if not data:
            data = DashboardService(request.user).get_dashboard_weather_overview()
            cache.set(cache_key, data, timeout=getattr(settings, 'CACHE_TTL_WEATHER', 600))
        return Response(data)

    @swagger_auto_schema(
        operation_summary="Analyse météo enrichie",
        tags=['Tableau de bord'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['get'])
    def enhanced_weather(self, request):
        """GET /api/v2/dashboard/enhanced_weather/ -- Analyse meteo enrichie."""
        from django.conf import settings
        cache_key = f'dashboard_enhanced_weather_{request.user.pk}'
        data = cache.get(cache_key)
        if not data:
            data = DashboardService(request.user).get_enhanced_weather_summary()
            cache.set(cache_key, data, timeout=getattr(settings, 'CACHE_TTL_WEATHER', 600))
        return Response(data)

    @swagger_auto_schema(
        operation_summary="Forcer le rafraîchissement météo",
        tags=['Tableau de bord'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['get'])
    def refresh_weather(self, request):
        """POST /api/v2/dashboard/refresh_weather/ — Force le rafraîchissement météo."""
        results = DashboardService(request.user).refresh_weather_data()
        return Response({'results': results, 'count': len(results)})

    @swagger_auto_schema(
        operation_summary="Données BI Organisation",
        tags=['Tableau de bord'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['get'])
    def bi_dashboard(self, request):
        """GET /api/v2/dashboard/bi_dashboard/ -- Donnees pour l'espace organisation."""
        from django.conf import settings
        timeframe = request.query_params.get('timeframe', 'annee')
        if timeframe not in ('annee', 'mois'):
            timeframe = 'annee'
        cache_key = f'dashboard_bi_{request.user.pk}_{timeframe}'
        data = cache.get(cache_key)
        if not data:
            data = DashboardService(request.user).get_bi_dashboard_data(timeframe=timeframe)
            cache.set(cache_key, data, timeout=getattr(settings, 'CACHE_TTL_DASHBOARD', 300))
        return Response(data)

    @swagger_auto_schema(
        operation_summary="Données Admin Superviseur",
        tags=['Tableau de bord'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['get'])
    def admin_dashboard(self, request):
        """GET /api/v2/dashboard/admin_dashboard/ -- Donnees pour l'espace superviseur."""
        from django.conf import settings
        cache_key = f'dashboard_admin_{request.user.pk}'
        data = cache.get(cache_key)
        if not data:
            data = DashboardService(request.user).get_admin_dashboard_data()
            cache.set(cache_key, data, timeout=getattr(settings, 'CACHE_TTL_DASHBOARD', 300))
        return Response(data)

    @swagger_auto_schema(
        operation_summary="Statistiques Marketplace",
        tags=['Tableau de bord'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT)}
    )
    @action(detail=False, methods=['get'])
    def marketplace_stats(self, request):
        """GET /api/v2/dashboard/marketplace_stats/ -- Volume marketplace et vendeurs actifs."""
        active_sellers = Product.objects.values('seller').distinct().count()
        total_posts = Product.objects.count()
        total_orders = Order.objects.count()
        delivered_orders = Order.objects.filter(status='DELIVERED').count()
        
        volume = Order.objects.filter(status='DELIVERED').aggregate(Sum('total_price'))['total_price__sum'] or 0

        data = {
            'active_sellers': active_sellers,
            'total_posts': total_posts,
            'total_orders': total_orders,
            'delivered_orders': delivered_orders,
            'marketplace_volume': volume,
        }
        return Response(data)

    @swagger_auto_schema(
        operation_summary="Export Excel Rapports Admin",
        tags=['Tableau de bord']
    )
    @action(detail=False, methods=['get'])
    def export_marketplace_report(self, request):
        """GET /api/v2/dashboard/export_marketplace_report/ -- Export openpyxl."""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Marketplace Report"

        # Headers
        headers = ["ID Commande", "Acheteur", "Vendeur", "Statut", "Total"]
        ws.append(headers)

        orders = Order.objects.select_related('buyer', 'seller').all()
        for order in orders:
            ws.append([
                str(order.uuid),
                order.buyer.username,
                order.seller.username,
                order.status,
                float(order.total_price)
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=marketplace_report.xlsx'
        wb.save(response)
        return response


# ──────────────────────────────────────────────────────────────────────────────
# dashboard() — Vue HTML template
# ──────────────────────────────────────────────────────────────────────────────
@login_required(login_url='login')
def dashboard(request):
    """
    GET /dashboard/
    Rend le template dashboard.html avec toutes les données agrégées.
    """
    all_parcels = Parcel.objects.all()
    service = DashboardService(user=request.user)
    dashboard_data = service.get_full_dashboard()

    # Rendement total
    rendement_total = sum(
        y['summary']['total_yield']
        for y in dashboard_data['yield_summary']
        if y['summary']
    )

    # Liste des parcelles pour le template
    parcelles = []
    for parcel in all_parcels:
        last_pc = (
            ParcelCrop.objects.filter(parcel=parcel)
            .order_by('-created_at')
            .first()
        )
        culture_name = last_pc.crop.name if last_pc and last_pc.crop else 'N/A'
        superficie = last_pc.area if last_pc else 0

        rendement_par_parcelle = (
            YieldRecord.objects.filter(parcelCrop__parcel=parcel)
            .aggregate(total=Sum('yield_amount'))['total'] or 0
        )

        parcelles.append({
            'id':         parcel.uuid,
            'nom':        parcel.parcel_name,
            'culture':    culture_name,
            'superficie': superficie,
            'rendement':  rendement_par_parcelle,
        })

    # Prévision (moyenne des YieldForecast existants)
    prevision = int(YieldForecast.objects.aggregate(avg=Avg('predicted_yield'))['avg'] or 0)

    # Utilisateur
    user = request.user if request.user.is_authenticated else None
    user_display = user.username if user else 'Invité'
    avatar_url = (
        f'https://ui-avatars.com/api/?name={user_display}&background=10b981&color=ffffff&size=64'
    )

    # Cultures pour le modal
    crops = list(Crop.objects.values_list('name', flat=True))

    # Filtres statistiques
    parcel_names = list(all_parcels.values_list('parcel_name', flat=True))
    years = list(
        YieldRecord.objects.annotate(y=ExtractYear('date'))
        .order_by('y')
        .values_list('y', flat=True)
        .distinct()
    )

    # Graphique des 6 derniers mois
    today = timezone.now().date()
    month_labels, month_values = [], []
    for i in range(5, -1, -1):
        year = today.year if today.month - i > 0 else today.year - 1
        month = ((today.month - i - 1) % 12) + 1
        label = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'][month - 1]
        month_labels.append(label)
        total = (
            YieldRecord.objects
            .filter(date__year=year, date__month=month)
            .aggregate(s=Sum('yield_amount'))['s'] or 0
        )
        month_values.append(total)

    # Données météo depuis ClimateData
    temp_max, temp_min, precip = [], [], []
    days_labels = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    latest_climate = ClimateData.objects.order_by('-created_at').first()
    if latest_climate and isinstance(latest_climate.data, dict):
        d = latest_climate.data
        temp_max = list(d.get('temperature_max', [])[:7])
        temp_min = list(d.get('temperature_min', [])[:7])
        precip = list(d.get('precipitations', [])[:7])

    context = {
        'parcelles':       parcelles,
        'rendement_total': rendement_total,
        'prevision':       prevision,
        'user_display':    user_display,
        'avatar_url':      avatar_url,
        'crops':           crops,
        'parcel_names':    parcel_names,
        'years':           years,
        'stats_labels':    month_labels,
        'stats_values':    month_values,
        'temp_labels':     days_labels,
        'temp_max':        temp_max,
        'temp_min':        temp_min,
        'rain_labels':     days_labels,
        'rain_values':     precip,
        'dashboard':       dashboard_data,
    }

    return render(request, 'dashboard.html', context)