"""
apps/chatbot/tasks.py
---------------------
Tâches Celery pour Sesily AI :
  - send_proactive_agro_alerts  : alertes proactives météo + cultures + calendrier
  - refresh_all_agronomic_profiles : reconstruit les profils agronomiques hebdo
"""
import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def send_proactive_agro_alerts():
    """
    Tourne chaque matin à 6h30 via Celery Beat.
    Analyse les données de chaque agriculteur actif et envoie des notifications
    personnalisées sans attendre qu'il pose une question.

    Alertes générées :
    - Risque météo élevé sur une parcelle avec cultures actives
    - Tâches en retard depuis plus de 3 jours
    - Rappel de calendrier cultural FOFIFA (semis, récolte imminents)
    """
    from apps.users.models import User
    from apps.parcels.models import Parcel
    from apps.crops.models import ParcelCrop
    from apps.tasks.models import Task
    from apps.weather.models import WeatherData
    from apps.notifications.models import Notification

    today = timezone.now().date()
    now = timezone.now()

    # Agriculteurs actifs (ayant au moins une parcelle avec culture)
    farmer_ids = (
        ParcelCrop.objects
        .filter(parcel__owner__isnull=False)
        .values_list('parcel__owner_id', flat=True)
        .distinct()
    )
    farmers = User.objects.filter(id__in=farmer_ids)

    notifications_to_create = []
    total_sent = 0

    for farmer in farmers:
        parcels = Parcel.objects.filter(owner=farmer).prefetch_related('parcel_crops')

        for parcel in parcels:
            active_crops = parcel.parcel_crops.select_related('crop').filter(
                harvest_date__isnull=True
            )
            if not active_crops.exists():
                continue

            crop_names = ', '.join(c.crop.name for c in active_crops[:3])

            # ── 1. Alerte météo ──────────────────────────────────────────────
            try:
                latest_weather = WeatherData.objects.filter(
                    parcel=parcel
                ).order_by('-created_at').first()

                if latest_weather:
                    high_alerts = [
                        a for a in (latest_weather.agricultural_alerts or [])
                        if a.get('severity') in ('HIGH', 'CRITICAL')
                    ]
                    for alert in high_alerts[:2]:
                        notifications_to_create.append(Notification(
                            recipient=farmer,
                            notification_type='system',
                            title=f'⚠️ Alerte météo — {parcel.parcel_name}',
                            body=(
                                f'[{alert["severity"]}] {alert.get("type", "Risque")} sur votre parcelle '
                                f'"{parcel.parcel_name}" ({crop_names}). '
                                f'{alert.get("action", "Prenez les précautions nécessaires.")} '
                                f'Consultez Sesily pour des conseils personnalisés.'
                            ),
                            data={
                                'type': 'agro_alert',
                                'alert_type': alert.get('type'),
                                'parcel_uuid': str(parcel.uuid),
                            },
                        ))
                        total_sent += 1
            except Exception as e:
                logger.warning(f"Alerte météo ignorée (parcel {parcel.uuid}): {e}")

            # ── 2. Tâches en retard ──────────────────────────────────────────
            try:
                overdue_tasks = Task.objects.filter(
                    parcelCrop__parcel=parcel,
                    completed_at__isnull=True,
                    due_date__lt=today,
                    due_date__gte=today - timezone.timedelta(days=7),
                ).order_by('due_date')[:3]

                if overdue_tasks.exists():
                    task_names = ', '.join(t.name for t in overdue_tasks)
                    notifications_to_create.append(Notification(
                        recipient=farmer,
                        notification_type='system',
                        title=f'📋 Tâches en retard — {parcel.parcel_name}',
                        body=(
                            f'Vous avez {overdue_tasks.count()} tâche(s) en retard sur '
                            f'"{parcel.parcel_name}" : {task_names}. '
                            f'Demandez conseil à Sesily pour rattraper le calendrier.'
                        ),
                        data={
                            'type': 'overdue_tasks',
                            'parcel_uuid': str(parcel.uuid),
                        },
                    ))
                    total_sent += 1
            except Exception as e:
                logger.warning(f"Tâches en retard ignorées (parcel {parcel.uuid}): {e}")

            # ── 3. Rappel calendrier cultural FOFIFA ─────────────────────────
            try:
                _check_fofifa_calendar_alerts(
                    farmer, parcel, active_crops, today, notifications_to_create
                )
            except Exception as e:
                logger.warning(f"Calendrier FOFIFA ignoré (parcel {parcel.uuid}): {e}")

    if notifications_to_create:
        Notification.objects.bulk_create(notifications_to_create, ignore_conflicts=True)

    logger.info(f"send_proactive_agro_alerts: {total_sent} notification(s) envoyée(s) à {farmers.count()} agriculteurs.")
    return {'sent': total_sent, 'farmers': farmers.count()}


def _check_fofifa_calendar_alerts(farmer, parcel, active_crops, today, notifications):
    """
    Compare la date actuelle avec le calendrier cultural FOFIFA.
    Envoie une alerte si le mois prochain est un mois de semis ou de récolte.
    """
    import calendar as cal_module
    from apps.chatbot.knowledge_base import AgriculturalKnowledgeBase
    from apps.notifications.models import Notification

    kb = AgriculturalKnowledgeBase()
    next_month = (today.month % 12) + 1
    next_month_name = cal_module.month_name[next_month]

    for parcel_crop in active_crops[:3]:
        crop_name = parcel_crop.crop.name
        calendar_data = kb.get_planting_calendar_struct(crop_name)
        if not calendar_data:
            continue

        if next_month in calendar_data.get('planting_months', []):
            notifications.append(Notification(
                recipient=farmer,
                notification_type='system',
                title=f'🌱 Calendrier semis — {crop_name}',
                body=(
                    f'Le mois prochain ({next_month_name}) est la période de semis '
                    f'recommandée pour {crop_name} sur "{parcel.parcel_name}". '
                    f'Demandez à Sesily comment préparer votre terrain.'
                ),
                data={'type': 'planting_reminder', 'crop': crop_name, 'parcel_uuid': str(parcel.uuid)},
            ))

        if next_month in calendar_data.get('harvest_months', []) and parcel_crop.planting_date:
            notifications.append(Notification(
                recipient=farmer,
                notification_type='system',
                title=f'🌾 Approche de la récolte — {crop_name}',
                body=(
                    f'La récolte de {crop_name} approche sur "{parcel.parcel_name}" '
                    f'({next_month_name}). Consultez Sesily pour les meilleures pratiques '
                    f'post-récolte et de stockage.'
                ),
                data={'type': 'harvest_reminder', 'crop': crop_name, 'parcel_uuid': str(parcel.uuid)},
            ))


@shared_task
def refresh_all_agronomic_profiles():
    """
    Tourne chaque dimanche à 2h via Celery Beat.
    Reconstruit les profils agronomiques de tous les utilisateurs actifs.
    """
    from apps.users.models import User
    from apps.chatbot.models import UserAgronomicProfile

    users = User.objects.filter(is_active=True)
    count = 0
    for user in users:
        try:
            UserAgronomicProfile.refresh_for_user(user)
            count += 1
        except Exception as e:
            logger.warning(f"Profil non rafraîchi pour {user.email}: {e}")

    logger.info(f"refresh_all_agronomic_profiles: {count} profil(s) mis à jour.")
    return {'refreshed': count}
