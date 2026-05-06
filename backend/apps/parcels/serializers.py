"""
apps/parcels/serializers.py
---------------------------
Serializers pour Parcel et ParcelPoint.
"""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from apps.parcels.models import Parcel, ParcelPoint


class ParcelPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelPoint
        fields = ['latitude', 'longitude', 'order']


class ParcelSerializer(serializers.ModelSerializer):
    parcel_points      = ParcelPointSerializer(many=True)
    has_gps_points     = serializers.SerializerMethodField()
    points_count       = serializers.SerializerMethodField()
    center_coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = [
            'uuid', 'owner', 'parcel_name', 'points', 'parcel_points',
            'created_at', 'updated_at',
            'has_gps_points', 'points_count', 'center_coordinates',
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']

    # Utilise les méthodes du proxy → plus de duplication
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_has_gps_points(self, obj):
        return obj.has_gps_points()

    @extend_schema_field(OpenApiTypes.INT)
    def get_points_count(self, obj):
        return len(obj.points) if obj.points and isinstance(obj.points, list) else 0

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_center_coordinates(self, obj):
        return obj.get_center()

    def create(self, validated_data):
        points_data = validated_data.pop('parcel_points', [])
        parcel = Parcel.objects.create(**validated_data)
        for point_data in points_data:
            ParcelPoint.objects.create(parcel=parcel, **point_data)
        parcel.points = [{'lat': p['latitude'], 'lng': p['longitude']} for p in points_data]
        parcel.save()
        return parcel

    def update(self, instance, validated_data):
        points_data = validated_data.pop('parcel_points', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if points_data is not None:
            instance.parcel_points.all().delete()
            for point_data in points_data:
                ParcelPoint.objects.create(parcel=instance, **point_data)
            instance.points = [{'lat': p['latitude'], 'lng': p['longitude']} for p in points_data]
            instance.save()
        return instance


class ParcelWeatherSerializer(serializers.ModelSerializer):
    """Serializer léger pour l'API météo — uniquement les infos GPS."""
    center_coordinates = serializers.SerializerMethodField()
    points_count       = serializers.SerializerMethodField()

    class Meta:
        model = Parcel
        fields = ['uuid', 'parcel_name', 'points_count', 'center_coordinates']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_center_coordinates(self, obj):
        return obj.get_center()

    @extend_schema_field(OpenApiTypes.INT)
    def get_points_count(self, obj):
        return len(obj.points) if obj.points and isinstance(obj.points, list) else 0
