from django.db import models
from django.conf import settings
import uuid

class PaymentMethod(models.Model):
    PROVIDER_CHOICES = [
        ('MVOLA', 'MVola'),
        ('ORANGE_MONEY', 'Orange Money'),
        ('AIRTEL_MONEY', 'Airtel Money'),
        ('STRIPE', 'Stripe'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_methods')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    phone = models.CharField(max_length=20, null=True, blank=True, help_text="Pour les Mobile Money")
    card_last4 = models.CharField(max_length=4, null=True, blank=True, help_text="Pour Stripe")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        desc = self.phone if self.phone else f"**** {self.card_last4}"
        return f"{self.user} - {self.get_provider_display()} ({desc})"

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PROCESSING', 'En traitement'),
        ('SUCCESS', 'Succès'),
        ('FAILED', 'Échoué'),
        ('CANCELLED', 'Annulé'),
    ]
    CURRENCY_CHOICES = [
        ('MGA', 'Ariary'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey('marketplace.Order', on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='transactions_as_buyer')
    method = models.CharField(max_length=20, choices=PaymentMethod.PROVIDER_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='MGA')
    
    provider_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.amount} {self.currency} ({self.status})"

class Escrow(models.Model):
    STATUS_CHOICES = [
        ('HELD', 'Retenu'),
        ('RELEASED', 'Libéré'),
        ('REFUNDED', 'Remboursé'),
    ]
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='escrow')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='HELD')
    created_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Escrow pour Txn {self.transaction.id} - {self.status}"

class Refund(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('SUCCESS', 'Remboursé'),
        ('FAILED', 'Échoué'),
    ]
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='refund')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True)
    pdf_file = models.FileField(upload_to='invoices/%Y/%m/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Commission(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='commission')
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Taux en %")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Dispute(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Ouvert'),
        ('RESOLVED', 'Résolu'),
        ('CLOSED', 'Fermé'),
    ]
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='disputes')
    opened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='opened_disputes')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(null=True, blank=True)
