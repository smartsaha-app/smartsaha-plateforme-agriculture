import logging
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q

from apps.orders.models import Order
from apps.users.models import User
from apps.notifications.models import Notification
from .models import Transaction, Escrow, Subscription
from .serializers import (
    TransactionSerializer, PaymentInitiateSerializer,
    SubscriptionSerializer, SubscriptionUpgradeSerializer,
    UserSubscriptionRequestSerializer,
)
from .services import PaymentService, FirebaseNotificationService
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

logger = logging.getLogger(__name__)


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or getattr(request.user, 'role', None) == 'ADMIN'
        )


class SubscriptionAdminViewSet(viewsets.ViewSet):
    """Admin ViewSet to manage user subscriptions."""
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(summary="Liste de tous les abonnements", tags=["Admin – Abonnements"], responses={200: SubscriptionSerializer(many=True)})
    def list(self, request):
        qs = Subscription.objects.select_related('user').order_by('-started_at')
        search = request.query_params.get('search', '').strip()
        plan   = request.query_params.get('plan', '').upper()
        status_filter = request.query_params.get('status', '').upper()
        if search:
            qs = qs.filter(Q(user__email__icontains=search) | Q(user__username__icontains=search))
        if plan in ('FREE', 'PRO'):
            qs = qs.filter(plan=plan)
        if status_filter in ('PENDING', 'ACTIVE', 'EXPIRED', 'CANCELLED'):
            qs = qs.filter(status=status_filter)
        return Response(SubscriptionSerializer(qs, many=True).data)

    @extend_schema(summary="Détail d'un abonnement", tags=["Admin – Abonnements"], responses={200: SubscriptionSerializer})
    def retrieve(self, request, pk=None):
        sub = get_object_or_404(Subscription, pk=pk)
        return Response(SubscriptionSerializer(sub).data)

    @extend_schema(
        summary="Mettre à jour le plan d'un utilisateur",
        tags=["Admin – Abonnements"],
        request=SubscriptionUpgradeSerializer,
        responses={200: SubscriptionSerializer},
    )
    @action(detail=False, methods=['post'], url_path='set-plan/(?P<user_uuid>[^/.]+)')
    def set_plan(self, request, user_uuid=None):
        user = get_object_or_404(User, uuid=user_uuid)
        serializer = SubscriptionUpgradeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        plan          = serializer.validated_data['plan']
        duration_days = serializer.validated_data['duration_days']
        payment_ref   = serializer.validated_data.get('payment_ref', '')
        provider      = serializer.validated_data.get('provider', 'MANUAL')

        now = timezone.now()
        if plan == 'PRO':
            base = user.plan_expires_at if (user.plan_expires_at and user.plan_expires_at > now) else now
            expires = base + timedelta(days=duration_days)
        else:
            expires = None

        # Update User fields
        user.plan = plan
        user.plan_expires_at = expires
        user.save(update_fields=['plan', 'plan_expires_at'])

        # Cancel previous active subscriptions
        Subscription.objects.filter(user=user, status='ACTIVE').update(status='CANCELLED')

        sub = Subscription.objects.create(
            user=user,
            plan=plan,
            status='ACTIVE',
            expires_at=expires,
            payment_ref=payment_ref or None,
            provider=provider,
        )

        # Annuler aussi les demandes PENDING de cet utilisateur
        Subscription.objects.filter(user=user, status='PENDING').update(status='CANCELLED')

        # Notifier l'utilisateur de l'activation de son plan
        expiry_str = expires.strftime('%d/%m/%Y') if expires else '∞'
        Notification.objects.create(
            recipient=user,
            notification_type='system',
            title=f'Plan {plan} activé !',
            body=f'Votre abonnement {plan} a été activé jusqu\'au {expiry_str}. Profitez de toutes les fonctionnalités SmartSaha.',
            data={'plan': plan, 'expires_at': expires.isoformat() if expires else None},
        )

        return Response(SubscriptionSerializer(sub).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Annuler l'abonnement d'un utilisateur",
        tags=["Admin – Abonnements"],
        responses={200: SubscriptionSerializer},
    )
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        sub = get_object_or_404(Subscription, pk=pk)
        sub.status = 'CANCELLED'
        sub.save(update_fields=['status'])
        # Downgrade user to FREE
        sub.user.plan = 'FREE'
        sub.user.plan_expires_at = None
        sub.user.save(update_fields=['plan', 'plan_expires_at'])
        return Response(SubscriptionSerializer(sub).data)

    @extend_schema(
        summary="Statistiques des abonnements",
        tags=["Admin – Abonnements"],
        responses={200: OpenApiTypes.OBJECT},
    )
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        total_users = User.objects.count()
        pro_users   = User.objects.filter(plan='PRO').count()
        free_users  = total_users - pro_users
        active_subs = Subscription.objects.filter(status='ACTIVE').count()
        return Response({
            'total_users': total_users,
            'pro_users':   pro_users,
            'free_users':  free_users,
            'active_subscriptions': active_subs,
        })


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter l'historique et le statut des transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()
        # L'utilisateur ne voit que ses propres transactions
        return Transaction.objects.filter(buyer=self.request.user).order_by('-created_at')

    def retrieve(self, request, *args, **kwargs):
        """Correspond à /api/mobile/payments/status/{id}/"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema(
    summary="Initialiser un paiement",
    tags=['Paiements'],
    request=PaymentInitiateSerializer,
    responses={200: OpenApiTypes.OBJECT}
)
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
    sender_name = serializer.validated_data.get('sender_name', None)
    transaction_reference = serializer.validated_data.get('transaction_reference', None)
    payment_token = serializer.validated_data.get('payment_token', None)

    order = get_object_or_404(Order, id=order_id)
    
    # Vérifier que l'utilisateur est bien l'acheteur
    if order.buyer != request.user:
        return Response({"detail": "Vous n'êtes pas l'acheteur de cette commande."}, status=status.HTTP_403_FORBIDDEN)
    
    # Initier le paiement
    try:
        payment_response = PaymentService.initiate_transaction(
            order=order,
            method=method,
            amount=order.total,
            user=request.user,
            phone=phone,
            sender_name=sender_name,
            transaction_reference=transaction_reference,
            payment_token=payment_token
        )
        return Response(payment_response, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Erreur d'initiation de paiement: {str(e)}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Statistiques financières du vendeur",
    tags=['Paiements'],
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def seller_stats(request):
    """
    GET /api/mobile/payments/seller-stats/
    Retourne les statistiques financières du vendeur (solde, séquestre, etc.)
    """
    user = request.user
    
    # On cherche toutes les transactions liées aux ordres contenant des produits de ce vendeur
    transactions = Transaction.objects.filter(order__items__seller=user, status='SUCCESS').distinct()
    
    available_balance = 0
    escrow_balance = 0
    
    for txn in transactions:
        # On ne prend que la part du vendeur (somme des items vendus)
        from apps.orders.models import OrderItem
        order_items = OrderItem.objects.filter(order=txn.order, seller=user)
        seller_amount = sum(item.subtotal for item in order_items)
        
        try:
            escrow = txn.escrow
            if escrow.status == 'RELEASED':
                available_balance += seller_amount
            elif escrow.status == 'HELD':
                escrow_balance += seller_amount
        except Escrow.DoesNotExist:
            continue

    return Response({
        "available_balance": float(available_balance),
        "escrow_balance": float(escrow_balance),
        "total_sales": float(available_balance + escrow_balance),
        "currency": "MGA"
    })


@extend_schema(
    summary="Demande d'upgrade de plan par l'utilisateur",
    tags=['Abonnements'],
    request=UserSubscriptionRequestSerializer,
    responses={201: SubscriptionSerializer}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_subscription_upgrade(request):
    """
    POST /api/mobile/payments/subscription-request/
    L'utilisateur soumet une demande d'upgrade PRO avec sa référence de paiement.
    Crée un abonnement PENDING en attente de validation par l'admin.
    """
    serializer = UserSubscriptionRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    provider      = serializer.validated_data['provider']
    phone         = serializer.validated_data.get('phone', '')
    sender_name   = serializer.validated_data.get('sender_name', '')
    payment_ref   = serializer.validated_data['payment_ref']
    duration_days = serializer.validated_data['duration_days']

    now  = timezone.now()
    user = request.user
    base = user.plan_expires_at if (user.plan_expires_at and user.plan_expires_at > now) else now
    expires = base + timedelta(days=duration_days)

    # Annuler toute demande PENDING existante pour éviter les doublons
    Subscription.objects.filter(user=request.user, status='PENDING').update(status='CANCELLED')

    sub = Subscription.objects.create(
        user=request.user,
        plan='PRO',
        status='PENDING',
        expires_at=expires,
        payment_ref=payment_ref,
        provider=provider,
        sender_name=sender_name or None,
    )

    # Notifier tous les admins de la nouvelle demande
    admin_users = User.objects.filter(is_staff=True)
    notifications = [
        Notification(
            recipient=admin,
            notification_type='system',
            title=f'Demande abonnement PRO — {user.email}',
            body=f'{user.get_full_name() or user.email} a soumis une demande PRO via {provider} (réf: {payment_ref}, {duration_days}j).',
            data={'user_uuid': str(user.uuid), 'subscription_id': str(sub.id)},
        )
        for admin in admin_users
    ]
    if notifications:
        Notification.objects.bulk_create(notifications)

    return Response(SubscriptionSerializer(sub).data, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Abonnement actif de l'utilisateur connecté",
    tags=['Abonnements'],
    responses={200: SubscriptionSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_subscription(request):
    """
    GET /api/mobile/payments/my-subscription/
    Retourne l'abonnement actif ou en attente de l'utilisateur.
    """
    sub = Subscription.objects.filter(
        user=request.user,
        status__in=['ACTIVE', 'PENDING']
    ).order_by('-started_at').first()
    if not sub:
        return Response({'plan': request.user.plan, 'status': None}, status=status.HTTP_200_OK)
    return Response(SubscriptionSerializer(sub).data)


@api_view(['POST'])
@permission_classes([AllowAny])

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
        transaction.order.status = 'PAID'
        transaction.order.payment_status = 'ESCROWED'
        transaction.order.decrease_stock() # Mise à jour des stocks
        transaction.order.save()
        
        # Mettre les fonds en Escrow (Séquestre)
        Escrow.objects.get_or_create(transaction=transaction, defaults={'status': 'HELD'})
        
        # Envoi notification push (Appel réel Firebase)
        FirebaseNotificationService.send_payment_notification(transaction.buyer, transaction)
        
    elif txn_status in ['FAILED', 'ERROR']:
        transaction.status = 'FAILED'
        transaction.save()

    return Response({"status": "acknowledged"}, status=status.HTTP_200_OK)
