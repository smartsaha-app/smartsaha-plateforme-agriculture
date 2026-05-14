from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, initiate_payment, payment_webhook, seller_stats

router = DefaultRouter()
# /api/mobile/payments/history/ and /status/{txn_id}/ can be handled by this ViewSet
router.register(r'history', TransactionViewSet, basename='payment-history')

urlpatterns = [
    path('initiate/', initiate_payment, name='payment-initiate'),
    path('confirm/', payment_webhook, name='payment-confirm'),
    path('seller-stats/', seller_stats, name='seller-stats'),
    
    # history/ maps to the Viewset's list
    # history/{id}/ maps to Viewset's retrieve -> acts as status/{id}/
    path('', include(router.urls)),
]
