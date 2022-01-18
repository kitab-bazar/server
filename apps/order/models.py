import uuid
from django.utils.translation import ugettext_lazy as _
from django.db import models


class CartItem(models.Model):
    book = models.ForeignKey(
        'book.Book',
        on_delete=models.CASCADE,
        related_name='book_cart_item',
        null=True,
        blank=True,
        verbose_name=_('Book')
    )
    created_by = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='cart_item',
        null=True,
        blank=True,
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
    isbn = models.CharField(max_length=255, verbose_name=_('ISBN'))
    edition = models.CharField(max_length=255, verbose_name=_('Edition'))
    price = models.BigIntegerField(verbose_name=_('Price'))

    class Meta:
        verbose_name = _('Book Order')
        verbose_name_plural = _('Book Orders')

    def __str__(self):
        return self.title


class Order(models.Model):
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
    book_orders = models.ManyToManyField(
        'order.BookOrder',
        related_name='book_orders',
        blank=True,
        verbose_name=_('Book orders')
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return self.total_price
