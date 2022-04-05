import django_filters

from utils.graphene.filters import SimpleInputFilter
from apps.payment.models import Payment, PaymentLog
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


class PaymentLogFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = PaymentLog
        fields = ()

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(comment__icontains=value)
