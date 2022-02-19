from rest_framework import serializers
from django.db.models import F, Sum
from django.utils.translation import gettext_lazy as _
from django.db import transaction

from config.serializers import CreatedUpdatedBaseSerializer

from apps.book.models import WishList

from .models import (
    CartItem,
    Order,
    BookOrder,
    OrderWindow,
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
                _('Only %(new_count)d books are allowed. Current request has %(allowed_count)d books.') % dict(
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
            raise serializers.ValidationError(_('Book is already added in cart.'))
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
            raise serializers.ValidationError(_('Your cart is empty.'))

        active_order_window = OrderWindow.get_active_window()
        if active_order_window is None:
            raise serializers.ValidationError(
                _('No active order window available right now.')
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
        BookOrder.objects.bulk_create([
            BookOrder(
                title_en=cart_item.book.title_en,
                title_ne=cart_item.book.title_ne,
                price=cart_item.book.price,
                quantity=cart_item.quantity,
                isbn=cart_item.book.isbn,
                edition=cart_item.book.edition,
                image=cart_item.book.image,
                total_price=cart_item.total_price,
                order=order,
                book=cart_item.book,
                publisher=cart_item.book.publisher
            ) for cart_item in cart_items
        ])
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


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    '''
    This serializer is used to update status of order only
    '''

    class Meta:
        model = Order
        fields = ('id', 'status',)

    def save(self, **kwargs):
        instance = self.instance
        updated_order = super().update(instance, self.validated_data)
        # Send notification
        transaction.on_commit(
            lambda: send_notification.delay(updated_order.id)
        )
        return updated_order
