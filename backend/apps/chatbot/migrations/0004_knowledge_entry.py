import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0003_user_agronomic_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(
                    choices=[
                        ('maladie', '🦠 Maladie / Ravageur'),
                        ('calendrier', '📅 Calendrier cultural'),
                        ('pratique', '🌱 Bonne pratique'),
                        ('variete', '🌾 Variété / Semence'),
                        ('marche', '💰 Marché / Prix'),
                        ('sol', '🪨 Sol / Fertilisation'),
                        ('meteo', '🌦️ Météo / Climat'),
                        ('stockage', '🏚️ Stockage / Post-récolte'),
                        ('elevage', '🐄 Élevage'),
                        ('general', '📖 Général'),
                    ],
                    default='general',
                    max_length=20,
                )),
                ('content', models.TextField()),
                ('crops', models.JSONField(blank=True, default=list)),
                ('region', models.CharField(blank=True, default='', max_length=100)),
                ('language', models.CharField(
                    choices=[('fr', 'Français'), ('en', 'English'), ('mg', 'Malagasy')],
                    default='fr',
                    max_length=5,
                )),
                ('status', models.CharField(
                    choices=[('DRAFT', 'Brouillon'), ('PUBLISHED', 'Publié')],
                    default='DRAFT',
                    max_length=10,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='knowledge_entries',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Entrée de la base de connaissances',
                'verbose_name_plural': 'Base de connaissances Sesily',
                'ordering': ['-updated_at'],
            },
        ),
    ]
