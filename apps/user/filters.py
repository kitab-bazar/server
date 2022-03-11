import django_filters
from apps.user.models import User
from django.db.models import Q

from utils.graphene.filters import MultipleInputFilter

from .enums import UserTypeEnum


class UserFilter(django_filters.FilterSet):
    user_type = MultipleInputFilter(UserTypeEnum)
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = User
        fields = ['email', 'is_active', 'is_verified']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(full_name__icontains=value) |
            Q(school__name__icontains=value) |
            Q(publisher__name__icontains=value)
        ).distinct()

    @property
    def qs(self):
        return super().qs.order_by('-id').distinct()
