from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard'
    verbose_name = 'Tableau de bord'

    def ready(self):
        import apps.dashboard.signals  # noqa: F401 — connecte les signaux au démarrage
