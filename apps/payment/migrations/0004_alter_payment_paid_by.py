# Generated by Django 3.2.12 on 2022-03-21 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0003_auto_20220302_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paid_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_paid_by', to=settings.AUTH_USER_MODEL, verbose_name='payment_paid_by'),
        ),
    ]
