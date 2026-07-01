"""
apps/chatbot/models.py
----------------------
Modèles pour la mémoire conversationnelle et le feedback.

UserAgronomicProfile — profil persistant de l'agriculteur (mémoire longue)
ChatSession          — session de chat liée à un utilisateur
ChatMessage          — message individuel (user / assistant / system)
ChatFeedback         — feedback 👍/👎 sur une réponse de l'assistant
"""
import uuid

from django.conf import settings
from django.db import models


# ══════════════════════════════════════════════════════════════════════════════
# KnowledgeEntry — Base de connaissances Sesily (enrichissement RAG via admin)
# ══════════════════════════════════════════════════════════════════════════════
class KnowledgeEntry(models.Model):
    """
    Entrée de la base de connaissances Sesily AI.
    Enrichit le contexte RAG sans toucher au code.
    Gérée par l'admin via l'interface d'administration.
    """

    CATEGORY_CHOICES = [
        ('maladie',    '🦠 Maladie / Ravageur'),
        ('calendrier', '📅 Calendrier cultural'),
        ('pratique',   '🌱 Bonne pratique'),
        ('variete',    '🌾 Variété / Semence'),
        ('marche',     '💰 Marché / Prix'),
        ('sol',        '🪨 Sol / Fertilisation'),
        ('meteo',      '🌦️ Météo / Climat'),
        ('stockage',   '🏚️ Stockage / Post-récolte'),
        ('elevage',    '🐄 Élevage'),
        ('general',    '📖 Général'),
    ]

    STATUS_CHOICES = [
        ('DRAFT',     'Brouillon'),
        ('PUBLISHED', 'Publié'),
    ]

    title      = models.CharField(max_length=255)
    category   = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    content    = models.TextField(help_text='Contenu en Markdown. Sera injecté dans le contexte de Sesily.')
    crops      = models.JSONField(default=list, blank=True,
                                  help_text='Liste des cultures concernées. Ex: ["riz", "maïs"]')
    region     = models.CharField(max_length=100, blank=True, default='',
                                  help_text='Région spécifique (laisser vide = valable partout)')
    language   = models.CharField(max_length=5,
                                  choices=[('fr', 'Français'), ('en', 'English'), ('mg', 'Malagasy')],
                                  default='fr')
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='knowledge_entries',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Entrée de la base de connaissances'
        verbose_name_plural = 'Base de connaissances Sesily'
        ordering = ['-updated_at']

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title}'

    def to_context_block(self) -> str:
        """Formate l'entrée pour injection dans le contexte IA."""
        header = f'### {self.title}'
        if self.region:
            header += f' ({self.region})'
        return f'{header}\n{self.content}'


