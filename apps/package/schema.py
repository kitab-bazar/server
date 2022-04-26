
import graphene
from django.db.models import QuerySet
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.fields import DjangoPaginatedListObjectField, CustomDjangoListField
from utils.graphene.types import CustomDjangoListObjectType, FileFieldType

from apps.package.models import (
    PublisherPackage,
    PublisherPackageBook,
    SchoolPackage,
    SchoolPackageBook,
    CourierPackage,
    PublisherPackageLog,
    SchoolPackageLog,
    CourierPackageLog,
    InstitutionPackage,
    InstitutionPackageBook,
    InstitutionPackageLog,
)
from apps.user.models import User
from apps.package.filters import (
    PublisherPackageFilterSet,
    SchoolPackageFilterSet,
    CourierPackageFilterSet,
    PublisherPackageLogFilterSet,
    SchoolPackageLogFilterSet,
    CourierPackageLogFilterSet,
    InstitutionPackageFilterSet,
    InstitutionPackageLogFilterSet,
)
from apps.package.enums import (
    PublisherPackageStatusEnum,
    SchoolPackageStatusEnum,
    CourierPackageStatusEnum,
    InstitutionPackageStatusEnum,
    CourierPackageTypeEnum,
)
from utils.graphene.enums import EnumDescription
from apps.common.schema import ActivityFileType
from apps.order.schema import OrderType
from apps.order.models import Order


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


def institution_package_qs(info):
    if info.context.user.user_type == User.UserType.INSTITUTIONAL_USER.value:
        return InstitutionPackage.objects.filter(institution=info.context.user)
    elif info.context.user.user_type == User.UserType.MODERATOR.value:
        return InstitutionPackage.objects.all()
    return InstitutionPackage.objects.none()


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
    orders_export_file = graphene.Field(FileFieldType)

    @staticmethod
    def get_custom_queryset(queryset, info):
        return publisher_package_qs(info)

    class Meta:
        model = PublisherPackage
        fields = (
            'id', 'package_id', 'status', 'related_orders', 'publisher',
            'total_price', 'total_quantity', 'incentive', 'orders_export_file',
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
            'total_price', 'total_quantity', 'is_eligible_for_incentive'
        )

    @staticmethod
    def resolve_logs(root, info, **kwargs) -> QuerySet:
        return root.school_package_logs


class SchoolPackageListType(CustomDjangoListObjectType):
    class Meta:
        model = SchoolPackage
        filterset_class = SchoolPackageFilterSet


class InstitutionPackageBookType(DjangoObjectType):
    class Meta:
        model = InstitutionPackageBook
        fields = (
            'id', 'quantity', 'book'
        )


class InstitutionPackageBookListType(CustomDjangoListObjectType):
    class Meta:
        model = InstitutionPackageBook


class InstitutionPackageLogType(DjangoObjectType):
    files = CustomDjangoListField(ActivityFileType, required=False)

    class Meta:
        model = InstitutionPackageLog
        fields = ('comment', 'snapshot', 'id')


class InstitutionPackageLogListType(CustomDjangoListObjectType):
    class Meta:
        model = InstitutionPackageLog
        filterset_class = InstitutionPackageLogFilterSet


class InstitutionPackageType(DjangoObjectType):
    status = graphene.Field(InstitutionPackageStatusEnum, required=True)
    status_display = EnumDescription(source='get_status_display')

    institution_package_books = DjangoPaginatedListObjectField(
        InstitutionPackageBookListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    logs = DjangoPaginatedListObjectField(
        InstitutionPackageLogListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def get_custom_queryset(queryset, info):
        return institution_package_qs(info)

    class Meta:
        model = InstitutionPackage
        fields = (
            'id', 'package_id', 'status', 'related_orders', 'institution',
            'total_price', 'total_quantity',
        )

    @staticmethod
    def resolve_logs(root, info, **kwargs) -> QuerySet:
        return root.institution_package_logs


class InstitutionPackageListType(CustomDjangoListObjectType):
    class Meta:
        model = InstitutionPackage
        filterset_class = InstitutionPackageFilterSet


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
    type = graphene.Field(CourierPackageTypeEnum, required=True)
    type_display = EnumDescription(source='get_type_display')

    logs = DjangoPaginatedListObjectField(
        PublisherPackageLogListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    school_packages = DjangoPaginatedListObjectField(
        SchoolPackageListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    institution_packages = DjangoPaginatedListObjectField(
        InstitutionPackageListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    school_courier_package_books = DjangoPaginatedListObjectField(
        SchoolPackageBookListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    institution_courier_package_books = DjangoPaginatedListObjectField(
        InstitutionPackageBookListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    related_orders = CustomDjangoListField(OrderType, required=False)

    @staticmethod
    def get_custom_queryset(queryset, info):
        return courier_package_qs(info)

    @staticmethod
    def resolve_logs(root, info, **kwargs) -> QuerySet:
        return root.courier_package_logs

    @staticmethod
    def resolve_school_courier_package_books(root, info, **kwargs) -> QuerySet:
        # TODO: Use dataloader
        return SchoolPackageBook.objects.filter(school_package__courier_package=root.id)

    @staticmethod
    def resolve_related_orders(root, info, **kwargs) -> QuerySet:
        # TODO: use dataloader
        school_package_ids = SchoolPackage.objects.filter(courier_package=root.id).values_list('id', flat=True)
        if root.type == CourierPackage.Type.SCHOOL.value:
            return Order.objects.filter(
                school_related_orders__in=school_package_ids
            )
            # return root.courier_package.first().related_orders.all()
        elif root.type == CourierPackage.Type.INSTITUTION.value:
            institution_package_ids = InstitutionPackage.objects.filter(courier_package=root.id).values_list('id', flat=True)
            return root.institution_courier_package.first().related_orders.all()
            return Order.objects.filter(
                institution_related_orders__in=institution_package_ids
            )
        return CourierPackage.objects.none()

    class Meta:
        model = CourierPackage
        fields = (
            'id', 'package_id', 'status', 'total_price', 'total_quantity', 'municipality',
            'related_orders', 'is_eligible_for_incentive', 'type'
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
    institution_package = DjangoObjectField(InstitutionPackageType)
    institution_packages = DjangoPaginatedListObjectField(
        InstitutionPackageListType,
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

    @staticmethod
    def resolve_institution_packages(root, info, **kwargs) -> QuerySet:
        return institution_package_qs(info)
