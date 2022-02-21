import django_filters
from apps.user.models import User


class UserFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(method='filter_full_name')
    school = django_filters.NumberFilter(method='filter_school')

    class Meta:
        model = User
        fields = ['email', 'is_active', 'is_verified']

    def filter_full_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(full_name__icontains=value)

    def filter_school(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(school__id=value)
