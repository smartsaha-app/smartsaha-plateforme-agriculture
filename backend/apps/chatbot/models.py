"""
apps/chatbot/models.py
----------------------
Modèles pour la mémoire conversationnelle et le feedback.

ChatSession  — session de chat liée à un utilisateur (et optionnellement une parcelle)
ChatMessage  — message individuel (user / assistant / system)
ChatFeedback — feedback 👍/👎 sur une réponse de l'assistant
"""
import uuid

from django.conf import settings
from django.db import models


# ══════════════════════════════════════════════════════════════════════════════
# ChatSession
# ══════════════════════════════════════════════════════════════════════════════
class ChatSession(models.Model):
    """Session de conversation entre un utilisateur et l'assistant IA."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
