# Generated by Django 3.2.11 on 2022-01-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_auto_20220110_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Email'),
        ),
    ]