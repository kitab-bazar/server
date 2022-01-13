import graphene
from graphene_django import DjangoObjectType
from apps.user.models import User
from apps.user.filters import UserFilter
from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'is_active', 'last_login'
        )

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class UserListType(CustomDjangoListObjectType):
    class Meta:
        model = User
        filterset_class = UserFilter


class UserMeType(DjangoObjectType):

    class Meta:
        model = User
        skip_registry = True
        fields = (
            'id', 'first_name', 'last_name', 'full_name', 'email',
            'is_active', 'last_login', 'user_type', 'institution',
            'publisher', 'school'
        )


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
