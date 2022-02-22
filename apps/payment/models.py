from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.common.models import BaseActivityLog
from apps.user.models import User


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        CASH = 'cash', _('Cash')
        CHEQUE = 'cheque', _('Cheque')

    class TransactionType(models.TextChoices):
        CREDIT = 'credit', _('Credit')
        DEBIT = 'debit', _('Debit')

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        VERIFIED = 'verified', _('Verified')
        CANCELLED = 'cancelled', _('Cancelled')

    transaction_type = models.CharField(
        max_length=20, choices=TransactionType.choices,
        null=True, blank=True,
        verbose_name=_('Transaction type')
    )
    payment_type = models.CharField(
        max_length=20, choices=PaymentType.choices,
        null=True, blank=True,
        verbose_name=_('Payment type')
    )
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('created at'))
    amount = models.FloatField(
        verbose_name=_('Amount')
    )
    status = models.CharField(
        verbose_name=_('Status'), choices=Status.choices,
        default=Status.PENDING,
        max_length=50
    )
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name=_('User')
    )

    def __str__(self):
        return f'{self.created_by_id} {self.transaction_type} - {self.payment_type}'

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payment')


class PaymentLog(BaseActivityLog):
    payment = models.ForeignKey(
        Payment, verbose_name=_('Payment'),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.payment_id)

    class Meta:
        verbose_name = _('Payment log')
        verbose_name_plural = _('Payment log')
