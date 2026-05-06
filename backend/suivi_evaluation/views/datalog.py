from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from ..models import DataLog, CustomField, CustomFieldValue
from ..serializers.datalog import (
    DataLogSerializer,
    CustomFieldSerializer,
    CustomFieldValueSerializer
)

@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation']),
    retrieve=extend_schema(tags=['Suivi & Évaluation']),
    create=extend_schema(tags=['Suivi & Évaluation']),
    update=extend_schema(tags=['Suivi & Évaluation']),
    partial_update=extend_schema(tags=['Suivi & Évaluation']),
    destroy=extend_schema(tags=['Suivi & Évaluation']),
)
class DataLogViewSet(viewsets.ModelViewSet):
    """
    Gère les journaux de données (création, modification, suppression)
    """
    queryset = DataLog.objects.all()
    serializer_class = DataLogSerializer


@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation']),
    retrieve=extend_schema(tags=['Suivi & Évaluation']),
    create=extend_schema(tags=['Suivi & Évaluation']),
    update=extend_schema(tags=['Suivi & Évaluation']),
    partial_update=extend_schema(tags=['Suivi & Évaluation']),
    destroy=extend_schema(tags=['Suivi & Évaluation']),
)
class CustomFieldViewSet(viewsets.ModelViewSet):
    """
    Gère la définition des champs personnalisés dynamiques
    """
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer


@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation']),
    retrieve=extend_schema(tags=['Suivi & Évaluation']),
    create=extend_schema(tags=['Suivi & Évaluation']),
    update=extend_schema(tags=['Suivi & Évaluation']),
    partial_update=extend_schema(tags=['Suivi & Évaluation']),
    destroy=extend_schema(tags=['Suivi & Évaluation']),
)
class CustomFieldValueViewSet(viewsets.ModelViewSet):
    """
    Gère les valeurs associées aux champs personnalisés
    """
    queryset = CustomFieldValue.objects.all()
    serializer_class = CustomFieldValueSerializer
