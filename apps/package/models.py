import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class PublisherPackageBook(models.Model):
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    book = models.ForeignKey(
        'book.Book',
        on_delete=models.PROTECT,
        related_name='publisher_package_book',
        verbose_name=_('Book')
    )
    publisher_package = models.ForeignKey(
        'package.PublisherPackage',
        related_name='publisher_package',
        on_delete=models.PROTECT,
        verbose_name=_('Publisher package')
    )

    class Meta:
        verbose_name = _('Publisher package related book')
        verbose_name_plural = _('Publisher related books')

    def __str__(self):
        return f'{self.book.title} - {self.id}'


class PublisherPackage(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ISSUE = 'issue', _('Issue')
        DELIVERED = 'delivered', _('Delivered')

    package_id = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False
    )
    status = models.CharField(
        max_length=40,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Publisher package status")
    )
    related_orders = models.ManyToManyField(
        'order.Order', verbose_name=_('Publisher related order'), related_name='publisher_related_orders',
    )
    publisher = models.ForeignKey(
        'publisher.Publisher',
        on_delete=models.PROTECT,
        related_name='publisher_packages',
        verbose_name=_('Publisher')
    )
    order_window = models.ForeignKey(
        'order.OrderWindow',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('Order window')
    )

    class Meta:
        verbose_name = _('Publisher Package')
        verbose_name_plural = _('Publisher packages')

    def __str__(self):
        return str(self.package_id)


class SchoolPackageBook(models.Model):
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    book = models.ForeignKey(
        'book.Book',
        on_delete=models.PROTECT,
        related_name='school_package_book',
        verbose_name=_('Book'),
    )
    school_package = models.ForeignKey(
        'package.SchoolPackage',
        related_name='school_package',
        on_delete=models.PROTECT,
        verbose_name=_('School package')
    )

    class Meta:
        verbose_name = _('School package related book')
        verbose_name_plural = _('School package related books')

    def __str__(self):
        return f'{self.book.title} - {self.id}'


class SchoolPackage(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_TRANSIT = 'in_transit', _('In transit')
        ISSUE = 'issue', _('Issue')
        DELIVERED = 'delivered', _('Delivered')

    package_id = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False
    )
    status = models.CharField(
        max_length=40,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("School package status")
    )
    related_orders = models.ManyToManyField(
        'order.Order', verbose_name=_('School related order'), related_name='school_related_orders',
    )
    school = models.ForeignKey(
        'user.User',
        on_delete=models.PROTECT,
        related_name='school_packages',
        verbose_name=_('School')
    )
    order_window = models.ForeignKey(
        'order.OrderWindow',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('Order window'),
        null=True
    )

    class Meta:
        verbose_name = _('School Package')
        verbose_name_plural = _('School packages')

    def __str__(self):
        return str(self.package_id)


class CourierPackage(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_TRANSIT = 'in_transit', _('In transit')
        ISSUE = 'issue', _('Issue')
        DELIVERED = 'delivered', _('Delivered')

    package_id = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False
    )
    status = models.CharField(
        max_length=40,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Courier package status")
    )
    related_orders = models.ManyToManyField(
        'order.Order', verbose_name=_('School related order'), related_name='courier_related_orders',
    )
    school_package_books = models.ManyToManyField(
        'package.SchoolPackageBook', verbose_name=_('School package books'), related_name='courier_school_package_books',
    )
    order_window = models.ForeignKey(
        'order.OrderWindow',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('Order window')
    )

    class Meta:
        verbose_name = _('Courier Package')
        verbose_name_plural = _('Courier Packages')
