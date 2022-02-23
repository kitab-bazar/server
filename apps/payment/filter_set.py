import django_filters

from utils.graphene.filters import SimpleInputFilter
from apps.payment.models import Payment
from apps.payment.enums import (
    StatusEnum,
    TransactionTypeEnum,
    PaymentTypeEnum
)


class PaymentFilterSet(django_filters.FilterSet):
    status = SimpleInputFilter(StatusEnum)
    transaction_type = SimpleInputFilter(TransactionTypeEnum)
    payment_type = SimpleInputFilter(PaymentTypeEnum)

    class Meta:
        model = Payment
        fields = ()
