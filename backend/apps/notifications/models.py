import uuid
from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('new_message',      'Nouveau message'),
        ('new_order',        'Nouvelle commande'),
        ('order_status',     'Statut commande'),
        ('payment_received', 'Paiement reçu'),
        ('weather_alert',    'Alerte météo'),
        ('system',           'Système'),
    ]

    uuid              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='system')
    title             = models.CharField(max_length=255)
    body              = models.TextField()
    is_read           = models.BooleanField(default=False)
    data              = models.JSONField(null=True, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.notification_type}] {self.title} → {self.recipient.username}"
