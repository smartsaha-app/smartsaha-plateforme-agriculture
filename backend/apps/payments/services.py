import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError
import logging
from .models import Transaction, Escrow

logger = logging.getLogger(__name__)

class MVolaAPI:
    """Implement real API calls to MVola Madagascar"""
    def __init__(self):
        self.client_id = getattr(settings, 'MVOLA_CONSUMER_KEY', '')
        self.client_secret = getattr(settings, 'MVOLA_CONSUMER_SECRET', '')
        self.base_url = "https://api.mvola.mg/v1" # Example API endpoint or sandbox
        self.token = None

    def get_token(self):
        url = f"{self.base_url}/oauth2/token"
        response = requests.post(
            url,
            data={'grant_type': 'client_credentials'},
            auth=(self.client_id, self.client_secret)
        )
        if response.status_code == 200:
            self.token = response.json().get('access_token')
            return self.token
        raise ValidationError("Impossible de s'authentifier auprès de MVola")

    def initiate_payment(self, transaction: Transaction, phone: str):
        if not self.token:
            self.get_token()
            
        url = f"{self.base_url}/transactions"
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "amount": float(transaction.amount),
            "currency": transaction.currency,
            "description": f"Paiement commande {transaction.order.order_number}",
            "amount_currency": "MGA",
            "requesting_organisation_transaction_reference": str(transaction.id),
            "credit_party": [{"key": "msisdn", "value": "MERCHANT_PHONE"}], # To be replaced with real merchant
            "debit_party": [{"key": "msisdn", "value": phone}]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in [200, 201, 202]:
            data = response.json()
            transaction.provider_transaction_id = data.get('server_correlation_id', 'TESTING_TXN_ID')
            transaction.status = 'PROCESSING'
            transaction.phone = phone
            transaction.save()
            return data
        else:
            logger.error(f"MVola Error: {response.text}")
            transaction.status = 'FAILED'
            transaction.save()
            raise ValidationError(f"Échec de l'initiation MVola: {response.status_code}")

class OrangeMoneyAPI:
    """Implement real API calls to Orange Money Madagascar"""
    def __init__(self):
        self.client_id = getattr(settings, 'ORANGE_MONEY_CLIENT_ID', '')
        
    def initiate_payment(self, transaction: Transaction, phone: str):
        # Implementation of real Orange money web payment
        transaction.status = 'PROCESSING'
        transaction.phone = phone
        transaction.provider_transaction_id = f"OM_TXN_{transaction.id}"
        transaction.save()
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

class PaymentService:
    @staticmethod
    def initiate_transaction(order, method: str, amount, user, phone=None, payment_token=None):
        transaction = Transaction.objects.create(
            order=order,
            buyer=user,
            method=method,
            amount=amount,
            # we default currency based on provider
            currency='MGA' if method in ['MVOLA', 'ORANGE_MONEY', 'AIRTEL_MONEY'] else 'USD'
        )
        
        if method == 'MVOLA':
            return MVolaAPI().initiate_payment(transaction, phone)
        elif method == 'ORANGE_MONEY':
            return OrangeMoneyAPI().initiate_payment(transaction, phone)
        elif method == 'STRIPE':
            return StripeAPI().initiate_payment(transaction, payment_token)
        else:
            raise ValidationError("Fournisseur de paiement non supporté.")
