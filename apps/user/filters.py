import django_filters
from apps.user.models import User
from utils.filters import AllowInitialFilterSetMixin


class UserFilter(AllowInitialFilterSetMixin, django_filters.FilterSet):
    full_name = django_filters.CharFilter(method='filter_full_name')

    class Meta:
        model = User
        fields = ['email', 'is_active']

    def filter_full_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(full_name__icontains=value)
