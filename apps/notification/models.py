from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class Notification(models.Model):
    ''' Generic Notification Model '''

    class NotificationType(models.TextChoices):
        ORDER_RECEIVED = 'order_received', 'Order received'
        ORDER_PACKED = 'order_packed', 'Order packed'
        ORDER_COMPLETED = 'order_completed', 'Order completed'
        ORDER_CANCELLED = 'order_cancelled', 'Order cancelled'
        GENERAL = 'general', 'General'

    notification_type = models.CharField(
        choices=NotificationType.choices, max_length=40,
        default=NotificationType.GENERAL,
        verbose_name=_("Notification Type")
    )
    # Display to user
    recipient = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name=_('For user'),)
    # Unread/Read
    read = models.BooleanField(
        default=False, verbose_name=_('Read'), help_text=_('Whether notification has been marked as read')
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created at'), help_text=_('When notification was created')
    )
    #  For generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.title
