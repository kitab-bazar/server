# Generated by Django 3.2.11 on 2022-01-25 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0006_remove_publisher_email'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookorder',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to='publisher.publisher', verbose_name='Publisher'),
        ),
    ]
