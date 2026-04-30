from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.yields.views import YieldRecordViewSet, YieldForecastView, YieldAnalyticsView

router = DefaultRouter()
router.register(r'yield-records', YieldRecordViewSet, basename='yield-record')

urlpatterns = [
    
    # Prévision ML pour une ParcelCrop
    path('forecast/<int:parcel_crop_id>/', YieldForecastView.as_view(), name='yield-forecast'),
    # Statistiques agrégées
    path('analytics/yields/',             YieldAnalyticsView.as_view(), name='yield-analytics'),

    path('', include(router.urls)),
]