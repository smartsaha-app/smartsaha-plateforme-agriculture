"""
apps/crops/serializers.py
-------------------------
Serializers pour Crop, Variety, StatusCrop, ParcelCrop.
"""
from rest_framework import serializers

from apps.crops.models import Variety, StatusCrop, Crop, ParcelCrop
from apps.parcels.models import Parcel


class VarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Variety
        fields = '__all__'


class StatusCropSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusCrop
        fields = '__all__'


class CropSerializer(serializers.ModelSerializer):
    variety = VarietySerializer(read_only=True)
    variety_id = serializers.PrimaryKeyRelatedField(
        queryset=Variety.objects.all(),
        source='variety',
        write_only=True,
        required=False
    )
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Crop
        fields = ['id', 'name', 'variety', 'variety_id', 'created_at', 'display_name']

    def get_display_name(self, obj):
        return obj.get_display_name()


class ParcelCropSerializer(serializers.ModelSerializer):
    parcel = serializers.PrimaryKeyRelatedField(queryset=Parcel.objects.all())
    crop = CropSerializer(read_only=True)
    crop_id = serializers.PrimaryKeyRelatedField(
        queryset=Crop.objects.all(),
        source='crop',
        write_only=True
    )
    status = StatusCropSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=StatusCrop.objects.all(),
        source='status',
        write_only=True,
        required=False
    )
    is_active = serializers.SerializerMethodField()
    days_until_harvest = serializers.SerializerMethodField()

    class Meta:
        model = ParcelCrop
        fields = [
            'id', 'parcel', 'crop', 'crop_id',
            'planting_date', 'harvest_date', 'area',
            'status', 'status_id', 'created_at',
            'is_active', 'days_until_harvest',
        ]

    def get_is_active(self, obj):
        return obj.is_active()

    def get_days_until_harvest(self, obj):
        return obj.days_until_harvest()