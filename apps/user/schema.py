import graphene
from graphene_django_extras import DjangoObjectType
from apps.user.models import User
from apps.user.filters import UserFilter
from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.pagination import PageGraphqlPaginationWithoutCount
from graphene_django_extras import DjangoObjectField


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ('password',)

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class UserListType(CustomDjangoListObjectType):
    class Meta:
        model = User
        filterset_class = UserFilter
        exclude_fields = ('password',)


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    user = DjangoObjectField(UserType)
    users = DjangoPaginatedListObjectField(
        UserListType,
        pagination=PageGraphqlPaginationWithoutCount(
            page_size_query_param='pageSize'
        )
    )

    def resolve_me(parent, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None
