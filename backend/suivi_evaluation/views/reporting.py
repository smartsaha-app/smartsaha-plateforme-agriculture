from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view
from ..models import Report, ReportData, ReportAttachment
from ..serializers.reporting import (
    ReportSerializer, ReportDataSerializer, ReportAttachmentSerializer
)

from ..services.reporting import ReportGenerator

@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    retrieve=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    create=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    update=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    partial_update=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    destroy=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
)
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        # Save the report first to get a UUID
        report = serializer.save(created_by=self.request.user)
        # Trigger data aggregation
        try:
            generator = ReportGenerator(report)
            generator.generate()
        except Exception as e:
            # Optionally log error or update status to ERROR
            print(f"Error generating report: {e}")
            report.status = Report.ReportStatus.DRAFT # Or add an ERROR status
            report.save()


@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    retrieve=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    create=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    update=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    partial_update=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    destroy=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
)
class ReportDataViewSet(viewsets.ModelViewSet):
    queryset = ReportData.objects.all()
    serializer_class = ReportDataSerializer


@extend_schema_view(
    list=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    retrieve=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    create=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    update=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    partial_update=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
    destroy=extend_schema(tags=['Suivi & Évaluation (Reporting)']),
)
class ReportAttachmentViewSet(viewsets.ModelViewSet):
    queryset = ReportAttachment.objects.all()
    serializer_class = ReportAttachmentSerializer
    parser_classes = [MultiPartParser, FormParser]
