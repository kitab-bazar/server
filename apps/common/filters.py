import django_filters
from apps.common.models import Province, Municipality, District


class ProvinceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Province
        fields = ['name', ]

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)


class MunicipalityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Municipality
        fields = ['name', ]

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)


class DistrictFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = District
        fields = ['name', ]

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
