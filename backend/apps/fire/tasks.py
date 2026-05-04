import logging
from celery import shared_task
from apps.fire.services import FireAlertService

logger = logging.getLogger(__name__)

@shared_task
def refresh_fire_alerts():
    """
    Tâche Celery planifiée pour s'exécuter quotidiennement.
    Télécharge les dernières données FIRMS, croise avec les parcelles
    et envoie les emails de notification.
    """
    logger.info("Démarrage de la tâche Celery : refresh_fire_alerts")
    try:
        service = FireAlertService()
        report = service.run(radius_km=15.0)
        logger.info(f"Tâche Celery terminée avec succès. Rapport: {report}")
        return report
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution de refresh_fire_alerts : {e}", exc_info=True)
        raise e
