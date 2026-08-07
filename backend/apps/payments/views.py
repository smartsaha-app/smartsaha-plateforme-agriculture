import logging
from datetime import timedelta
from rest_framework import viewsets, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.db import transaction as db_transaction

from apps.orders.models import Order
from apps.users.models import User
from apps.notifications.models import Notification
from .models import Transaction, Escrow, Subscription
from .serializers import (
    TransactionSerializer, PaymentInitiateSerializer,
    SubscriptionSerializer, SubscriptionUpgradeSerializer,
    UserSubscriptionRequestSerializer, SubscriptionStripeIntentSerializer,
)
from .services import PaymentService, FirebaseNotificationService
from django.conf import settings
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

logger = logging.getLogger(__name__)

# Grille tarifaire des abonnements PRO (en MGA), doit rester alignée avec le
# frontend (const PRICES dans la page subscription).
SUBSCRIPTION_PRICES = {
    30: 15000,
    90: 42750,
    180: 81000,
    365: 144000,
}


def _checkout_orders(order, buyer):
    """Retourne toutes les sous-commandes issues du même checkout."""
    if not order.checkout_reference:
        return Order.objects.filter(id=order.id, buyer=buyer)
    return Order.objects.filter(
        buyer=buyer,
        checkout_reference=order.checkout_reference,
    ).order_by('created_at')


def _complete_stripe_transactions(payment_intent_id, buyer=None):
    """Finalise chaque sous-commande liée à un PaymentIntent Stripe."""
    transactions = Transaction.objects.filter(provider_transaction_id=payment_intent_id)
    if buyer is not None:
        transactions = transactions.filter(buyer=buyer)

    with db_transaction.atomic():
        transactions = list(transactions.select_for_update().select_related('order', 'buyer'))
        if not transactions:
            return False

        for payment_transaction in transactions:
            if payment_transaction.status == 'SUCCESS':
                continue

            payment_transaction.status = 'SUCCESS'
            payment_transaction.completed_at = timezone.now()
            payment_transaction.save(update_fields=['status', 'completed_at'])

            order = payment_transaction.order
            order.status = 'PAID'
            order.payment_status = 'ESCROWED'
            order.decrease_stock()
            order.save(update_fields=['status', 'payment_status'])
            Escrow.objects.get_or_create(transaction=payment_transaction, defaults={'status': 'HELD'})
            FirebaseNotificationService.send_payment_notification(payment_transaction.buyer, payment_transaction)

    return True


def _activate_subscription_from_payment_intent(payment_intent_id):
    """Active l'abonnement PRO lié à un PaymentIntent Stripe réussi.

    Contrepartie, pour les abonnements, de `_complete_stripe_transactions`
    (qui, lui, s'occupe des commandes/Order).

    Important : la date d'expiration est recalculée ICI, à partir de l'état
    ACTUEL de l'utilisateur (verrouillé via select_for_update) et de
    `sub.duration_days`, et non reprise telle quelle depuis la valeur figée
    au moment de la création du PaymentIntent. Si un autre paiement (Mobile
    Money validé par un admin, ou un second paiement Stripe) a été activé
    entre-temps, ce recalcul permet de cumuler correctement au lieu
    d'écraser cette extension.
    """
    with db_transaction.atomic():
        sub = (
            Subscription.objects
            .select_for_update()
            .filter(payment_ref=payment_intent_id, provider='STRIPE')
            .order_by('-started_at')
            .first()
        )
        if not sub:
            return False
        if sub.status == 'ACTIVE':
            return True

        user = User.objects.select_for_update().get(pk=sub.user_id)

        now = timezone.now()
        base = user.plan_expires_at if (user.plan_expires_at and user.plan_expires_at > now) else now
        duration_days = sub.duration_days or 0
        new_expiry = base + timedelta(days=duration_days) if duration_days else base

        sub.status = 'ACTIVE'
        sub.expires_at = new_expiry
        sub.save(update_fields=['status', 'expires_at'])

        user.plan = 'PRO'
        user.plan_expires_at = new_expiry
        user.save(update_fields=['plan', 'plan_expires_at'])

        # Annuler les autres demandes PENDING / anciens abonnements actifs de l'utilisateur
        Subscription.objects.filter(user=user, status='PENDING').exclude(id=sub.id).update(status='CANCELLED')
        Subscription.objects.filter(user=user, status='ACTIVE').exclude(id=sub.id).update(status='CANCELLED')

        expiry_str = new_expiry.strftime('%d/%m/%Y') if new_expiry else '∞'
        Notification.objects.create(
            recipient=user,
            notification_type='system',
            title='Plan PRO activé !',
            body=f'Votre abonnement PRO a été activé jusqu\'au {expiry_str}. Profitez de toutes les fonctionnalités SmartSaha.',
            data={'plan': 'PRO', 'expires_at': new_expiry.isoformat() if new_expiry else None},
        )

    return True


