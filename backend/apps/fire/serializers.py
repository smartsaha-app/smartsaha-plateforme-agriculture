"""
apps/fire/serializers.py
------------------------
Serializers pour FireAlert.
"""
from rest_framework import serializers
from apps.fire.models import FireAlert


class FireAlertSerializer(serializers.ModelSerializer):
    parcel_name  = serializers.CharField(source='parcel.parcel_name', read_only=True, default=None)
    owner_email  = serializers.CharField(source='parcel.owner.email', read_only=True, default=None)
    severity_label = serializers.SerializerMethodField()

    class Meta:
        model  = FireAlert
        fields = [
            'uuid',
            'latitude', 'longitude',
            'brightness', 'confidence',
            'acq_date', 'acq_time', 'satellite', 'source',
            'parcel', 'parcel_name', 'owner_email',
            'distance_km',
            'severity', 'severity_label',
            'is_active', 'is_notified',
            'created_at',
        ]
        read_only_fields = fields

    def get_severity_label(self, obj) -> str:
        labels = {
            'CRITICAL': '🔴 Critique',
            'HIGH':     '🟠 Élevé',
            'MEDIUM':   '🟡 Moyen',
        }
        return labels.get(obj.severity, obj.severity)


class FireAlertSummarySerializer(serializers.Serializer):
    """Résumé statistique des alertes feu actives."""
    total_active          = serializers.IntegerField()
    critical_count        = serializers.IntegerField()
    high_count            = serializers.IntegerField()
    medium_count          = serializers.IntegerField()
    parcels_at_risk_count = serializers.IntegerField()
    last_update           = serializers.DateField()
    recent_alerts         = FireAlertSerializer(many=True)
