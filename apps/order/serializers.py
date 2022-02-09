from rest_framework import serializers
from django.db.models import F, Sum
from django.utils.translation import ugettext_lazy as _

from apps.order.models import CartItem, Order, BookOrder
from apps.book.models import Book, WishList
from config.serializers import CreatedUpdatedBaseSerializer, IntegerIDField


class CartItemSerializer(CreatedUpdatedBaseSerializer, serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('book', 'quantity',)

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

    def save(self, **kwargs):
        # Get current users cart
        cart_items = CartItem.objects.filter(created_by=self.context['request'].user).annotate(
            total_price=F('book__price') * F('quantity')
        )
        if not cart_items.exists():
            raise serializers.ValidationError(_('Your cart is empty.'))

        # Create order
        created_by = self.context['request'].user
        self.validated_data['created_by'] = created_by
        total_price = cart_items.aggregate(Sum('total_price'))['total_price__sum']
        cart_items.aggregate(Sum('total_price'))['total_price__sum']
        self.validated_data['total_price'] = total_price
        order = Order.objects.create(**self.validated_data)

        # Create book orders
        BookOrder.objects.bulk_create([
            BookOrder(
                title=cart_item.book.title,
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
        book_ids = CartItem.objects.filter(created_by=self.context['request'].user).values_list('book', flat=True)
        WishList.objects.filter(book_id__in=book_ids).delete()

        # Clear cart
        cart_items.delete()
        return order


class PlaceSingleOrderSerializer(serializers.Serializer):
    book_id = IntegerIDField(required=True, write_only=True)
    quantity = serializers.IntegerField(required=True, write_only=True)

    def validate_book_id(self, book_id):
        try:
            return Book.objects.get(pk=book_id).id
        except Book.DoesNotExist:
            raise serializers.ValidationError(_('Invalid book id.'))

    def save(self, **kwargs):
        created_by = self.context['request'].user
        book_id = self.validated_data['book_id']
        quantity = self.validated_data['quantity']

        book = Book.objects.get(pk=book_id)
        total_price = book.price * quantity

        # Create order
        self.validated_data['created_by'] = created_by
        self.validated_data['total_price'] = total_price
        order = Order.objects.create(created_by=created_by, total_price=total_price)

        # Create book orders
        BookOrder.objects.create(
            title=book.title,
            price=book.price,
            quantity=quantity,
            isbn=book.isbn,
            edition=book.edition,
            image=book.image,
            total_price=total_price,
            order=order,
            book=book,
            publisher=book.publisher
        )

        # Remove book form withlist
        WishList.objects.filter(book_id=book_id).delete()

        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    '''
    This serializer is used to update status of order only
    '''

    class Meta:
        model = Order
        fields = ('id', 'status',)
