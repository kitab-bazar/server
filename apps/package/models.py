import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseActivityLog


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
    total_price = models.IntegerField(verbose_name=_('Total price'), default=0)
    total_quantity = models.IntegerField(verbose_name=_('Total quantity'), default=0)

    class Meta:
        unique_together = ('publisher', 'order_window')
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
    )
    total_price = models.IntegerField(verbose_name=_('Total price'), default=0)
    total_quantity = models.IntegerField(verbose_name=_('Total quantity'), default=0)
    courier_package = models.ForeignKey(
        'package.CourierPackage',
        on_delete=models.PROTECT,
        related_name='courier_package',
        verbose_name=_('Courier package'),
    )

    class Meta:
        unique_together = ('school', 'order_window')
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
    order_window = models.ForeignKey(
        'order.OrderWindow',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name=_('Order window')
    )
    total_price = models.IntegerField(verbose_name=_('Total price'), default=0)
    total_quantity = models.IntegerField(verbose_name=_('Total quantity'), default=0)
    municipality = models.ForeignKey(
        'common.Municipality', verbose_name=_('Municipality'), related_name='courier_package_municipality',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = _('Courier Package')
        verbose_name_plural = _('Courier Packages')


class SchoolPackageLog(BaseActivityLog):
    school_package = models.ForeignKey(
        'package.SchoolPackage', verbose_name=_('School package'), related_name='school_package_logs',
        on_delete=models.CASCADE
    )


class PublisherPackageLog(BaseActivityLog):
    publisher_package = models.ForeignKey(
        'package.PublisherPackage', verbose_name=_('Publisher package'), related_name='publisher_package_logs',
        on_delete=models.CASCADE
    )


class CourierPackageLog(BaseActivityLog):
    courier_package = models.ForeignKey(
        'package.CourierPackage', verbose_name=_('Courier package'), related_name='courier_package_logs',
        on_delete=models.CASCADE
    )
