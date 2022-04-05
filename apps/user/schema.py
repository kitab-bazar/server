import graphene
from django.core.cache import cache
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from config.permissions import UserPermissions
from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.graphene.enums import EnumDescription

from apps.payment.schema import Query as PaymentQuery
from apps.order.schema import OrderActivityLogQuery

from .models import User
from .filters import UserFilter
from .enums import UserByTypePermissionEnum, UserTypeEnum


class UserTypeMixin():
    canonical_name = graphene.String(required=True)
    image = graphene.Field(FileFieldType)

    user_type = graphene.Field(UserTypeEnum, required=True)
    user_type_display = EnumDescription(source='get_user_type_display', required=True)

    @staticmethod
    def resolve_canonical_name(root, info):
        return info.context.dl.user.canonical_name.load(root.pk)


class UserType(UserTypeMixin, DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'canonical_name',
        )


class UserMeType(UserTypeMixin, DjangoObjectType):
    class Meta:
        model = User
        skip_registry = True
        fields = (
            'id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'is_active',
            'is_verified',
            'last_login',
            'user_type',
            'publisher',
            'school',
            'phone_number',
            'image',
            'institution',
            'publisher',
            'school',
        )

    allowed_permissions = graphene.List(
        graphene.NonNull(UserByTypePermissionEnum),
        required=True
    )

    @staticmethod
    def resolve_allowed_permissions(root, info):
        return UserPermissions.get_permissions(info.context.request.user.user_type)


class ModeratorQueryUserType(UserTypeMixin, DjangoObjectType):
    payment_credit_sum = graphene.Int()
    payment_debit_sum = graphene.Int()
    total_verified_payment = graphene.Int()
    total_unverified_payment = graphene.Int()
    total_unverified_payment_count = graphene.Int()
    total_verified_payment_count = graphene.Int()
    total_order_pending_price = graphene.Int()
    outstanding_balance = graphene.Int()

    class Meta:
        model = User
        skip_registry = True
        fields = (
            'id',
            'full_name',
            'email',
            'is_active',
            'is_verified',
            'last_login',
            'user_type',
            'phone_number',
            'image',
            'institution',  # TODO: Add dataloader
            'publisher',  # TODO: Add dataloader
            'school',  # TODO: Add dataloader
            'verified_by',  # TODO: Add dataloader
            'date_joined',
            'is_deactivated',
            'is_deactivated_by'
        )


class ModeratorQueryUserListType(CustomDjangoListObjectType):
    class Meta:
        model = User
        filterset_class = UserFilter
        base_type = ModeratorQueryUserType


class ModeratorUserQueryType(graphene.ObjectType):
    user = DjangoObjectField(ModeratorQueryUserType)
    users = DjangoPaginatedListObjectField(
        ModeratorQueryUserListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    deactivated_users = DjangoPaginatedListObjectField(
        ModeratorQueryUserListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def resolve_users(root, info, **kwargs):
        return User.objects.filter(is_deactivated=False).annotate(
            **User.annotate_mismatch_order_statements()
        )

    @staticmethod
    def resolve_deactivated_users(root, info, **kwargs):
        return User.objects.filter(is_deactivated=True).annotate(
            **User.annotate_mismatch_order_statements()
        )


class ModeratorQueryType(
    # ---Start --Moderator scopped entities
    ModeratorUserQueryType,
    PaymentQuery,
    # ---End --Moderator scopped entities
    OrderActivityLogQuery,
    graphene.ObjectType
):
    pass


class Query(graphene.ObjectType):
    me = graphene.Field(UserMeType)
    moderator_query = graphene.Field(ModeratorQueryType)

    def resolve_me(parent, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None

    def resolve_moderator_query(parent, info):
        if info.context.user.user_type == User.UserType.MODERATOR:
            return {}
