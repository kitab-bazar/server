
import graphene
from django.db.models import QuerySet
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.graphene.types import CustomDjangoListObjectType

from apps.package.models import (
    PublisherPackage,
    PublisherPackageBook,
    SchoolPackage,
    SchoolPackageBook,
    CourierPackage
)
from apps.user.models import User
from apps.package.filters import (
    PublisherPackageFilterSet,
    SchoolPackageFilterSet,
    CourierPackageFilterSet,
)


def publisher_package_qs(info):
    if info.context.user.user_type == User.UserType.PUBLISHER.value:
        return PublisherPackage.objects.filter(publisher=info.context.user.publisher)
    elif info.context.user.user_type == User.UserType.MODERATOR.value:
        return PublisherPackage.objects.all()
    return PublisherPackage.objects.none()


def school_package_qs(info):
    if info.context.user.user_type == User.UserType.SCHOOL.value:
        return SchoolPackage.objects.filter(school__user_type=info.context.user.school)
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


class PublisherPackageType(DjangoObjectType):
    publisher_package_books = DjangoPaginatedListObjectField(
        PublisherPackageBookListType,
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
            'id', 'package_id', 'status', 'related_orders'
        )


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


class SchoolPackageType(DjangoObjectType):
    publisher_package_books = DjangoPaginatedListObjectField(
        SchoolPackageBookListType,
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
            'id', 'package_id', 'status', 'related_orders'
        )


class SchoolPackageListType(CustomDjangoListObjectType):
    class Meta:
        model = SchoolPackage
        filterset_class = SchoolPackageFilterSet


class CourierPackageType(DjangoObjectType):
    publisher_package_books = DjangoPaginatedListObjectField(
        SchoolPackageBookListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def get_custom_queryset(queryset, info):
        return courier_package_qs(info)

    class Meta:
        model = CourierPackage
        fields = (
            'id', 'package_id', 'status', 'related_orders', 'school_package_books'
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
    school_package = DjangoObjectField(PublisherPackageType)
    school_packages = DjangoPaginatedListObjectField(
        PublisherPackageListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    courier_package = DjangoObjectField(PublisherPackageType)
    courier_packages = DjangoPaginatedListObjectField(
        PublisherPackageListType,
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
