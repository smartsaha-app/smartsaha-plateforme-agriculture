from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KYCViewSet, KYCAdminViewSet

router = DefaultRouter()
router.register(r'documents', KYCViewSet, basename='kyc')
router.register(r'admin', KYCAdminViewSet, basename='kyc-admin')

urlpatterns = [
    path('', include(router.urls)),
]
