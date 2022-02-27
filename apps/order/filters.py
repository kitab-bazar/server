import django_filters
from django.db import models

from utils.graphene.filters import (
    DateGteFilter,
    DateLteFilter,
    MultipleInputFilter,
)

from apps.common.filters import SearchFilterMixin
from .models import BookOrder, Order, OrderWindow
from .enums import OrderStatusEnum


class BookOrderFilterSet(SearchFilterMixin, django_filters.FilterSet):
    class Meta:
        model = BookOrder
        fields = ('title',)
        search_fields = ('title',)


class OrderFilterSet(django_filters.FilterSet):
    status = MultipleInputFilter(OrderStatusEnum)

    class Meta:
        model = Order
        fields = ('status',)


class OrderWindowFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    start_date_gte = DateGteFilter(field_name='start_date')
    start_date_lte = DateLteFilter(field_name='start_date')
    end_date_gte = DateGteFilter(field_name='end_date')
    end_date_lte = DateLteFilter(field_name='end_date')

    class Meta:
        model = OrderWindow
        fields = ()

    def filter_search(self, qs, name, value):
        if value:
            qs = qs.filter(
                models.Q(title__icontains=value) |
                models.Q(description__icontains=value)
            )
        return qs
