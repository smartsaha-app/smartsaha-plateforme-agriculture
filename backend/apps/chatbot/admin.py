"""
apps/chatbot/admin.py
---------------------
Administration des modèles de chat pour le dashboard admin Django.
"""
from django.contrib import admin
from django.utils.html import format_html
from apps.chatbot.models import ChatSession, ChatMessage, ChatFeedback, KnowledgeEntry, UserAgronomicProfile


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


@admin.register(KnowledgeEntry)
class KnowledgeEntryAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category_badge', 'crops_display', 'region', 'language', 'status_badge', 'created_by', 'updated_at')
    list_filter   = ('category', 'status', 'language')
    search_fields = ('title', 'content', 'region')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    actions = ['publish_entries', 'unpublish_entries']

    fieldsets = (
        ('Identification', {
            'fields': ('title', 'category', 'language', 'status'),
        }),
        ('Contenu', {
            'fields': ('content',),
            'description': 'Écrivez en Markdown. Ce contenu sera injecté dans le contexte de Sesily lors des conversations correspondantes.',
        }),
        ('Ciblage', {
            'fields': ('crops', 'region'),
            'description': 'Laissez "crops" vide pour toutes les cultures. Laissez "region" vide pour tout Madagascar.',
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def category_badge(self, obj):
        colors = {
            'maladie': '#ef4444', 'calendrier': '#3b82f6', 'pratique': '#10b981',
            'variete': '#f59e0b', 'marche': '#8b5cf6', 'sol': '#92400e',
            'meteo': '#0ea5e9', 'stockage': '#6b7280', 'elevage': '#d97706', 'general': '#374151',
        }
        color = colors.get(obj.category, '#374151')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',
            color, obj.get_category_display(),
        )
    category_badge.short_description = 'Catégorie'

    def status_badge(self, obj):
        color = '#10b981' if obj.status == 'PUBLISHED' else '#f59e0b'
        label = 'Publié' if obj.status == 'PUBLISHED' else 'Brouillon'
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',
            color, label,
        )
    status_badge.short_description = 'Statut'

    def crops_display(self, obj):
        return ', '.join(obj.crops) if obj.crops else '—'
    crops_display.short_description = 'Cultures'

    @admin.action(description='✅ Publier les entrées sélectionnées')
    def publish_entries(self, request, queryset):
        queryset.update(status='PUBLISHED')

    @admin.action(description='⏸️ Mettre en brouillon les entrées sélectionnées')
    def unpublish_entries(self, request, queryset):
        queryset.update(status='DRAFT')


@admin.register(UserAgronomicProfile)
class UserAgronomicProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'main_crops_display', 'main_zones_display', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'main_crops', 'main_zones', 'known_issues', 'last_yield_notes', 'summary', 'updated_at')

    def main_crops_display(self, obj):
        return ', '.join(obj.main_crops) if obj.main_crops else '—'
    main_crops_display.short_description = 'Cultures'

    def main_zones_display(self, obj):
        return ', '.join(obj.main_zones) if obj.main_zones else '—'
    main_zones_display.short_description = 'Zones'
