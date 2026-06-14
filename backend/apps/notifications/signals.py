from django.db.models.signals import post_save
from django.dispatch import receiver


def _create(recipient, notification_type, title, body, data=None):
    from .models import Notification
    Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        body=body,
        data=data,
    )


@receiver(post_save, sender='messaging.Message')
def on_new_message(sender, instance, created, **kwargs):
    if not created:
        return
    sender_user  = instance.sender
    conversation = instance.conversation
    sender_name  = sender_user.first_name or sender_user.username
    for participant in conversation.participants.all():
        if participant.pk != sender_user.pk:
            _create(
                recipient=participant,
                notification_type='new_message',
                title='Nouveau message',
                body=f"{sender_name} vous a envoyé un message",
                data={'conversation_id': str(conversation.uuid)},
            )


@receiver(post_save, sender='orders.Order')
def on_order_event(sender, instance, created, **kwargs):
    order_data = {'order_id': str(instance.pk)}

    if created:
        # Notifier l'acheteur
        _create(
            recipient=instance.buyer,
            notification_type='new_order',
            title='Commande enregistrée',
            body=f"Votre commande #{instance.order_number} a bien été enregistrée.",
            data=order_data,
        )
        # Notifier chaque vendeur concerné (un par OrderItem distinct)
        sellers_notified: set = set()
        for item in instance.items.filter(seller__isnull=False).select_related('seller'):
            if item.seller_id not in sellers_notified:
                sellers_notified.add(item.seller_id)
                buyer_name = instance.buyer.first_name or instance.buyer.username
                _create(
                    recipient=item.seller,
                    notification_type='new_order',
                    title='Nouvelle commande reçue',
                    body=f"{buyer_name} a passé la commande #{instance.order_number}.",
                    data=order_data,
                )
        return

    status_labels = {
        'PAID':      ('Paiement confirmé',  'payment_received'),
        'CONFIRMED': ('Commande confirmée', 'order_status'),
        'SHIPPED':   ('Commande expédiée',  'order_status'),
        'DELIVERED': ('Commande livrée',    'order_status'),
        'CANCELLED': ('Commande annulée',   'order_status'),
    }
    if instance.status in status_labels:
        label, ntype = status_labels[instance.status]
        # Notifier l'acheteur du changement de statut
        _create(
            recipient=instance.buyer,
            notification_type=ntype,
            title=label,
            body=f"Commande #{instance.order_number} — {label}.",
            data=order_data,
        )
