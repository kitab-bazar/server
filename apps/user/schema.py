import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from config.permissions import (
    SchoolPermissions,
    InstitutionPermissions,
    PublisherPermissions,
    BookPermissions,
)
from .enums import (
    SchoolPermissionEnum,
    InstitutionPermissionEnum,
    PublisherPermissionEnum,
    BookPermissionEnum,
)

from apps.user.models import User
from apps.user.filters import UserFilter


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'full_name',
            'is_active', 'last_login', 'user_type', 'institution',
            'publisher', 'school'
        )

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class UserListType(CustomDjangoListObjectType):
    class Meta:
        model = User
        filterset_class = UserFilter


class UserPermissionType(graphene.ObjectType):
    school_permissions = graphene.List(
        graphene.NonNull(
            SchoolPermissionEnum,
        ), required=True
    )
    publisher_permissions = graphene.List(
        graphene.NonNull(
            PublisherPermissionEnum,
        ), required=True
    )
    institution_permissions = graphene.List(
        graphene.NonNull(
            InstitutionPermissionEnum,
        ), required=True
    )
    book_permissions = graphene.List(
        graphene.NonNull(
            BookPermissionEnum,
        ), required=True
    )

    class Meta:
        model = User
        skip_registry = True

    @staticmethod
    def resolve_school_permissions(root, info):
        return SchoolPermissions.get_permissions(info.context.request.user.user_type)

    @staticmethod
    def resolve_publisher_permissions(root, info):
        return PublisherPermissions.get_permissions(info.context.request.user.user_type)

    @staticmethod
    def resolve_institution_permissions(root, info):
        return InstitutionPermissions.get_permissions(info.context.request.user.user_type)

    @staticmethod
    def resolve_book_permissions(root, info):
        return BookPermissions.get_permissions(info.context.request.user.user_type)


class UserMeType(DjangoObjectType):
    allowed_permissions = graphene.Field(UserPermissionType)

    class Meta:
        model = User
        skip_registry = True
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'email',
            'is_active', 'last_login', 'user_type', 'institution',
            'publisher', 'school'
        )

    @staticmethod
    def resolve_allowed_permissions(root, info):
        return UserPermissionType


class Query(graphene.ObjectType):
    me = graphene.Field(UserMeType)
    user = DjangoObjectField(UserType)
    users = DjangoPaginatedListObjectField(
        UserListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    def resolve_me(parent, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
