from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from apps.order.models import Order
from apps.notification.models import Notification
from apps.common.tasks import generic_email_sender


def send_notification_to_customer(instance, notification_type, title):
    # Send in app notification
    Notification.objects.create(
        content_object=instance,
        recipient=instance.created_by,
        notification_type=notification_type,
        title=title,
    )
    # Send mail notification
    html_context = {
        "heading": title,
        "message": title,
        "full_name": instance.created_by.full_name,
    }
    subject, message = title, title
    transaction.on_commit(lambda: generic_email_sender.delay(
        subject, message, [instance.created_by.email], html_context=html_context
    ))
    return True


def send_notfication_to_publisher(instance, notification_type, title):
    book_orders = instance.book_order.distinct('publisher')
    # NOTE: a book oder may have multiple publishers
    # Send in app notification
    Notification.objects.bulk_create([
        Notification(
            content_object=book_order.order,
            # Assuming a publisher profile is associated with single user
            recipient=book_order.publisher.publisher_user.first(),
            notification_type=notification_type,
            title=title,
        ) for book_order in book_orders
    ])

    # Prepare recipient list
    recipient_list = []
    for book_order in book_orders:
        # Assuming a publisher profile is associated with single user
        email = book_order.publisher.publisher_user.first().email
        recipient_list.append(email)

    # Send mail notifications
    # TODO: Improve subject, message, headings of email
    html_context = {
        "heading": title,
        "message": title
    }
    subject, message = title, title
    transaction.on_commit(lambda: generic_email_sender.delay(
        subject, message, recipient_list, html_context=html_context
    ))
    return True


@receiver(post_save, sender=Order)
def send_notification(
    sender, instance, **kwargs
):
    if instance.status == Order.OrderStatus.RECEIVED.value:
        title = _('Book order received.')
        notification_type = Notification.NotificationType.ORDER_RECEIVED.value
        send_notfication_to_publisher(instance, notification_type, title)

    elif instance.status == Order.OrderStatus.PACKED.value:
        title = _('Book order packed.')
        notification_type = Notification.NotificationType.ORDER_PACKED.value
        send_notification_to_customer(instance, notification_type, title)

    elif instance.status == Order.OrderStatus.COMPLETED.value:
        title = _('Book order completed.')
        notification_type = Notification.NotificationType.ORDER_COMPLETED.value
        send_notification_to_customer(instance, notification_type, title)

    elif instance.status == Order.OrderStatus.CANCELLED.value:
        title = _('Book order cancelled.')
        notification_type = Notification.NotificationType.ORDER_CANCELLED.value
        send_notification_to_customer(instance, notification_type, title)
