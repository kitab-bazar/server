# Generated by Django 3.2.12 on 2022-03-07 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0002_courierpackagelog_publisherpackagelog_schoolpackagelog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courierpackagelog',
            name='courier_package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='package.courierpackage', verbose_name='Courier package'),
        ),
    ]