import django_filters
from utils.graphene.filters import MultipleInputFilter, IDListFilter
from apps.package.models import (
    PublisherPackage,
    SchoolPackage,
    CourierPackage,
    PublisherPackageLog,
    SchoolPackageLog,
    CourierPackageLog,
)
from apps.package.enums import (
    PublisherPackageStatusEnum,
    SchoolPackageStatusEnum,
    CourierPackageStatusEnum
)


class PublisherPackageFilterSet(django_filters.FilterSet):

    status = MultipleInputFilter(PublisherPackageStatusEnum, field_name='status')
    publishers = IDListFilter(method='filter_publishers')
    order_windows = IDListFilter(method='filter_order_windows')

    class Meta:
        model = PublisherPackage
        fields = ()

    def filter_publishers(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(publisher__in=value)

    def filter_order_windows(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(order_window__in=value)


class SchoolPackageFilterSet(django_filters.FilterSet):

    status = MultipleInputFilter(SchoolPackageStatusEnum, field_name='status')
    schools = IDListFilter(method='filter_schools')
    order_windows = IDListFilter(method='filter_order_windows')

    class Meta:
        model = SchoolPackage
        fields = ()

    def filter_schools(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(school__in=value)

    def filter_order_windows(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(order_window__in=value)


class CourierPackageFilterSet(django_filters.FilterSet):

    status = MultipleInputFilter(CourierPackageStatusEnum, field_name='status')
    municipalities = IDListFilter(method='filter_municipalities')
    order_windows = IDListFilter(method='filter_order_windows')

    class Meta:
        model = CourierPackage
        fields = ()

    def filter_municipalities(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(municipality__in=value)

    def filter_order_windows(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(order_window__in=value)


class PublisherPackageLogFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = PublisherPackageLog
        fields = ()

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(comment__icontains=value)


class SchoolPackageLogFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = SchoolPackageLog
        fields = ()

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(comment__icontains=value)


class CourierPackageLogFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = CourierPackageLog
        fields = ()

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(comment__icontains=value)
