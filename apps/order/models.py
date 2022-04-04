import uuid

from django.utils import timezone
from django.utils.translation import gettext_lazy as _, gettext
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models


class OrderWindow(models.Model):

    class OrderWindowType(models.TextChoices):
        SCHOOL = 'school', _('School')
        INSTITUTION = 'institution', _('Institution')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    type = models.CharField(
        choices=OrderWindowType.choices, max_length=40, verbose_name=_('Order window type'), blank=True
    )

    def __str__(self):
        return f'{self.title} :: {self.start_date} - {self.end_date}'

    @classmethod
    def get_active_window(cls):
        now_date = timezone.now().date()
        return cls.objects.filter(
            start_date__lte=now_date,
            end_date__gte=now_date,
        ).first()

    def clean(self):
        conflicting_order_window_qs = OrderWindow.objects.filter(
            # (StartA <= EndB) and (EndA >= StartB) https://stackoverflow.com/a/325964/3436502
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        )
        if self.pk:
            conflicting_order_window_qs = conflicting_order_window_qs.exclude(id=self.pk)
        conflicting_order_window = conflicting_order_window_qs.first()
        if self.end_date < self.start_date:
            raise ValidationError(
                gettext('Start date should not be greater than end date')
            )
        elif conflicting_order_window:
            raise ValidationError(
                gettext(
                    "This order window conflicts with another order window with id: %(id)d"
                    % dict(id=conflicting_order_window.pk)
                )
            )
        return super().clean()

    def save(self, *args, **kwargs):
        # Making sure clean is always called
        self.clean()
        return super().save(*args, **kwargs)


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

    def _set_book_attributes(self):
        for attr in [
            *(
                f'title_{lang}'
                for lang, _ in settings.LANGUAGES
            ),
            'publisher',
            'price',
            'isbn',
            'edition',
            'image',
        ]:
            setattr(self, attr, getattr(self.book, attr))
        self.total_price = self.price * self.quantity

    def save(self, *args, **kwargs):
        if self.pk is None:  # Create
            self._set_book_attributes()
        return super().save(*args, **kwargs)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')  # Order not acknowledged
        IN_TRANSIT = 'in_transit', _('IN TRANSIT')  # Order is in-transit
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')

    assigned_order_window = models.ForeignKey(OrderWindow, null=True, blank=True, on_delete=models.SET_NULL)
    total_price = models.BigIntegerField(verbose_name=_('Total Price'))
    order_code = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Order placed at"))
    created_by = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name=_('Created by')
    )
    status = models.CharField(
        max_length=40,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Order status")
    )

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return self.status


class OrderActivityLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='activity_logs')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Created by')
    )
    system_generated_comment = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ('-id',)
