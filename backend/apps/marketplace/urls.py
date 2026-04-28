from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.marketplace.views import PostViewSet, CartViewSet, OrderViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='marketplace-post')
router.register(r'cart', CartViewSet, basename='marketplace-cart')
router.register(r'orders', OrderViewSet, basename='marketplace-order')
router.register(r'reviews', ReviewViewSet, basename='marketplace-review')

urlpatterns = [
    path('', include(router.urls)),
]
