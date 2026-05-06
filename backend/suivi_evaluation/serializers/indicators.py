from rest_framework import serializers
from suivi_evaluation.models import Indicator, IndicatorValue, IndicatorCategory

from django.contrib.auth import get_user_model

User = get_user_model()

class IndicatorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorCategory
        fields = '__all__'

class IndicatorSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Indicator
        fields = '__all__'

class IndicatorValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorValue
        fields = '__all__'
