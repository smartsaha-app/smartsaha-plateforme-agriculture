from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from ..models import Indicator, IndicatorValue, IndicatorCategory
from ..serializers.indicators import IndicatorSerializer, IndicatorValueSerializer, IndicatorCategorySerializer

@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation']),
    retrieve=extend_schema(tags=['Suivi & Évaluation']),
    create=extend_schema(tags=['Suivi & Évaluation']),
    update=extend_schema(tags=['Suivi & Évaluation']),
    partial_update=extend_schema(tags=['Suivi & Évaluation']),
    destroy=extend_schema(tags=['Suivi & Évaluation']),
)
class IndicatorCategoryViewSet(viewsets.ModelViewSet):
    queryset = IndicatorCategory.objects.all()
    serializer_class = IndicatorCategorySerializer

@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation']),
    retrieve=extend_schema(tags=['Suivi & Évaluation']),
    create=extend_schema(tags=['Suivi & Évaluation']),
    update=extend_schema(tags=['Suivi & Évaluation']),
    partial_update=extend_schema(tags=['Suivi & Évaluation']),
    destroy=extend_schema(tags=['Suivi & Évaluation']),
)
class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer


@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation']),
    retrieve=extend_schema(tags=['Suivi & Évaluation']),
    create=extend_schema(tags=['Suivi & Évaluation']),
    update=extend_schema(tags=['Suivi & Évaluation']),
    partial_update=extend_schema(tags=['Suivi & Évaluation']),
    destroy=extend_schema(tags=['Suivi & Évaluation']),
)
class IndicatorValueViewSet(viewsets.ModelViewSet):
    queryset = IndicatorValue.objects.all()
    serializer_class = IndicatorValueSerializer
