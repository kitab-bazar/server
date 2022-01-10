import graphene
from graphene_django import DjangoObjectType
from apps.publisher.models import Publisher
from apps.publisher.filters import PublisherFilter
from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination


class PublisherType(DjangoObjectType):
    class Meta:
        model = Publisher
        fields = (
            'id', 'publisher_name', 'publisher_email', 'province', 'district',
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