
import graphene
from django.db.models import QuerySet
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.fields import DjangoPaginatedListObjectField, CustomDjangoListField
from utils.graphene.types import CustomDjangoListObjectType

from apps.package.models import (
    PublisherPackage,
    PublisherPackageBook,
    SchoolPackage,
    SchoolPackageBook,
    CourierPackage,
    PublisherPackageLog,
    SchoolPackageLog,
    CourierPackageLog,
)
from apps.user.models import User
from apps.package.filters import (
    PublisherPackageFilterSet,
    SchoolPackageFilterSet,
    CourierPackageFilterSet,
    PublisherPackageLogFilterSet,
    SchoolPackageLogFilterSet,
    CourierPackageLogFilterSet,
)
from apps.package.enums import (
    PublisherPackageStatusEnum,
    SchoolPackageStatusEnum,
    CourierPackageStatusEnum
)
from utils.graphene.enums import EnumDescription
from apps.common.schema import ActivityFileType


def publisher_package_qs(info):
    if info.context.user.user_type == User.UserType.PUBLISHER.value:
        return PublisherPackage.objects.filter(publisher=info.context.user.publisher)
    elif info.context.user.user_type == User.UserType.MODERATOR.value:
        return PublisherPackage.objects.all()
    return PublisherPackage.objects.none()


def school_package_qs(info):
    if info.context.user.user_type == User.UserType.SCHOOL_ADMIN.value:
        return SchoolPackage.objects.filter(school=info.context.user)
    elif info.context.user.user_type == User.UserType.MODERATOR.value:
        return SchoolPackage.objects.all()
    return SchoolPackage.objects.none()


def courier_package_qs(info):
    if info.context.user.user_type == User.UserType.MODERATOR.value:
        return CourierPackage.objects.all()
    return CourierPackage.objects.none()


class PublisherPackageBookType(DjangoObjectType):
    class Meta:
        model = PublisherPackageBook
        fields = (
            'id', 'quantity', 'book'
        )


class PublisherPackageBookListType(CustomDjangoListObjectType):
    class Meta:
        model = PublisherPackageBook


class PublisherPackageLogType(DjangoObjectType):
    files = CustomDjangoListField(ActivityFileType, required=False)

    class Meta:
        model = PublisherPackageLog
        fields = ('comment', 'snapshot', 'id')


class PublisherPackageLogListType(CustomDjangoListObjectType):
    class Meta:
        model = PublisherPackageLog
        filterset_class = PublisherPackageLogFilterSet


class PublisherPackageType(DjangoObjectType):
    status = graphene.Field(PublisherPackageStatusEnum, required=True)
    status_display = EnumDescription(source='get_status_display')

    publisher_package_books = DjangoPaginatedListObjectField(
        PublisherPackageBookListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    logs = DjangoPaginatedListObjectField(
        PublisherPackageLogListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def get_custom_queryset(queryset, info):
        return publisher_package_qs(info)

    class Meta:
        model = PublisherPackage
        fields = (
            'id', 'package_id', 'status', 'related_orders', 'publisher',
            'total_price', 'total_quantity'
        )

    @staticmethod
    def resolve_logs(root, info, **kwargs) -> QuerySet:
        return root.publisher_package_logs


class PublisherPackageListType(CustomDjangoListObjectType):
    class Meta:
        model = PublisherPackage
        filterset_class = PublisherPackageFilterSet


class SchoolPackageBookType(DjangoObjectType):
    class Meta:
        model = SchoolPackageBook
        fields = (
            'id', 'quantity', 'book'
        )


class SchoolPackageBookListType(CustomDjangoListObjectType):
    class Meta:
        model = SchoolPackageBook


class SchoolPackageLogType(DjangoObjectType):
    files = CustomDjangoListField(ActivityFileType, required=False)

    class Meta:
        model = SchoolPackageLog
        fields = ('comment', 'snapshot', 'id')


class SchoolPackageLogListType(CustomDjangoListObjectType):
    class Meta:
        model = SchoolPackageLog
        filterset_class = SchoolPackageLogFilterSet


class SchoolPackageType(DjangoObjectType):
    status = graphene.Field(SchoolPackageStatusEnum, required=True)
    status_display = EnumDescription(source='get_status_display')

    school_package_books = DjangoPaginatedListObjectField(
        SchoolPackageBookListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    logs = DjangoPaginatedListObjectField(
        SchoolPackageLogListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def get_custom_queryset(queryset, info):
        return school_package_qs(info)

    class Meta:
        model = SchoolPackage
        fields = (
            'id', 'package_id', 'status', 'related_orders', 'school',
            'total_price', 'total_quantity'
        )

    @staticmethod
    def resolve_logs(root, info, **kwargs) -> QuerySet:
        return root.school_package_logs


class SchoolPackageListType(CustomDjangoListObjectType):
    class Meta:
        model = SchoolPackage
        filterset_class = SchoolPackageFilterSet


class CourierPackageLogType(DjangoObjectType):
    files = CustomDjangoListField(ActivityFileType, required=False)

    class Meta:
        model = CourierPackageLog
        fields = ('comment', 'snapshot', 'id')


class CourierPackageLogListType(CustomDjangoListObjectType):
    class Meta:
        model = SchoolPackageLog
        filterset_class = CourierPackageLogFilterSet


class CourierPackageType(DjangoObjectType):
    status = graphene.Field(CourierPackageStatusEnum, required=True)
    status_display = EnumDescription(source='get_status_display')

    courier_package_books = DjangoPaginatedListObjectField(
        SchoolPackageBookListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    logs = DjangoPaginatedListObjectField(
        PublisherPackageLogListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def get_custom_queryset(queryset, info):
        return courier_package_qs(info)

    @staticmethod
    def resolve_logs(root, info, **kwargs) -> QuerySet:
        return root.courier_package_logs

    class Meta:
        model = CourierPackage
        fields = (
            'id', 'package_id', 'status', 'related_orders', 'total_price', 'total_quantity'
        )


class CourierPackageListType(CustomDjangoListObjectType):
    class Meta:
        model = CourierPackage
        filterset_class = CourierPackageFilterSet


class Query(graphene.ObjectType):
    publisher_package = DjangoObjectField(PublisherPackageType)
    publisher_packages = DjangoPaginatedListObjectField(
        PublisherPackageListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    school_package = DjangoObjectField(SchoolPackageType)
    school_packages = DjangoPaginatedListObjectField(
        SchoolPackageListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    courier_package = DjangoObjectField(CourierPackageType)
    courier_packages = DjangoPaginatedListObjectField(
        CourierPackageListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def resolve_publisher_packages(root, info, **kwargs) -> QuerySet:
        return publisher_package_qs(info)

    @staticmethod
    def resolve_school_packages(root, info, **kwargs) -> QuerySet:
        return school_package_qs(info)

    @staticmethod
    def resolve_courier_packages(root, info, **kwargs) -> QuerySet:
        return courier_package_qs(info)
