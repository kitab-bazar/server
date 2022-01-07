import graphene
from graphene_django_extras import DjangoObjectType
from apps.publisher.models import Publisher
from apps.publisher.filters import PublisherFilter
from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.pagination import PageGraphqlPaginationWithoutCount
from graphene_django_extras import DjangoObjectField


class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class PublisherListType(CustomDjangoListObjectType):
    class Meta:
        model = Publisher
        filterset_class = PublisherFilter


class Query(graphene.ObjectType):
    publisher = DjangoObjectField(PublisherType)
    publishers = DjangoPaginatedListObjectField(
        PublisherListType,
        pagination=PageGraphqlPaginationWithoutCount(
            page_size_query_param='pageSize'
        )
    )
