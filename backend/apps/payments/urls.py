from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, initiate_payment, payment_webhook, seller_stats, request_subscription_upgrade, my_subscription

router = DefaultRouter()
router.register(r'history', TransactionViewSet, basename='payment-history')

urlpatterns = [
    path('initiate/', initiate_payment, name='payment-initiate'),
    path('confirm/', payment_webhook, name='payment-confirm'),
    path('seller-stats/', seller_stats, name='seller-stats'),
    path('subscription-request/', request_subscription_upgrade, name='subscription-request'),
    path('my-subscription/', my_subscription, name='my-subscription'),
    path('', include(router.urls)),
]
