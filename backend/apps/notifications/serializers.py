from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Notification
        fields = ['uuid', 'notification_type', 'title', 'body', 'is_read', 'data', 'created_at']
        read_only_fields = ['uuid', 'created_at']
