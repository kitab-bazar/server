# Generated by Django 3.2.11 on 2022-01-28 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20220117_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title_ne',
            field=models.CharField(max_length=255, null=True, verbose_name='Title'),
        ),
    ]