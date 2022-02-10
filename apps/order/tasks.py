from celery import shared_task
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from apps.order.models import Order
from apps.notification.models import Notification
from apps.common.tasks import generic_email_sender
import logging

logger = logging.getLogger(__name__)


def get_order_data(order_obj):
    '''
    Prepare data to send order email
    '''
    return {
        'total_price': order_obj.total_price,
        'order_code': order_obj.order_code,
        'status': order_obj.status,
        'order_placed_at': order_obj.order_placed_at,
        'order_items': [
            {
                'title': order_item.title,
                'price': order_item.price,
                'quantity': order_item.quantity,
                'isbn': order_item.isbn,
                'edition': order_item.edition,
                'total_price': order_item.total_price,
                'image': order_item.image.url if order_item.image else ''
            } for order_item in order_obj.book_order.all()
        ]
    }


def send_notification_to_customer(
    order_obj,
    notification_type,
    in_app_title,
    mail_title,
    heading,
):
    # Send in app notification
    Notification.objects.create(
        content_object=order_obj,
        recipient=order_obj.created_by,
        notification_type=notification_type,
        title=in_app_title,
    )
    # Send mail notification
    html_context = {
        'heading': heading,
        'message': mail_title,
        'full_name': order_obj.created_by.full_name,
        'order_data': get_order_data(order_obj)
    }
    subject, message = mail_title, mail_title
    transaction.on_commit(
        lambda: generic_email_sender.delay(
            subject, message, [order_obj.created_by.email], html_context=html_context, email_for='order'
        )
    )
    return True


def send_notfication_to_publisher(
    order_obj,
    notification_type,
    in_app_title,
    mail_title,
    heading,
):
    book_orders = order_obj.book_order.distinct('publisher')
    # NOTE: a book oder may have multiple publishers
    # Send in app notification
    Notification.objects.bulk_create([
        Notification(
            content_object=book_order.order,
            # Assuming a publisher profile is associated with single user
            recipient=book_order.publisher.publisher_user.first(),
            notification_type=notification_type,
            title=in_app_title,
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
        'heading': heading,
        'message': mail_title,
        'full_name': order_obj.created_by.full_name,
        'order_data': get_order_data(order_obj)
    }
    subject, message = mail_title, mail_title
    transaction.on_commit(
        lambda: generic_email_sender.delay(
            subject, message, recipient_list, html_context=html_context, email_for='order'
        )
    )
    return True


@shared_task(name='notification_sender')
def send_notification(order_id):
    order_obj = Order.objects.get(id=order_id)
    notification_date_attrs = {
        'day_name': order_obj.order_placed_at.strftime('%A'),
        'day': order_obj.order_placed_at.day,
        'month_name': order_obj.order_placed_at.strftime('%B'),
        'year': order_obj.order_placed_at.year,
        'time': order_obj.order_placed_at.strftime('%H:%M'),
        'order_code': order_obj.order_code,
    }
    if order_obj.status == Order.OrderStatus.RECEIVED.value:
        heading = 'Order received.'
        in_app_title = _(
            'Your Order %{order_code} placed on {day_name} {day}th {month_name} {year} at {time} has been recieved'
        ).format(**notification_date_attrs)

        mail_title = _(
            'Your Order %{order_code} placed on {day_name} {day}th {month_name}'
            '{year} at {time} has been recieved with details as below.'
        ).format(**notification_date_attrs)

        notification_type = Notification.NotificationType.ORDER_RECEIVED.value
        send_notfication_to_publisher(order_obj, notification_type, in_app_title, mail_title, heading)

    elif order_obj.status == Order.OrderStatus.PACKED.value:
        heading = 'Order packed.'
        in_app_title = _(
            'Your order %{order_code} placed on {day}th {month_name} {year} at {time} has been packed.'
        ).format(**notification_date_attrs)

        mail_title = _(
            'Your order %{order_code} placed on {day}th {month_name}'
            '{year} at {time} has been packed with details as below.'
        ).format(**notification_date_attrs)

        notification_type = Notification.NotificationType.ORDER_PACKED.value
        send_notification_to_customer(order_obj, notification_type, in_app_title, mail_title, heading)

    elif order_obj.status == Order.OrderStatus.COMPLETED.value:
        heading = 'Order completed.'
        in_app_title = _(
            'Your order %{order_code} placed on {day}th {month_name} {year} at {time} has been successfully delivered.'
        ).format(**notification_date_attrs)

        mail_title = _(
            'Your order %{order_code} placed on {day}th {month_name}'
            '{year} at {time} has been successfully delivered with details as below.'
        ).format(**notification_date_attrs)

        notification_type = Notification.NotificationType.ORDER_COMPLETED.value
        send_notification_to_customer(order_obj, notification_type, in_app_title, mail_title, heading)

    elif order_obj.status == Order.OrderStatus.CANCELLED.value:
        heading = 'Order cancelled.'
        in_app_title = _(
            'Your Order %{order_code} has been successfully cancelled.'
        ).format(**notification_date_attrs)
        mail_title = _(
            'Your Order %{order_code} has been successfully cancelled.'
        ).format(**notification_date_attrs)
        notification_type = Notification.NotificationType.ORDER_CANCELLED.value
        send_notification_to_customer(order_obj, notification_type, in_app_title, mail_title, heading)
