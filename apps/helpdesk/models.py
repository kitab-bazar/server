from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class ContactMessage(models.Model):

    class MessageType(models.TextChoices):
        PAYMENT_RELATED = 'payment_related', 'Payment Related'
        ORDER_RELATED = 'order_related', 'Order Related'
        COURIER_RELATED = 'courier_related', 'Courier Related'
        AUTHOR_PUBLISHER_RELATED = 'author_publisher_related', 'Author/Publisher Related'
        BUSINESS_RELATED = 'business_related', 'Business Related'
        FEATURES_SUGGESTIONS_FEEDBACK = 'feature_suggestions_feedback', 'Features/Suggestions/Feedback'
        OTHER = 'other', 'Any Other'

    full_name = models.CharField(max_length=255, verbose_name=_('Full Name'))
    email = models.EmailField(_('Email address'))
    municipality = models.ForeignKey(
        'common.Municipality', verbose_name=_('Municipality'), related_name='contact_municipality',
        on_delete=models.PROTECT
    )
    address = models.CharField(verbose_name=_('Local address'), max_length=255, blank=True)
    message = models.TextField(blank=True, verbose_name=_('Description'))
    phone_number = PhoneNumberField(blank=True)
    message_type = models.CharField(
        choices=MessageType.choices, max_length=80,
        default=MessageType.OTHER,
        verbose_name=_('Message Type')
    )

    class Meta:
        verbose_name = _('Contact message')
        verbose_name_plural = _('Contact messages')

    def __str__(self):
        return self.message_type


class Faq(models.Model):
    class FaqPublishType(models.TextChoices):
        PUBLISH = 'publish', 'Publish'
        DRAFT = 'draft', 'Draft'

    question = models.TextField(null=True, blank=True, verbose_name=_('Question'))
    answer = models.TextField(null=True, blank=True, verbose_name=_('Answer'))
    faq_publish_type = models.CharField(
        choices=FaqPublishType.choices, max_length=40,
        default=FaqPublishType.DRAFT,
        verbose_name=_('Publish Type')
    )

    class Meta:
        verbose_name = _('Faq')
        verbose_name_plural = _('Faqs')

    def __str__(self):
        return self.question
