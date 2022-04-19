import django_filters
from apps.user.models import User
from django.db.models import Q

from utils.graphene.filters import MultipleInputFilter

from .enums import UserTypeEnum


class UserFilter(django_filters.FilterSet):
    user_type = MultipleInputFilter(UserTypeEnum)
    search = django_filters.CharFilter(method='filter_search')
    order_mismatch_users = django_filters.rest_framework.BooleanFilter(
        method='filter_order_mismatch_users', initial=True
    )
    provinces = django_filters.CharFilter(method='filter_provinces')
    districts = django_filters.CharFilter(method='filter_districts')
    municipalities = django_filters.CharFilter(method='filter_municipalities')

    class Meta:
        model = User
        fields = ['email', 'is_active', 'is_verified']

    @property
    def qs(self):
        return super().qs.order_by('-id').distinct()

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(full_name__icontains=value) |
            Q(school__name__icontains=value) |
            Q(publisher__name__icontains=value) |
            Q(institution__name__icontains=value)
        ).distinct()

    def filter_order_mismatch_users(self, queryset, name, value):
        if not value:
            return queryset.filter(outstanding_balance__gte=0)

        return queryset.filter(outstanding_balance__lt=0).distinct()

    def filter_provinces(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(school__province__in=value) |
            Q(institution__province__in=value) |
            Q(publisher__province__in=value)
        )

    def filter_districts(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(school__district__in=value) |
            Q(institution__district__in=value) |
            Q(publisher__district__in=value)
        )

    def filter_municipalities(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(school__municipality__in=value) |
            Q(institution__municipality__in=value) |
            Q(publisher__municipality__in=value)
        )
