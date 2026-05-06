from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.weather.views import (
    WeatherDataViewSet, AgriculturalAlertViewSet,
    WeatherCollectionViewSet, AlertViewSet,
    SoilDataView, ClimateDataView,
)

router = DefaultRouter()
router.register(r'weather-data',         WeatherDataViewSet,       basename='weather-data')
router.register(r'agricultural-alerts',   AgriculturalAlertViewSet, basename='agricultural-alert')
router.register(r'weather-collection',    WeatherCollectionViewSet, basename='weather-collection')
router.register(r'alerts',               AlertViewSet,             basename='alert')

urlpatterns = [
    path('', include(router.urls)),
    path('soil-data/',    SoilDataView.as_view(),    name='soil-data'),
    path('climate-data/', ClimateDataView.as_view(), name='climate-data'),
]
