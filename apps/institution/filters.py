import django_filters
from utils.filters import AllowInitialFilterSetMixin
from apps.institution.models import Institution


class InstitutionFilter(AllowInitialFilterSetMixin, django_filters.FilterSet):
    institution_name = django_filters.CharFilter(method='filter_institution_name')
    provinces = django_filters.CharFilter(method='filter_provinces')
    districts = django_filters.CharFilter(method='filter_districts')
    municipalities = django_filters.CharFilter(method='filter_municipalities')
    ward_number = django_filters.CharFilter(method='filter_ward_number')
    local_address = django_filters.CharFilter(method='filter_local_address')
    pan_number = django_filters.CharFilter(method='filter_pan_number')
    vat_number = django_filters.CharFilter(method='filter_vat_number')

    class Meta:
        model = Institution
        fields = [
            'institution_name', 'provinces', 'districts', 'municipalities', 'ward_number',
            'local_address', 'pan_number', 'vat_number'
        ]

    def filter_institution_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(institution_name__icontains=value)

    def filter_provinces(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(province__in=value)

    def filter_districts(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(district__in=value)

    def filter_municipalities(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(municipality__in=value)

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
