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
        verbose_name=_('transaction type')
    )
    payment_type = models.CharField(
        max_length=20, choices=PaymentType.choices,
        null=True, blank=True,
        verbose_name=_('payment type')
    )
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('created at'))
    amount = models.FloatField(
        null=True, blank=True,
        verbose_name=_('amount')
    )
    status = models.CharField(
        verbose_name=_('status'), choices=Status.choices,
        default=Status.PENDING,
        max_length=50
    )
    description = models.TextField(
        verbose_name=_('description'),
        null=True, blank=True
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name=_('user')
    )

    def __str__(self):
        return f'{self.user.email} {self.transaction_type} - {self.payment_type}'

    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payment')


class PaymentLog(BaseActivityLog):
    payment = models.ForeignKey(
        Payment, verbose_name=_('payment'),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.payment)

    class Meta:
        verbose_name = _('payment log')
        verbose_name_plural = _('payment log')
