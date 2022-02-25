# Generated by Django 3.2.12 on 2022-02-27 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0002_activitylogimage_created_by'),
        ('payment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentlog',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='images',
            field=models.ManyToManyField(blank=True, to='common.ActivityLogImage', verbose_name='Images'),
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.payment', verbose_name='Payment'),
        ),
        migrations.AddField(
            model_name='payment',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='payment',
            name='modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payment_modified_by', to=settings.AUTH_USER_MODEL, verbose_name='Modified by'),
        ),
        migrations.AddField(
            model_name='payment',
            name='paid_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='payment_paid_by'),
        ),
    ]