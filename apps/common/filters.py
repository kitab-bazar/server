import django_filters
from utils.filters import AllowInitialFilterSetMixin
from apps.common.models import Province, Municipality, District


class ProvinceFilter(AllowInitialFilterSetMixin, django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Province
        fields = ['name', ]

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)


class MunicipalityFilter(AllowInitialFilterSetMixin, django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Municipality
        fields = ['name', ]

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)


class DistrictFilter(AllowInitialFilterSetMixin, django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = District
        fields = ['name', ]

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
