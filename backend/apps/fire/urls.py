"""
apps/fire/urls.py
-----------------
Routes :
  GET  /api/fire/alerts/              → liste alertes actives
  GET  /api/fire/alerts/summary/      → stats globales
  GET  /api/fire/alerts/my_parcels/   → alertes pour mes parcelles (auth)
  POST /api/fire/alerts/refresh/      → pipeline FIRMS (admin)
  POST /api/fire/alerts/{uuid}/dismiss/ → ignorer une alerte
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.fire.views import FireAlertViewSet

router = DefaultRouter()
router.register(r'fire/alerts', FireAlertViewSet, basename='fire-alert')

urlpatterns = [
    path('', include(router.urls)),
]
