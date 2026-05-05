from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.marketplace.views import CategoryViewSet, ProductViewSet, CartViewSet, OrderViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='marketplace-category')
router.register(r'products', ProductViewSet, basename='marketplace-product')
router.register(r'cart', CartViewSet, basename='marketplace-cart')
router.register(r'orders', OrderViewSet, basename='marketplace-order')
router.register(r'reviews', ReviewViewSet, basename='marketplace-review')

urlpatterns = [
    path('', include(router.urls)),
]
