from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from .apps import CatalogueConfig

@receiver(post_migrate, sender=CatalogueConfig)
def run_seed_categories(sender, **kwargs):
    """
    Automatiquement exécuter le seed des catégories après chaque migration
    de l'application catalogue.
    """
    print("Automating category seeding...")
    try:
        call_command('seed_categories')
    except Exception as e:
        print(f"Error seeding categories: {e}")
