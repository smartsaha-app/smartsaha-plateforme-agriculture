from rest_framework import serializers
from suivi_evaluation.models import Report, ReportData, ReportAttachment


class ReportDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportData
        fields = '__all__'


class ReportAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportAttachment
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    data = ReportDataSerializer(many=True, read_only=True)
    attachments = ReportAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = [
            'uuid', 'name', 'type', 'period_start', 'period_end',
            'status', 'organisation_id', 'created_by', 'updated_by',
            'created_at', 'data', 'attachments'
        ]
        read_only_fields = ['uuid', 'status', 'created_at']
