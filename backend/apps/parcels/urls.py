from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.parcels.views import ParcelViewSet, ParcelPointViewSet

router = DefaultRouter()
router.register(r'parcels',       ParcelViewSet,      basename='parcel')
router.register(r'parcel-points', ParcelPointViewSet, basename='parcel-point')

urlpatterns = [
    path('', include(router.urls)),
]