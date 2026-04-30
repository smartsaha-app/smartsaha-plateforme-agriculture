"""
apps/yields/serializers.py
--------------------------
Serializers pour YieldRecord et YieldForecast.
"""
from rest_framework import serializers
from apps.yields.models import YieldRecord, YieldForecast


class YieldRecordSerializer(serializers.ModelSerializer):
    # ✅ CORRIGÉ : la méthode yield_per_area() est maintenant définie sur le modèle
    yield_per_area = serializers.SerializerMethodField()

    class Meta:
        model = YieldRecord
        fields = '__all__'

    def get_yield_per_area(self, obj):
        return obj.yield_per_area()


class YieldForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldForecast
        fields = [
            'id', 'parcelCrop', 'forecast_date',
            'predicted_yield', 'created_at',
        ]
        read_only_fields = ['created_at']