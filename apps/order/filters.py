import django_filters
from django.db import models

from utils.graphene.filters import StringListFilter, DateGteFilter, DateLteFilter

from .models import BookOrder, Order, OrderWindow


class BookOrderFilterSet(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_title')

    class Meta:
        model = BookOrder
        fields = ('title',)

    def filter_title(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(title__icontains=value)


class OrderFilterSet(django_filters.FilterSet):
    status = StringListFilter(method='filter_order_status')

    class Meta:
        model = Order
        fields = ('status',)

    def filter_order_status(self, queryset, name, value):
        if not value:
            return queryset
        order_status_list = list(map(str.lower, value))
        return queryset.filter(status__in=order_status_list)


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
