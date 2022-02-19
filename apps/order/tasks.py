from celery import shared_task
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from apps.order.models import Order
from apps.notification.models import Notification
from apps.common.tasks import generic_email_sender
import logging

logger = logging.getLogger(__name__)


def send_notification_to_customer(order_obj, notification_type, title):
    # Send in app notification
    Notification.objects.create(
        content_object=order_obj,
        recipient=order_obj.created_by,
        notification_type=notification_type,
        title=title,
    )
    # Send mail notification
    html_context = {
        "heading": title,
        "message": title,
        "full_name": order_obj.created_by.full_name,
    }
    subject, message = title, title
    transaction.on_commit(
        lambda: generic_email_sender.delay(
            subject, message, [order_obj.created_by.email], html_context=html_context
        )
    )
    return True


def send_notfication_to_publisher(order_obj, notification_type, title):
    book_orders = order_obj.book_order.distinct('publisher')
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
    transaction.on_commit(
        lambda: generic_email_sender.delay(
            subject, message, recipient_list, html_context=html_context
        )
    )
    return True


@shared_task(name="notification_sender")
def send_notification(order_id):
    order_obj = Order.objects.get(id=order_id)
    if order_obj.status == Order.Status.RECEIVED.value:
        title = _('Book order received.')
        notification_type = Notification.NotificationType.ORDER_RECEIVED.value
        send_notfication_to_publisher(order_obj, notification_type, title)

    elif order_obj.status == Order.Status.PACKED.value:
        title = _('Book order packed.')
        notification_type = Notification.NotificationType.ORDER_PACKED.value
        send_notification_to_customer(order_obj, notification_type, title)

    elif order_obj.status == Order.Status.COMPLETED.value:
        title = _('Book order completed.')
        notification_type = Notification.NotificationType.ORDER_COMPLETED.value
        send_notification_to_customer(order_obj, notification_type, title)

    elif order_obj.status == Order.Status.CANCELLED.value:
        title = _('Book order cancelled.')
        notification_type = Notification.NotificationType.ORDER_CANCELLED.value
        send_notification_to_customer(order_obj, notification_type, title)
