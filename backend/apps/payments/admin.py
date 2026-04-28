from django.contrib import admin
from .models import PaymentMethod, Transaction, Escrow, Refund, Invoice, Commission, Dispute

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'phone', 'card_last4', 'is_default')
    list_filter = ('provider', 'is_default')
    search_fields = ('user__username', 'phone')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'order', 'method', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'method', 'currency', 'created_at')
    search_fields = ('id', 'provider_transaction_id', 'buyer__username')
    readonly_fields = ('created_at', 'completed_at', 'id')

@admin.register(Escrow)
class EscrowAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'status', 'created_at', 'released_at')
    list_filter = ('status', 'created_at')

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'transaction', 'created_at')
    search_fields = ('invoice_number',)

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'rate', 'amount', 'created_at')

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'opened_by', 'status', 'created_at')
    list_filter = ('status', 'created_at')
