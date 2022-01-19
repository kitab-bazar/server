import django_filters
from apps.order.models import BookOrder


class BookOrderFilterSet(django_filters.FilterSet):

    class Meta:
        model = BookOrder
        fields = ['id', ]


class OrderFilterSet(django_filters.FilterSet):

    class Meta:
        model = BookOrder
        fields = ['id', ]
