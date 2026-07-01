from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_paymentmethod_provider_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(
                choices=[
                    ('PENDING', 'En attente de validation'),
                    ('ACTIVE', 'Actif'),
                    ('EXPIRED', 'Expiré'),
                    ('CANCELLED', 'Annulé'),
                ],
                default='ACTIVE',
                max_length=20,
            ),
        ),
    ]
