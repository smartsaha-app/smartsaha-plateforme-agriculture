from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from apps.weather.models import WeatherData, AgriculturalAlert, Alert


class WeatherDataSerializer(serializers.ModelSerializer):
    parcel_name         = serializers.CharField(source='parcel.parcel_name', read_only=True)
    risk_analysis       = serializers.SerializerMethodField()
    agricultural_summary = serializers.SerializerMethodField()
    current_temperature = serializers.FloatField(read_only=True)
    total_precipitation = serializers.FloatField(read_only=True)

    class Meta:
        model = WeatherData
        fields = [
            'id', 'parcel_name', 'start', 'end', 'data_type', 'risk_level',
            'current_temperature', 'total_precipitation',
            'risk_analysis', 'agricultural_summary', 'created_at',
        ]

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_risk_analysis(self, obj):
        
        from apps.weather.services import AgriculturalAnalyzer  # ← import local anti-circulaire

        return AgriculturalAnalyzer().analyze_risks(obj.data)

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_agricultural_summary(self, obj):
        return {
            'alerts_count':              len(obj.agricultural_alerts),
            'optimal_planting_days':     obj.optimal_planting_days,
            'irrigation_recommendation': obj.irrigation_recommendation,
        }


class AgriculturalAlertSerializer(serializers.ModelSerializer):
    weather_data_id = serializers.IntegerField(source='weather_data.id', read_only=True)
    parcel_name     = serializers.CharField(source='weather_data.parcel.parcel_name', read_only=True)

    class Meta:
        model = AgriculturalAlert
        fields = [
            'id', 'alert_type', 'message', 'recommendation', 'severity',
            'alert_date', 'is_active', 'weather_data_id', 'parcel_name',
        ]


class AlertSerializer(serializers.ModelSerializer):
    parcel_name = serializers.CharField(source='parcel.parcel_name', read_only=True)
    
    is_critical = serializers.SerializerMethodField()  # ← NOUVEAU


    class Meta:
        model = Alert
        fields = [
            'id', 'parcel', 'parcel_name', 'type', 'message',
            'severity', 'action', 'is_read', 'is_critical',
            'created_at', 'alert_date',
        ]

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_critical(self, obj):
        return obj.is_critical()
