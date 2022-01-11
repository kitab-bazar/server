import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.publisher.models import Publisher
from apps.publisher.filters import PublisherFilter


class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher
        fields = (
            'id', 'name', 'email', 'province', 'district',
            'municipality', 'ward_number', 'local_address', 'vat_number', 'pan_number'
        )

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
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
