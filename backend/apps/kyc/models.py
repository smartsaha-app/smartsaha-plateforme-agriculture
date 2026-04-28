from django.db import models
from django.conf import settings
import uuid

class KYCDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('ID_CARD', 'Carte d\'Identité Nationale'),
        ('PASSPORT', 'Passeport'),
        ('COMPANY_REG', 'Registre de Commerce'),
        ('FARMER_CERT', 'Certificat d\'Agriculteur'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvé'),
        ('REJECTED', 'Rejeté'),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kyc_documents')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)
    file_url = models.FileField(upload_to='kyc_documents/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='kyc_reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rejection_reason = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.get_doc_type_display()} - {self.status}"
