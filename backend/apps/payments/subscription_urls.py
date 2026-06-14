from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionAdminViewSet

router = DefaultRouter()
router.register(r'', SubscriptionAdminViewSet, basename='subscription-admin')

urlpatterns = [
    path('', include(router.urls)),
]