def _activate_subscription_manually(sub):
    """Active une demande d'abonnement PENDING (Mobile Money) validée par un admin.

    Même logique de recalcul que `_activate_subscription_from_payment_intent`,
    pour rester cohérent entre les deux moyens de paiement.
    """
    with db_transaction.atomic():
        sub = Subscription.objects.select_for_update().get(pk=sub.pk)
        if sub.status != 'PENDING':
            return sub, False

        user = User.objects.select_for_update().get(pk=sub.user_id)

        now = timezone.now()
        base = user.plan_expires_at if (user.plan_expires_at and user.plan_expires_at > now) else now
        duration_days = sub.duration_days or 0
        new_expiry = base + timedelta(days=duration_days) if duration_days else base

        sub.status = 'ACTIVE'
        sub.expires_at = new_expiry
        sub.save(update_fields=['status', 'expires_at'])

        user.plan = 'PRO'
        user.plan_expires_at = new_expiry
        user.save(update_fields=['plan', 'plan_expires_at'])

        Subscription.objects.filter(user=user, status='PENDING').exclude(id=sub.id).update(status='CANCELLED')
        Subscription.objects.filter(user=user, status='ACTIVE').exclude(id=sub.id).update(status='CANCELLED')

        expiry_str = new_expiry.strftime('%d/%m/%Y') if new_expiry else '∞'
        Notification.objects.create(
            recipient=user,
            notification_type='system',
            title='Plan PRO activé !',
            body=f'Votre abonnement PRO a été activé jusqu\'au {expiry_str}. Profitez de toutes les fonctionnalités SmartSaha.',
            data={'plan': 'PRO', 'expires_at': new_expiry.isoformat() if new_expiry else None},
        )

    return sub, True


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
        summary="Valider une demande d'abonnement Mobile Money (PENDING)",
        tags=["Admin – Abonnements"],
        responses={200: SubscriptionSerializer},
    )
    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """
        POST /api/admin/subscriptions/{id}/approve/
        À utiliser uniquement après vérification manuelle, par l'admin, que
        le paiement Mobile Money correspondant à `payment_ref` est bien
        arrivé sur le compte marchand. Les paiements Stripe ne passent
        jamais par ici : ils s'activent automatiquement (webhook).
        """
        sub = get_object_or_404(Subscription, pk=pk)

        if sub.provider == 'STRIPE':
            return Response(
                {"detail": "Les paiements Stripe sont validés automatiquement, aucune action admin requise ici."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if sub.status != 'PENDING':
            return Response({"detail": f"Cette demande est déjà '{sub.status}'."}, status=status.HTTP_400_BAD_REQUEST)

        # Anti-fraude : une référence de transaction Mobile Money déjà
        # utilisée pour une demande précédemment approuvée ne peut pas être
        # réutilisée (empêche une même capture d'écran / référence de
        # servir sur plusieurs comptes ou plusieurs demandes).
        if sub.payment_ref:
            already_used = Subscription.objects.filter(
                payment_ref=sub.payment_ref,
                status='ACTIVE',
            ).exclude(id=sub.id).exists()
            if already_used:
                return Response(
                    {"detail": "Cette référence de paiement a déjà été utilisée pour un autre abonnement. Vérifiez avant de valider."},
                    status=status.HTTP_409_CONFLICT,
                )

        sub, _ = _activate_subscription_manually(sub)
        return Response(SubscriptionSerializer(sub).data)

    @extend_schema(
        summary="Rejeter une demande d'abonnement Mobile Money (PENDING)",
        tags=["Admin – Abonnements"],
        responses={200: SubscriptionSerializer},
    )
    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """
        POST /api/admin/subscriptions/{id}/reject/
        Body optionnel: { "reason": "..." }
        À utiliser quand la référence de paiement fournie ne correspond à
        aucun paiement réellement reçu (référence invalide, déjà utilisée,
        montant ne correspond pas, etc.).
        """
        sub = get_object_or_404(Subscription, pk=pk)
        if sub.status != 'PENDING':
            return Response({"detail": f"Cette demande est déjà '{sub.status}'."}, status=status.HTTP_400_BAD_REQUEST)

        reason = (request.data.get('reason') or '').strip()

        sub.status = 'CANCELLED'
        sub.save(update_fields=['status'])

        Notification.objects.create(
            recipient=sub.user,
            notification_type='system',
            title='Demande d’abonnement refusée',
            body=(
                f'Votre demande d’abonnement PRO via {sub.provider} n’a pas pu être validée'
                + (f' : {reason}' if reason else '. Vérifiez votre référence de paiement et réessayez.')
            ),
            data={'subscription_id': str(sub.id), 'reason': reason},
        )

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
    L'utilisateur soumet une demande d'upgrade PRO avec sa référence de paiement
    (Mobile Money uniquement). Crée un abonnement PENDING en attente de
    validation par l'admin.

    Pour Stripe, utiliser /subscription-payment-intent/ puis
    /subscription-confirm-stripe/ : le paiement est validé automatiquement,
    sans intervention admin.
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
        duration_days=duration_days,
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
    summary="Créer un PaymentIntent Stripe pour un abonnement PRO",
    tags=['Abonnements'],
    request=SubscriptionStripeIntentSerializer,
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription_stripe_intent(request):
    """
    POST /api/mobile/payments/subscription-payment-intent/
    Crée un PaymentIntent Stripe pour l'upgrade/renouvellement PRO, ainsi
    qu'un Subscription en PENDING dont le payment_ref stocke l'ID du
    PaymentIntent (utilisé ensuite pour retrouver l'abonnement à activer).
    """
    serializer = SubscriptionStripeIntentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    duration_days = serializer.validated_data['duration_days']

    amount_mga = SUBSCRIPTION_PRICES.get(duration_days)
    if amount_mga is None:
        return Response({"detail": "Durée d'abonnement non supportée."}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    now = timezone.now()
    base = user.plan_expires_at if (user.plan_expires_at and user.plan_expires_at > now) else now
    expires = base + timedelta(days=duration_days)

    try:
        import stripe
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        currency = getattr(settings, 'STRIPE_CURRENCY', 'MGA').lower()
        zero_decimal_currencies = {
            'bif', 'clp', 'djf', 'gnf', 'jpy', 'kmf', 'krw', 'mga', 'pyg', 'rwf', 'vnd', 'vuv', 'xaf', 'xof', 'xpf'
        }
        amount = int(amount_mga) if currency in zero_decimal_currencies else int(amount_mga * 100)

        with db_transaction.atomic():
            # Annuler toute demande PENDING existante pour éviter les doublons
            Subscription.objects.filter(user=user, status='PENDING').update(status='CANCELLED')

            sub = Subscription.objects.create(
                user=user,
                plan='PRO',
                status='PENDING',
                expires_at=expires,
                provider='STRIPE',
                duration_days=duration_days,
            )

            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=['card'],
                metadata={
                    'type': 'subscription',
                    'subscription_id': str(sub.id),
                    'user_uuid': str(user.uuid),
                    'duration_days': str(duration_days),
                },
            )

            sub.payment_ref = payment_intent.id
            sub.save(update_fields=['payment_ref'])

        return Response({
            'client_secret': payment_intent.client_secret,
            'payment_intent_id': payment_intent.id,
            'amount': amount,
            'currency': currency,
        })
    except Exception as e:
        logger.error(f"Erreur création PaymentIntent Stripe (abonnement): {e}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Confirmer le PaymentIntent Stripe d'un abonnement",
    tags=['Abonnements'],
    request=OpenApiTypes.OBJECT,
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_subscription_stripe_intent(request):
    """
    POST /api/mobile/payments/subscription-confirm-stripe/
    Appelé par le frontend juste après confirmCardPayment(), en filet de
    sécurité en plus du webhook Stripe : vérifie le statut auprès de Stripe
    puis active immédiatement le plan PRO si le paiement a réussi.
    """
    payment_intent_id = request.data.get('payment_intent_id')
    if not payment_intent_id:
        return Response({"detail": "payment_intent_id missing"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        import stripe
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    except Exception as e:
        logger.error(f"Erreur récupération PaymentIntent Stripe (abonnement): {e}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if payment_intent.status != 'succeeded':
        return Response({"detail": "PaymentIntent not succeeded", "status": payment_intent.status}, status=status.HTTP_400_BAD_REQUEST)

    if not _activate_subscription_from_payment_intent(payment_intent_id):
        return Response({"detail": "Abonnement introuvable pour ce paiement."}, status=status.HTTP_404_NOT_FOUND)

    sub = Subscription.objects.filter(payment_ref=payment_intent_id).order_by('-started_at').first()
    return Response(SubscriptionSerializer(sub).data if sub else {"status": "success"})


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


@extend_schema(
    summary="Créer un PaymentIntent Stripe",
    tags=['Paiements'],
    request=OpenApiTypes.OBJECT,
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_stripe_payment_intent(request):
    order_id = request.data.get('order_id')
    if not order_id:
        return Response({"detail": "order_id missing"}, status=status.HTTP_400_BAD_REQUEST)

    order = get_object_or_404(Order, id=order_id)
    if order.buyer != request.user:
        return Response({"detail": "Vous n'êtes pas l'acheteur de cette commande."}, status=status.HTTP_403_FORBIDDEN)
    if order.payment_method != 'STRIPE':
        return Response({"detail": "La commande n'est pas configurée pour Stripe."}, status=status.HTTP_400_BAD_REQUEST)

    orders = _checkout_orders(order, request.user)
    if orders.exclude(payment_method='STRIPE').exists():
        return Response({"detail": "Les sous-commandes doivent utiliser Stripe."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        import stripe
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        currency = getattr(settings, 'STRIPE_CURRENCY', 'MGA').lower()
        zero_decimal_currencies = {
            'bif','clp','djf','gnf','jpy','kmf','krw','mga','pyg','rwf','vnd','vuv','xaf','xof','xpf'
        }
        total = sum((checkout_order.total for checkout_order in orders), start=0)
        amount = int(total) if currency in zero_decimal_currencies else int(total * 100)

        # Évite de créer plusieurs PaymentIntents si l'acheteur relance le paiement.
        pending_transaction = Transaction.objects.filter(
            order__in=orders,
            buyer=request.user,
            method='STRIPE',
            status='PENDING',
            provider_transaction_id__isnull=False,
        ).order_by('-created_at').first()
        if pending_transaction:
            existing_intent = stripe.PaymentIntent.retrieve(pending_transaction.provider_transaction_id)
            if existing_intent.status in {'requires_payment_method', 'requires_confirmation', 'requires_action'}:
                return Response({
                    'client_secret': existing_intent.client_secret,
                    'payment_intent_id': existing_intent.id,
                    'amount': amount,
                    'currency': currency,
                    'checkout_reference': order.checkout_reference,
                })

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=['card'],
            metadata={
                'type': 'order',
                'checkout_reference': order.checkout_reference or order.order_number,
                'order_ids': ','.join(str(checkout_order.id) for checkout_order in orders),
            },
        )

        for checkout_order in orders:
            Transaction.objects.create(
                order=checkout_order,
                buyer=request.user,
                method='STRIPE',
                amount=checkout_order.total,
                currency=getattr(settings, 'STRIPE_CURRENCY', 'MGA'),
                provider_transaction_id=payment_intent.id,
                status='PENDING'
            )

        return Response({
            'client_secret': payment_intent.client_secret,
            'payment_intent_id': payment_intent.id,
            'amount': amount,
            'currency': currency,
            'checkout_reference': order.checkout_reference,
        })
    except Exception as e:
        logger.error(f"Erreur création PaymentIntent Stripe: {e}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Confirmer un PaymentIntent Stripe",
    tags=['Paiements'],
    request=OpenApiTypes.OBJECT,
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_stripe_payment_intent(request):
    payment_intent_id = request.data.get('payment_intent_id')
    if not payment_intent_id:
        return Response({"detail": "payment_intent_id missing"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        import stripe
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    except Exception as e:
        logger.error(f"Erreur récupération PaymentIntent Stripe: {e}")
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if payment_intent.status != 'succeeded':
        return Response({"detail": "PaymentIntent not succeeded", "status": payment_intent.status}, status=status.HTTP_400_BAD_REQUEST)

    if not _complete_stripe_transactions(payment_intent_id, request.user):
        return Response({"detail": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"status": "success"}, status=status.HTTP_200_OK)


@extend_schema(
    summary="Stripe webhook pour confirmer les paiements",
    tags=['Paiements'],
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    try:
        import stripe
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        event = stripe.Webhook.construct_event(payload, sig_header, getattr(settings, 'STRIPE_WEBHOOK_SECRET', ''))
    except ValueError as e:
        logger.error(f"Stripe Webhook ValueError: {e}")
        return Response({"detail": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Stripe Webhook error: {e}")
        return Response({"detail": "Webhook signature verification failed"}, status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        provider_id = session.get('payment_intent') or session['id']
        _complete_stripe_transactions(provider_id)
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        metadata = payment_intent.get('metadata') or {}
        if metadata.get('type') == 'subscription':
            _activate_subscription_from_payment_intent(payment_intent['id'])
        else:
            _complete_stripe_transactions(payment_intent['id'])

    return Response({"status": "received"}, status=status.HTTP_200_OK)