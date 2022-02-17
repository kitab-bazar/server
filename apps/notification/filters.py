import django_filters
from apps.notification.models import Notification


class NotificationFilter(django_filters.FilterSet):
    is_read = django_filters.rest_framework.BooleanFilter(
        method='filter_is_read', initial=False
    )

    class Meta:
        model = Notification
        fields = ()

    def filter_is_read(self, queryset, name, value):
        return queryset.filter(read=value)
