from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Indicator, IndicatorValue, IndicatorCategory
from ..serializers.indicators import IndicatorSerializer, IndicatorValueSerializer, IndicatorCategorySerializer

@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class IndicatorCategoryViewSet(viewsets.ModelViewSet):
    queryset = IndicatorCategory.objects.all()
    serializer_class = IndicatorCategorySerializer

@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class IndicatorValueViewSet(viewsets.ModelViewSet):
    queryset = IndicatorValue.objects.all()
    serializer_class = IndicatorValueSerializer
