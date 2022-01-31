# Generated by Django 3.2.11 on 2022-01-31 08:23

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0003_auto_20220110_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, null=True, verbose_name='Question')),
                ('question_en', models.TextField(blank=True, null=True, verbose_name='Question')),
                ('question_ne', models.TextField(blank=True, null=True, verbose_name='Question')),
                ('answer', models.TextField(blank=True, null=True, verbose_name='Answer')),
                ('answer_en', models.TextField(blank=True, null=True, verbose_name='Answer')),
                ('answer_ne', models.TextField(blank=True, null=True, verbose_name='Answer')),
                ('publish_type', models.CharField(choices=[('publish', 'Publish'), ('draft', 'Draft')], default='draft', max_length=40, verbose_name='Publish Type')),
            ],
            options={
                'verbose_name': 'Faq',
                'verbose_name_plural': 'Faqs',
            },
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email address')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Local address')),
                ('message', models.TextField(blank=True, verbose_name='Description')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('message_type', models.CharField(choices=[('payment_related', 'Payment Related'), ('order_related', 'Order Related'), ('courier_related', 'Courier Related'), ('author_publisher_related', 'Author/Publisher Related'), ('business_related', 'Business Related'), ('feature_suggestions_feedback', 'Features/Suggestions/Feedback'), ('other', 'Any Other')], default='other', max_length=80, verbose_name='Message Type')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contact_municipality', to='common.municipality', verbose_name='Municipality')),
            ],
            options={
                'verbose_name': 'Contact message',
                'verbose_name_plural': 'Contact messages',
            },
        ),
    ]
