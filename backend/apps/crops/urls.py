from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.crops.views import CropViewSet, VarietyViewSet, StatusCropViewSet, ParcelCropViewSet

router = DefaultRouter()
router.register(r'crops',        CropViewSet,       basename='crop')
router.register(r'varieties',    VarietyViewSet,    basename='variety')
router.register(r'status-crops', StatusCropViewSet, basename='status-crop')
router.register(r'parcel-crops', ParcelCropViewSet, basename='parcel-crop')

urlpatterns = [
    path('', include(router.urls)),
]
