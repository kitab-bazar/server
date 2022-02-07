import django_filters
from apps.order.models import BookOrder, Order
from utils.graphene.filters import StringListFilter


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
