from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.catalogue.models import Category

class Command(BaseCommand):
    help = 'Seed marketplace categories'

    def handle(self, *args, **options):
        categories = [
            "Semences",
            "Engrais",
            "Produits agricoles",
            "Matériels agricoles",
            "Intrants agricoles",
            "Services agricoles",
            "Équipements d’irrigation",
            "Produits phytosanitaires",
            "Produits transformés",
            "Autres"
        ]

        for index, cat_name in enumerate(categories):
            slug = slugify(cat_name)
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': cat_name,
                    'order': index
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category "{cat_name}" created'))
            else:
                category.name = cat_name
                category.order = index
                category.save()
                self.stdout.write(self.style.WARNING(f'Category "{cat_name}" already exists, updated order'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded categories'))
