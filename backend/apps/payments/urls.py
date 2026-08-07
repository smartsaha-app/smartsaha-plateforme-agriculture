from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionViewSet,
    initiate_payment,
    payment_webhook,
    create_stripe_payment_intent,
    confirm_stripe_payment_intent,
    stripe_webhook,
    seller_stats,
    request_subscription_upgrade,
    my_subscription,
    create_subscription_stripe_intent,
    confirm_subscription_stripe_intent
)

router = DefaultRouter()
router.register(r'history', TransactionViewSet, basename='payment-history')

urlpatterns = [
    path('initiate/', initiate_payment, name='payment-initiate'),
    path('confirm/', payment_webhook, name='payment-confirm'),
    path('stripe/create-payment-intent/', create_stripe_payment_intent, name='stripe-create-payment-intent'),
    path('stripe/confirm-payment-intent/', confirm_stripe_payment_intent, name='stripe-confirm-payment-intent'),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
    path('seller-stats/', seller_stats, name='seller-stats'),
    path('subscription-request/', request_subscription_upgrade, name='subscription-request'),
    path('my-subscription/', my_subscription, name='my-subscription'),
    path('subscription-payment-intent/', create_subscription_stripe_intent, name='subscription-payment-intent'),
    path('subscription-confirm-stripe/', confirm_subscription_stripe_intent, name='subscription-confirm-stripe'),
    path('', include(router.urls)),
]
