import django_filters
from django.db.models import Q
from apps.common.models import Province, Municipality, District, ActivityLogFile
from utils.graphene.filters import IDListFilter


class ProvinceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Province
        fields = ['name', ]

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(name_en__icontains=value) |
            Q(name_ne__icontains=value)
        )


class MunicipalityFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')
    provinces = IDListFilter(method='filter_provinces')
    districts = IDListFilter(method='filter_districts')

    class Meta:
        model = Municipality
        fields = ['name', ]

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(name_en__icontains=value) |
            Q(name_ne__icontains=value)
        )

    def filter_provinces(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(province__in=value)

    def filter_districts(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(district__in=value)


class DistrictFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')
    provinces = IDListFilter(method='filter_provinces')

    class Meta:
        model = District
        fields = ['name', ]

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(name_en__icontains=value) |
            Q(name_ne__icontains=value)
        )

    def filter_provinces(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(province__in=value)
