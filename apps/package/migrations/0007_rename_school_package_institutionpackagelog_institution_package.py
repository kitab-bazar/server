# Generated by Django 3.2.12 on 2022-04-05 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0006_courierpackage_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='institutionpackagelog',
            old_name='school_package',
            new_name='institution_package',
        ),
    ]