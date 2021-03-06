import django_filters
from django.db import models
from django.db.models import Q

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
    users = IDListFilter(method='filter_users')
    order_windows = IDListFilter(method='filter_order_windows')
    districts = IDListFilter(method='filter_order_by_districts')
    municipalities = IDListFilter(method='filter_order_by_municipalities')

    class Meta:
        model = Order
        fields = ('status', 'users')

    def filter_users(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(created_by__in=value)

    def filter_order_windows(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(assigned_order_window__in=value)

    def filter_order_by_districts(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(Q(created_by__school__district__in=value) | Q(created_by__institution__district__in=value))

    def filter_order_by_municipalities(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(created_by__school__municipality__in=value) | Q(created_by__institution__municipality__in=value)
        )


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
