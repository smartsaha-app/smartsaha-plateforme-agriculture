import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def downgrade_expired_subscriptions():
    """
    Tourne chaque nuit à minuit via Celery Beat.
    Repasse en FREE tous les utilisateurs dont le plan PRO a expiré,
    marque leurs abonnements comme EXPIRED et leur envoie une notification.
    """
    from apps.users.models import User
    from apps.payments.models import Subscription
    from apps.notifications.models import Notification

    now = timezone.now()
    expired_users = User.objects.filter(plan='PRO', plan_expires_at__lt=now)
    count = expired_users.count()

    if count == 0:
        logger.info("downgrade_expired_subscriptions: aucun abonnement expiré.")
        return {'downgraded': 0}

    notifications = []
    for user in expired_users:
        user.plan = 'FREE'
        user.plan_expires_at = None
        user.save(update_fields=['plan', 'plan_expires_at'])

        Subscription.objects.filter(user=user, status='ACTIVE').update(status='EXPIRED')

        notifications.append(Notification(
            recipient=user,
            notification_type='system',
            title='Votre abonnement PRO a expiré',
            body=(
                'Votre compte est repassé en offre Gratuite. '
                'Renouvelez votre abonnement pour continuer à profiter de toutes les fonctionnalités SmartSaha PRO.'
            ),
            data={'action': 'renew_subscription'},
        ))

    if notifications:
        Notification.objects.bulk_create(notifications)

    logger.info(f"downgrade_expired_subscriptions: {count} compte(s) repassé(s) en FREE.")
    return {'downgraded': count}
