# Generated by Django 3.2.12 on 2022-02-25 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20220225_0959'),
        ('payment', '0004_auto_20220223_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentlog',
            name='images',
        ),
        migrations.AddField(
            model_name='paymentlog',
            name='files',
            field=models.ManyToManyField(blank=True, to='common.ActivityLogFile', verbose_name='Flies'),
        ),
    ]