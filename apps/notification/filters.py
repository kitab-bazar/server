import django_filters
from apps.notification.models import Notification


class NotificationFilter(django_filters.FilterSet):
    class Meta:
        model = Notification
        fields = ['title', ]