# ══════════════════════════════════════════════════════════════════════════════
# UserAgronomicProfile — Mémoire longue de l'agriculteur
# ══════════════════════════════════════════════════════════════════════════════
class UserAgronomicProfile(models.Model):
    """
    Profil agronomique persistant par utilisateur.
    Mis à jour automatiquement après chaque conversation.
    Injecté dans le contexte de chaque session pour que Sesily "connaisse" l'agriculteur.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agronomic_profile',
    )
    summary = models.TextField(blank=True, default='')
    main_crops = models.JSONField(default=list, blank=True)
    main_zones = models.JSONField(default=list, blank=True)
    known_issues = models.JSONField(default=list, blank=True)
    last_yield_notes = models.TextField(blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil Agronomique'
        verbose_name_plural = 'Profils Agronomiques'

    def __str__(self):
        return f"Profil de {self.user.username}"

    def to_context_string(self) -> str:
        """Formate le profil pour injection dans le prompt IA."""
        if not self.summary:
            return ''
        lines = ['## 👤 Profil de l\'Agriculteur (mémoire long terme)']
        lines.append(self.summary)
        if self.known_issues:
            lines.append(f'**Problèmes passés connus** : {", ".join(self.known_issues[:5])}')
        return '\n'.join(lines)

    @classmethod
    def refresh_for_user(cls, user):
        """
        Reconstruit le profil depuis les données réelles de la plateforme.
        Appelé après chaque conversation et par la tâche Celery hebdomadaire.
        """
        from apps.parcels.models import Parcel
        from apps.crops.models import ParcelCrop
        from apps.yields.models import YieldRecord

        profile, _ = cls.objects.get_or_create(user=user)

        try:
            parcels = Parcel.objects.filter(owner=user)
            parcel_names = [p.parcel_name for p in parcels if p.parcel_name]

            crops_qs = (
                ParcelCrop.objects
                .filter(parcel__owner=user)
                .select_related('crop')
                .values_list('crop__name', flat=True)
                .distinct()
            )
            crop_names = list(crops_qs[:10])

            yield_notes = []
            yields = (
                YieldRecord.objects
                .filter(parcelCrop__parcel__owner=user)
                .select_related('parcelCrop__crop')
                .order_by('-date')[:5]
            )
            for y in yields:
                crop_name = y.parcelCrop.crop.name if y.parcelCrop and y.parcelCrop.crop else '?'
                yield_notes.append(f'{crop_name}: {y.yield_amount:.0f} kg/{y.area:.0f}m²')

            # Issues connues : extraites des sessions de diagnostic
            issues = list(
                ChatMessage.objects
                .filter(session__user=user, role='assistant', metadata__intent='diagnostic')
                .values_list('metadata__intent', flat=True)
                .distinct()[:5]
            )

            summary_parts = []
            if crop_names:
                summary_parts.append(f'**Cultures pratiquées** : {", ".join(crop_names)}')
            if parcel_names:
                summary_parts.append(f'**Parcelles** : {", ".join(parcel_names[:5])} ({parcels.count()} au total)')
            if yield_notes:
                summary_parts.append(f'**Derniers rendements** : {" | ".join(yield_notes)}')

            profile.main_crops = crop_names
            profile.main_zones = parcel_names[:5]
            profile.last_yield_notes = ' | '.join(yield_notes)
            profile.summary = '\n'.join(summary_parts)
            profile.save(update_fields=['summary', 'main_crops', 'main_zones', 'last_yield_notes', 'updated_at'])
        except Exception:
            pass

        return profile


# ══════════════════════════════════════════════════════════════════════════════
# ChatSession
# ══════════════════════════════════════════════════════════════════════════════
class ChatSession(models.Model):
    """Session de conversation entre un utilisateur et l'assistant IA."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='chat_sessions',
    )
    parcel = models.ForeignKey(
        'parcels.Parcel',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='chat_sessions',
    )
    title = models.CharField(max_length=255, blank=True, default='')
    language = models.CharField(
        max_length=5,
        choices=[('fr', 'Français'), ('en', 'English'), ('mg', 'Malagasy')],
        default='fr',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Session de chat'
        verbose_name_plural = 'Sessions de chat'

    def __str__(self):
        return f"{self.title or 'Sans titre'} — {self.user.username}"

    def get_history(self, last_n: int = 10) -> list:
        """Retourne les N derniers messages formatés pour le prompt LLM."""
        messages = self.messages.order_by('-created_at')[:last_n]
        return [
            {'role': msg.role, 'content': msg.content}
            for msg in reversed(messages)
        ]

    def auto_title(self):
        """Génère un titre automatique depuis le premier message utilisateur."""
        if not self.title:
            first_msg = self.messages.filter(role='user').first()
            if first_msg:
                self.title = first_msg.content[:80].strip()
                if len(first_msg.content) > 80:
                    self.title += '…'
                self.save(update_fields=['title'])


# ══════════════════════════════════════════════════════════════════════════════
# ChatMessage
# ══════════════════════════════════════════════════════════════════════════════
class ChatMessage(models.Model):
    """Message individuel dans une session de chat."""

    ROLE_CHOICES = [
        ('user', 'Utilisateur'),
        ('assistant', 'Assistant'),
        ('system', 'Système'),
    ]

    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    # metadata peut contenir : provider, model, response_time_ms, intent, tokens_used
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Message de chat'
        verbose_name_plural = 'Messages de chat'

    def __str__(self):
        return f"[{self.role}] {self.content[:60]}…"


# ══════════════════════════════════════════════════════════════════════════════
# ChatFeedback
# ══════════════════════════════════════════════════════════════════════════════
class ChatFeedback(models.Model):
    """Feedback utilisateur sur une réponse de l'assistant."""

    RATING_CHOICES = [
        (1, '👎 Mauvais'),
        (2, '👍 Bon'),
    ]

    message = models.OneToOneField(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name='feedback',
        limit_choices_to={'role': 'assistant'},
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        emoji = '👍' if self.rating == 2 else '👎'
        return f"{emoji} sur message #{self.message.pk}"
