"""
apps/chatbot/admin.py
---------------------
Administration des modèles de chat pour le dashboard admin Django.
"""
from django.contrib import admin
from apps.chatbot.models import ChatSession, ChatMessage, ChatFeedback


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('role', 'content', 'metadata', 'created_at')
    fields = ('role', 'content', 'metadata', 'created_at')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'title', 'language', 'message_count', 'is_active', 'created_at', 'updated_at')
    list_filter = ('language', 'is_active', 'created_at')
    search_fields = ('title', 'user__username')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    inlines = [ChatMessageInline]

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'role', 'content_short', 'provider_info', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content',)
    readonly_fields = ('created_at',)

    def content_short(self, obj):
        return obj.content[:80] + '…' if len(obj.content) > 80 else obj.content
    content_short.short_description = 'Contenu'

    def provider_info(self, obj):
        return obj.metadata.get('provider', '-')
    provider_info.short_description = 'Provider'


@admin.register(ChatFeedback)
class ChatFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'rating_display', 'comment', 'created_at')
    list_filter = ('rating', 'created_at')
    readonly_fields = ('created_at',)

    def rating_display(self, obj):
        return '👍' if obj.rating == 2 else '👎'
    rating_display.short_description = 'Note'
