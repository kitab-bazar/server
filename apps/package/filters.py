import django_filters
from utils.graphene.filters import MultipleInputFilter

from apps.package.models import PublisherPackage, SchoolPackage, CourierPackage
from apps.package.enums import (
    PublisherPackageStatusEnum,
    SchoolPackageStatusEnum,
    CourierPackageStatusEnum
)


class PublisherPackageFilterSet(django_filters.FilterSet):

    status = MultipleInputFilter(PublisherPackageStatusEnum, field_name='status')

    class Meta:
        model = PublisherPackage
        fields = ()


class SchoolPackageFilterSet(django_filters.FilterSet):

    status = MultipleInputFilter(SchoolPackageStatusEnum, field_name='status')

    class Meta:
        model = SchoolPackage
        fields = ()


class CourierPackageFilterSet(django_filters.FilterSet):

    status = MultipleInputFilter(CourierPackageStatusEnum, field_name='status')

    class Meta:
        model = CourierPackage
        fields = ()
