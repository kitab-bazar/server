# Generated by Django 3.2.12 on 2022-03-07 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_activitylogimage_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('package', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolPackageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('snapshot', models.JSONField(blank=True, default=None, null=True, verbose_name='Snapshot')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('images', models.ManyToManyField(blank=True, to='common.ActivityLogImage', verbose_name='Images')),
                ('school_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='package.schoolpackage', verbose_name='School package')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublisherPackageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('snapshot', models.JSONField(blank=True, default=None, null=True, verbose_name='Snapshot')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('images', models.ManyToManyField(blank=True, to='common.ActivityLogImage', verbose_name='Images')),
                ('publisher_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='package.publisherpackage', verbose_name='Publisher package')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CourierPackageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('snapshot', models.JSONField(blank=True, default=None, null=True, verbose_name='Snapshot')),
                ('courier_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='package.publisherpackage', verbose_name='Courier package')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('images', models.ManyToManyField(blank=True, to='common.ActivityLogImage', verbose_name='Images')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]