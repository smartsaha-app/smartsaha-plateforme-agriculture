from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import CertificationType, Certification, CertificationAudit
from ..serializers.evaluation import (
    CertificationTypeSerializer, CertificationSerializer, CertificationAuditSerializer
)

@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class CertificationTypeViewSet(viewsets.ModelViewSet):
    queryset = CertificationType.objects.all()
    serializer_class = CertificationTypeSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class CertificationAuditViewSet(viewsets.ModelViewSet):
    queryset = CertificationAudit.objects.all()
    serializer_class = CertificationAuditSerializer


# class ParcelEvaluationViewSet(viewsets.ModelViewSet):
#     """
#     Gère les évaluations des parcelles (risques, productivité, etc.)
#     """
#     queryset = ParcelEvaluation.objects.all()
#     serializer_class = ParcelEvaluationSerializer
#
#
# class GeoLayerViewSet(viewsets.ModelViewSet):
#     """
#     Gère les couches géographiques (région, district, commune, etc.)
#     """
#     queryset = GeoLayer.objects.all()
#     serializer_class = GeoLayerSerializer

