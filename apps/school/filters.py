import django_filters

from utils.graphene.filters import IDListFilter
from apps.common.filters import SearchFilterMixin
from apps.school.models import School


class SchoolFilter(SearchFilterMixin, django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')
    provinces = IDListFilter(method='filter_provinces')
    districts = IDListFilter(method='filter_districts')
    municipalities = IDListFilter(method='filter_municipalities')
    ward_number = django_filters.CharFilter(method='filter_ward_number')
    local_address = django_filters.CharFilter(method='filter_local_address')
    pan_number = django_filters.CharFilter(method='filter_pan_number')
    vat_number = django_filters.CharFilter(method='filter_vat_number')

    class Meta:
        model = School
        fields = ()
        search_fields = ('name',)

    def filter_ward_number(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(ward_number__icontains=value)

    def filter_local_address(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(icontains__icontains=value)

    def filter_pan_number(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(icontains__icontains=value)

    def filter_vat_number(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(icontains__icontains=value)
