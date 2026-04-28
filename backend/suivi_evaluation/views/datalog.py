from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import DataLog, CustomField, CustomFieldValue
from ..serializers.datalog import (
    DataLogSerializer,
    CustomFieldSerializer,
    CustomFieldValueSerializer
)

@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class DataLogViewSet(viewsets.ModelViewSet):
    """
    Gère les journaux de données (création, modification, suppression)
    """
    queryset = DataLog.objects.all()
    serializer_class = DataLogSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class CustomFieldViewSet(viewsets.ModelViewSet):
    """
    Gère la définition des champs personnalisés dynamiques
    """
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class CustomFieldValueViewSet(viewsets.ModelViewSet):
    """
    Gère les valeurs associées aux champs personnalisés
    """
    queryset = CustomFieldValue.objects.all()
    serializer_class = CustomFieldValueSerializer
