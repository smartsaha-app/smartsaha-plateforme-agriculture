from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Report, ReportData, ReportAttachment
from ..serializers.reporting import (
    ReportSerializer, ReportDataSerializer, ReportAttachmentSerializer
)

from ..services.reporting import ReportGenerator

@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer

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


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class ReportDataViewSet(viewsets.ModelViewSet):
    queryset = ReportData.objects.all()
    serializer_class = ReportDataSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='create', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['Suivi & Évaluation']))
class ReportAttachmentViewSet(viewsets.ModelViewSet):
    queryset = ReportAttachment.objects.all()
    serializer_class = ReportAttachmentSerializer
