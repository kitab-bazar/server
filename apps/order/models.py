import uuid
from django.utils.translation import gettext_lazy as _
from django.db import models


class CartItem(models.Model):
    book = models.ForeignKey(
        'book.Book',
        on_delete=models.CASCADE,
        related_name='book_cart_item',
        verbose_name=_('Book')
    )
    created_by = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='cart_item',
        verbose_name=_('Created by')
    )
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def __str__(self):
        return f'{self.created_by} - {self.book}'


class BookOrder(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    price = models.BigIntegerField(verbose_name=_('Price'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    isbn = models.CharField(max_length=13, verbose_name=_('ISBN'))
    edition = models.CharField(max_length=255, verbose_name=_('Edition'))
    total_price = models.BigIntegerField(verbose_name=_('Total Price'))
    image = models.FileField(
        upload_to='orders/books/images/', max_length=255, null=True, blank=True, default=None,
    )
    book = models.ForeignKey(
        'book.Book',
        on_delete=models.SET_NULL,
        related_name='book_order_cart_item',
        verbose_name=_('Book'),
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        'order.Order',
        related_name='book_order',
        on_delete=models.CASCADE,
        verbose_name=_('Order')
    )
    publisher = models.ForeignKey(
        'publisher.Publisher',
        on_delete=models.CASCADE,
        related_name='publisher',
        verbose_name=_('Publisher')
    )

    class Meta:
        verbose_name = _('Book Order')
        verbose_name_plural = _('Book Orders')

    def __str__(self):
        return self.title


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        RECEIVED = 'received', 'Received'
        PACKED = 'packed', 'Packed'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    total_price = models.BigIntegerField(verbose_name=_('Total Price'))
    order_code = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False
    )
    created_by = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name=_('Created by')
    )
    status = models.CharField(
        choices=OrderStatus.choices, max_length=40,
        default=OrderStatus.RECEIVED,
        verbose_name=_("Order status")
    )
    order_placed_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Order placed at")
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return self.status
