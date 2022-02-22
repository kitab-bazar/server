import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField
from config.permissions import UserPermissions
from .enums import UserByTypePermissionEnum

from apps.user.models import User
from apps.user.filters import UserFilter
from apps.payment.schema import Query as PaymentQuery


class UserType(DjangoObjectType):

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'full_name',
            'is_active', 'is_verified', 'last_login', 'user_type', 'institution',
            'publisher', 'school', 'image',
        )
    image = graphene.Field(FileFieldType)

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class UserListType(CustomDjangoListObjectType):
    class Meta:
        model = User
        filterset_class = UserFilter


class UserMeType(DjangoObjectType):
    allowed_permissions = graphene.List(graphene.NonNull(UserByTypePermissionEnum), required=True)

    class Meta:
        model = User
        skip_registry = True
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'email',
            'is_active', 'is_verified', 'last_login', 'user_type', 'institution',
            'publisher', 'school', 'phone_number', 'image',
        )
    image = graphene.Field(FileFieldType)

    @staticmethod
    def resolve_allowed_permissions(root, info):
        return UserPermissions.get_permissions(info.context.request.user.user_type)


class ModeratorQueryType(
    # ---Start --Moderator scopped entities
    PaymentQuery,
    # ---End --Moderator scopped entities
    graphene.ObjectType
):

    pass


class Query(graphene.ObjectType):
    me = graphene.Field(UserMeType)
    user = DjangoObjectField(UserType)
    users = DjangoPaginatedListObjectField(
        UserListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    moderator_query = graphene.Field(ModeratorQueryType)

    def resolve_me(parent, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None

    def resolve_moderator_query(parent, info):
        if info.context.user.user_type == User.UserType.MODERATOR:
            return {}
