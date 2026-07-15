from django.conf import settings
from rest_framework.exceptions import ValidationError
import logging
from .models import Transaction, Escrow

logger = logging.getLogger(__name__)

class MVolaAPI:
    """Implementation d'un traitement interne pour MVola sans appel externe."""
    def initiate_payment(self, transaction: Transaction, phone: str):
        transaction.status = 'PROCESSING'
        transaction.phone = phone
        transaction.provider_transaction_id = f"MVOLA_TXN_{transaction.id}"
        transaction.save()

        # Marquer la commande comme payée en attente de confirmation
        transaction.order.status = 'PAID'
        transaction.order.payment_status = 'ESCROWED'
        transaction.order.decrease_stock()
        transaction.order.save()

        Escrow.objects.get_or_create(transaction=transaction, defaults={'status': 'HELD'})
        return {"status": "processing", "provider_transaction_id": transaction.provider_transaction_id}

class OrangeMoneyAPI:
    """Implementation d'un traitement interne pour Orange Money sans appel externe."""  
    def initiate_payment(self, transaction: Transaction, phone: str):
        # Implementation of real Orange money web payment
        transaction.status = 'PROCESSING'
        transaction.phone = phone
        transaction.provider_transaction_id = f"OM_TXN_{transaction.id}"
        transaction.save()

        # Marquer la commande comme payée en attente de confirmation
        transaction.order.status = 'PAID'
        transaction.order.payment_status = 'ESCROWED'
        transaction.order.decrease_stock()
        transaction.order.save()

        Escrow.objects.get_or_create(transaction=transaction, defaults={'status': 'HELD'})

        return {"status": "processing", "provider_transaction_id": transaction.provider_transaction_id}

class AirtelMoneyAPI:
    """Implementation d'un traitement interne pour Airtel Money sans appel externe."""
    def initiate_payment(self, transaction: Transaction, phone: str):
        transaction.status = 'PROCESSING'
        transaction.phone = phone
        transaction.provider_transaction_id = f"AIRTEL_TXN_{transaction.id}"
        transaction.save()

        # Marquer la commande comme payée en attente de confirmation
        transaction.order.status = 'PAID'
        transaction.order.payment_status = 'ESCROWED'
        transaction.order.decrease_stock()
        transaction.order.save()

        Escrow.objects.get_or_create(transaction=transaction, defaults={'status': 'HELD'})

        return {"status": "processing", "provider_transaction_id": transaction.provider_transaction_id}

class StripeAPI:
    """Implement real API calls to Stripe"""
    def initiate_payment(self, transaction: Transaction, payment_token: str):
        try:
            import stripe
            stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
            
            charge = stripe.Charge.create(
                amount=int(transaction.amount * 100), # Amount in cents
                currency=transaction.currency.lower(),
                description=f"Commande SmartSaha {transaction.order.order_number}",
                source=payment_token,
            )
            
            if charge.status == 'succeeded':
                transaction.status = 'SUCCESS'
                transaction.provider_transaction_id = charge.id
                transaction.save()
                
                # Auto-create Escrow
                Escrow.objects.create(transaction=transaction, status='HELD')
                return {"status": "success", "charge_id": charge.id}
            else:
                transaction.status = 'FAILED'
                transaction.save()
                return {"status": "failed"}

        except Exception as e:
            logger.error(f"Stripe Error: {e}")
            transaction.status = 'FAILED'
            transaction.save()
            raise ValidationError(f"Erreur avec Stripe: {str(e)}")

class FirebaseNotificationService:
    @staticmethod
    def send_payment_notification(user, transaction: Transaction):
        # Real Firebase call
        try:
            import firebase_admin
            from firebase_admin import messaging
            
            # Check if app is initialized
            if not firebase_admin._apps:
                # App not initialized, typically should be done in apps.py
                # firebase_admin.initialize_app()
                pass
                
            # If user has a FCM token listed
            # Here we assume user model has a logic to get FCM tokens, or we send to a topic
            # topic = f"user_{user.id}"
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Paiement Confirmé",
                    body=f"Votre paiement de {transaction.amount} {transaction.currency} a été reçu.",
                ),
                topic=f"user_{user.uuid}"
            )
            try:
                response = messaging.send(message)
                logger.info(f"Firebase FCM message sent: {response}")
            except Exception as e:
                logger.error(f"Firebase FCM send error: {e}")
                
        except ImportError:
            logger.warning("firebase_admin package not installed.")

class MockPaymentAPI:
    """Fake API for testing workflow"""
    def initiate_payment(self, transaction: Transaction):
        transaction.status = 'SUCCESS'
        transaction.provider_transaction_id = f"MOCK_TXN_{transaction.id}"
        transaction.save()
        
        # Mettre à jour l'Order lié immédiatement pour le mode test
        transaction.order.status = 'PAID'
        transaction.order.payment_status = 'ESCROWED'
        transaction.order.decrease_stock() # Mise à jour des stocks
        transaction.order.save()
        
        # Créer le séquestre
        Escrow.objects.get_or_create(transaction=transaction, defaults={'status': 'HELD'})
        
        return {
            "status": "success", 
            "provider_transaction_id": transaction.provider_transaction_id,
            "message": "Paiement de test réussi (Simulation)"
        }

class PaymentService:
    @staticmethod
    def initiate_transaction(order, method: str, amount, user, phone=None, sender_name=None, transaction_reference=None, payment_token=None):
        transaction = Transaction.objects.create(
            order=order,
            buyer=user,
            method=method,
            amount=amount,
            sender_name=sender_name,
            transaction_reference=transaction_reference,
            # we default currency based on provider
            currency='MGA' if method in ['MVOLA', 'ORANGE_MONEY', 'AIRTEL_MONEY', 'TEST'] else 'USD'
        )
        
        if method == 'MVOLA':
            return MVolaAPI().initiate_payment(transaction, phone)
        elif method == 'ORANGE_MONEY':
            return OrangeMoneyAPI().initiate_payment(transaction, phone)
        elif method == 'AIRTEL_MONEY':
            return AirtelMoneyAPI().initiate_payment(transaction, phone)
        elif method == 'STRIPE':
            return StripeAPI().initiate_payment(transaction, payment_token)
        elif method == 'TEST':
            return MockPaymentAPI().initiate_payment(transaction)
        else:
            raise ValidationError("Fournisseur de paiement non supporté.")

    @staticmethod
    def release_escrow(order):
        """Libère les fonds du séquestre pour le vendeur"""
        try:
            from django.utils import timezone
            # Trouver la transaction réussie pour cet ordre
            transaction = Transaction.objects.filter(order=order, status='SUCCESS').first()
            if not transaction:
                return False
                
            escrow = Escrow.objects.filter(transaction=transaction, status='HELD').first()
            if escrow:
                escrow.status = 'RELEASED'
                escrow.released_at = timezone.now()
                escrow.save()
                return True
        except Exception as e:
            logger.error(f"Erreur lors de la libération du séquestre: {str(e)}")
        return False
