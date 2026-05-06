from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view
from ..models import CertificationType, Certification, CertificationAudit
from ..serializers.evaluation import (
    CertificationTypeSerializer, CertificationSerializer, CertificationAuditSerializer
)

@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    retrieve=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    create=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    update=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    partial_update=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    destroy=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
)
class CertificationTypeViewSet(viewsets.ModelViewSet):
    queryset = CertificationType.objects.all()
    serializer_class = CertificationTypeSerializer


@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    retrieve=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    create=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    update=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    partial_update=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    destroy=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
)
class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    parser_classes = [MultiPartParser, FormParser]


@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    retrieve=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    create=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    update=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    partial_update=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
    destroy=extend_schema(tags=['Suivi & Évaluation (Évaluation)']),
)
class CertificationAuditViewSet(viewsets.ModelViewSet):
    queryset = CertificationAudit.objects.all()
    serializer_class = CertificationAuditSerializer
    parser_classes = [MultiPartParser, FormParser]


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

