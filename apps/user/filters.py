import django_filters
from apps.user.models import User
from django.db.models.functions import Lower, StrIndex, Coalesce
from django.db.models import Value
from utils.filters import AllowInitialFilterSetMixin


class UserFilter(AllowInitialFilterSetMixin, django_filters.FilterSet):
    full_name = django_filters.CharFilter(method='filter_full_name')

    class Meta:
        model = User
        fields = ['email', 'is_active']

    def filter_full_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.annotate(
            full=Coalesce(
                Lower('first_name'), Value(' '), Lower('last_name'),
            )
        ).annotate(
            idx=StrIndex('full', Value(value.lower()))
        ).filter(full__icontains=value).order_by('idx')
