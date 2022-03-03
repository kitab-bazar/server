import django_filters
from django.db import models

from utils.graphene.filters import (
    DateGteFilter,
    DateLteFilter,
    MultipleInputFilter,
    IDListFilter,
)

from .models import BookOrder, Order, OrderWindow, OrderActivityLog
from .enums import OrderStatusEnum


class BookOrderFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_title')

    class Meta:
        model = BookOrder
        fields = ('title',)

    def filter_title(self, queryset, _, value):
        if not value:
            return queryset
        return queryset.filter(title__icontains=value)


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


class OrderActivityLogFilterSet(django_filters.FilterSet):
    create_by_users = IDListFilter(method='filter_create_by_users')

    class Meta:
        model = OrderActivityLog
        fields = ()

    def filter_create_by_users(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(created_by__in=value)
