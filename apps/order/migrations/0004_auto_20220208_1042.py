# Generated by Django 3.2.11 on 2022-02-08 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_bookorder_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookorder',
            name='title_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='bookorder',
            name='title_ne',
            field=models.CharField(max_length=255, null=True, verbose_name='Title'),
        ),
    ]