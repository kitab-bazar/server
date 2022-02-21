# Generated by Django 3.2.12 on 2022-02-19 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_order_placed_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderWindow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_transit', 'IN TRANSIT'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=40, verbose_name='Order status'),
        ),
        migrations.AddField(
            model_name='order',
            name='assigned_order_window',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.orderwindow'),
        ),
    ]