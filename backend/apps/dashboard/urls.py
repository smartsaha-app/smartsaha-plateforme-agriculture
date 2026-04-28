"""
apps/dashboard/urls.py
-----------------------
Routes disponibles sous /api/v2/ :

    GET   /api/v2/dashboard/full_dashboard/    → DashboardViewSet.full_dashboard
    GET   /api/v2/dashboard/weather_overview/  → DashboardViewSet.weather_overview
    GET   /api/v2/dashboard/enhanced_weather/  → DashboardViewSet.enhanced_weather
    POST  /api/v2/dashboard/refresh_weather/   → DashboardViewSet.refresh_weather

Vue HTML (montée directement dans config/urls.py) :
    GET   /dashboard/                          → dashboard()
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.dashboard.views import DashboardViewSet, dashboard

router = DefaultRouter()
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    # La route HTML /dashboard/ est montée dans config/urls.py car elle
    # n'est pas sous /api/v2/
]