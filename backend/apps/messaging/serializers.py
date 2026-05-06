from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    """Version allégée de l'utilisateur pour la messagerie."""
    class Meta:
        model = User
        fields = ['uuid', 'username', 'first_name', 'last_name']

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    is_me = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['uuid', 'conversation', 'sender', 'sender_name', 'content', 'is_read', 'is_me', 'created_at']
        read_only_fields = ['uuid', 'sender', 'is_read', 'created_at']

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_me(self, obj):
        request = self.context.get('request')
        if request:
            return obj.sender == request.user
        return False

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSimpleSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    related_post_name = serializers.CharField(source='related_post.name', read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'uuid', 'participants', 'related_post', 'related_post_name', 
            'last_message', 'unread_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'participants', 'created_at', 'updated_at']

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg, context=self.context).data
        return None

    @extend_schema_field(OpenApiTypes.INT)
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0
