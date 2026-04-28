import logging
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.marketplace.models import Order
from .models import Transaction, Escrow
from .serializers import TransactionSerializer, PaymentInitiateSerializer
from .services import PaymentService, FirebaseNotificationService

logger = logging.getLogger(__name__)

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter l'historique et le statut des transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # L'utilisateur ne voit que ses propres transactions
        return Transaction.objects.filter(buyer=self.request.user).order_by('-created_at')

    def retrieve(self, request, *args, **kwargs):
        """Correspond à /api/mobile/payments/status/{id}/"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    """
    POST /api/mobile/payments/initiate/
    Initialise un paiement via un provider.
    """
    serializer = PaymentInitiateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    order_id = serializer.validated_data['order_id']
    method = serializer.validated_data['method']
    phone = serializer.validated_data.get('phone', None)
    payment_token = serializer.validated_data.get('payment_token', None)

    order = get_object_or_404(Order, uuid=order_id)
    
    # Vérifier que l'utilisateur est bien l'acheteur
    if order.buyer != request.user:
        return Response({"detail": "Vous n'êtes pas l'acheteur de cette commande."}, status=status.HTTP_403_FORBIDDEN)
    
    # Initier le paiement
    try:
        payment_response = PaymentService.initiate_transaction(
            order=order,
            method=method,
            amount=order.total_price,
            user=request.user,
            phone=phone,
            payment_token=payment_token
        )
        return Response(payment_response, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Erreur d'initiation de paiement: {str(e)}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny]) # Webhook accessible publiquement de préférence (mais à sécuriser via IP ou signature)
def payment_webhook(request):
    """
    POST /api/mobile/payments/confirm/
    Webhook appelé par MVola, Orange, Stripe etc. pour confirmer un paiement.
    """
    # Note: Ceci est une implémentation générique qui doit être adaptée 
    # pour valider la signature cryptographique du provider réel.
    data = request.data
    provider_txn_id = data.get('provider_transaction_id') or data.get('server_correlation_id')
    txn_status = data.get('status', '').upper()
    
    if not provider_txn_id:
        return Response({"detail": "provider_transaction_id missing"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        transaction = Transaction.objects.get(provider_transaction_id=provider_txn_id)
    except Transaction.DoesNotExist:
        return Response({"detail": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

    if txn_status in ['SUCCESS', 'COMPLETED', '200']:
        transaction.status = 'SUCCESS'
        transaction.completed_at = timezone.now()
        transaction.save()
        
        # Mettre à jour l'Order lié
        transaction.order.status = 'CONFIRMED'
        transaction.order.save()
        
        # Mettre les fonds en Escrow (Séquestre)
        Escrow.objects.get_or_create(transaction=transaction, defaults={'status': 'HELD'})
        
        # Envoi notification push (Appel réel Firebase)
        FirebaseNotificationService.send_payment_notification(transaction.buyer, transaction)
        
    elif txn_status in ['FAILED', 'ERROR']:
        transaction.status = 'FAILED'
        transaction.save()

    return Response({"status": "acknowledged"}, status=status.HTTP_200_OK)
