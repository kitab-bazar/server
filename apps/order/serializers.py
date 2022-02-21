from rest_framework import serializers
from django.db.models import F, Sum
from django.utils.translation import gettext
from django.db import transaction

from config.serializers import CreatedUpdatedBaseSerializer

from apps.user.models import User
from apps.book.models import WishList

from .models import (
    CartItem,
    Order,
    BookOrder,
    OrderWindow,
    OrderActivityLog,
)
from .tasks import send_notification


class CartItemSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):
    MAX_ITEMS_ALLOWED = 1000

    class Meta:
        model = CartItem
        fields = ('book', 'quantity',)

    def validate_quantity(self, quantity):
        created_by = self.context['request'].user
        cart_item_qs = CartItem.objects.filter(created_by=created_by)
        if self.instance:
            # Exclude current item if already in database
            cart_item_qs = cart_item_qs.exclude(pk=self.instance.pk)
        current_total_cart_items_count = cart_item_qs.aggregate(Sum('quantity'))['quantity__sum'] or 0
        new_count = current_total_cart_items_count + quantity
        if new_count > self.MAX_ITEMS_ALLOWED:
            raise serializers.ValidationError(
                gettext('Only %(new_count)d books are allowed. Current request has %(allowed_count)d books.') % dict(
                    new_count=new_count,
                    allowed_count=self.MAX_ITEMS_ALLOWED,
                )
            )
        return quantity

    def validate_book(self, book):
        created_by = self.context['request'].user
        if not self.instance and CartItem.objects.filter(
            created_by=created_by, book=book
        ).exists():
            raise serializers.ValidationError(
                gettext('Book is already added in cart.')
            )
        return book


class CreateOrderFromCartSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ()

    def validate(self, data):
        created_by = self.context['request'].user
        # Get current users cart
        cart_items = CartItem.objects.filter(created_by=created_by).annotate(
            total_price=F('book__price') * F('quantity')
        )
        if not cart_items.exists():
            raise serializers.ValidationError(
                gettext('Your cart is empty.')
            )

        active_order_window = OrderWindow.get_active_window()
        if active_order_window is None:
            raise serializers.ValidationError(
                gettext('No active order window available right now.')
            )

        # Create order
        data['created_by'] = created_by
        data['assigned_order_window'] = active_order_window
        total_price = cart_items.aggregate(Sum('total_price'))['total_price__sum']
        cart_items.aggregate(Sum('total_price'))['total_price__sum']
        data['total_price'] = total_price
        data['cart_items'] = cart_items
        return data

    def create(self, validated_data):
        cart_items = validated_data.pop('cart_items')
        order = super().create(validated_data)
        # Create book orders
        book_orders = []
        for cart_item in cart_items:
            book_order = BookOrder(
                quantity=cart_item.quantity,
                total_price=cart_item.total_price,
                order=order,
                book=cart_item.book,
            )
            # Fetch and set attributes from book
            book_order._set_book_attributes()
            book_orders.append(book_order)
        BookOrder.objects.bulk_create(book_orders)
        # Remove books form withlist
        book_ids = CartItem.objects\
            .filter(created_by=validated_data['created_by'])\
            .values_list('book', flat=True)
        WishList.objects.filter(book_id__in=book_ids).delete()
        # Clear cart
        cart_items.delete()
        # Send notification
        transaction.on_commit(
            lambda: send_notification.delay(order.id)
        )
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    '''
    This serializer is used to update status of order only
    '''

    STATUS_CHANGE_ALLOWED_PERMISSION = {
        # UserType: [Current status, new status]
        User.UserType.SCHOOL_ADMIN: [
            (Order.Status.PENDING, Order.Status.CANCELLED),
        ],
        User.UserType.MODERATOR: [
            (Order.Status.PENDING, Order.Status.CANCELLED),
            (Order.Status.IN_TRANSIT, Order.Status.COMPLETED),
            (Order.Status.IN_TRANSIT, Order.Status.CANCELLED),
        ],
    }

    comment = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ('id', 'status', 'comment')

    def validate_status(self, status):
        current_status = self.instance.status
        user = self.context['request'].user
        if (
            # If user is SCHOOL_ADMIN, then the order should be created by that user
            user.user_type == User.UserType.SCHOOL_ADMIN and self.instance.created_by != user
        ) or (
            (current_status, status) not in self.STATUS_CHANGE_ALLOWED_PERMISSION.get(user.user_type) or []
        ):
            raise serializers.ValidationError(
                gettext('Changing from %(current_status)s to %(status)s is not allowed!!' % dict(
                    current_status=current_status,
                    status=status,
                ))
            )
        return status

    def update(self, instance, data):
        # Create a log
        OrderActivityLog.objects.create(
            order=self.instance,
            created_by=self.context['request'].user,
            system_generated_comment=f"Changed status from {self.instance.status} to {data['status']}",
            comment=data.pop('comment', '')
        )
        # Update
        updated_order = super().update(instance, data)
        # Send notification
        transaction.on_commit(
            lambda: send_notification.delay(updated_order.id)
        )
        return updated_order

    def create(self, data):
        raise Exception('Not allowed')
