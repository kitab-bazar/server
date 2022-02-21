# Generated by Django 3.2.12 on 2022-02-21 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0004_activitylogimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(blank=True, choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=20, null=True, verbose_name='Transaction type')),
                ('payment_type', models.CharField(blank=True, choices=[('cash', 'Cash'), ('cheque', 'Cheque')], max_length=20, null=True, verbose_name='Payment type')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='created at')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('verified', 'Verified'), ('cancelled', 'Cancelled')], default='pending', max_length=50, verbose_name='Status')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payment',
            },
        ),
        migrations.CreateModel(
            name='PaymentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('snapshot', models.JSONField(blank=True, default=None, null=True, verbose_name='Snapshot')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('images', models.ManyToManyField(blank=True, to='common.ActivityLogImage', verbose_name='Images')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.payment', verbose_name='Payment')),
            ],
            options={
                'verbose_name': 'Payment log',
                'verbose_name_plural': 'Payment log',
            },
        ),
    ]