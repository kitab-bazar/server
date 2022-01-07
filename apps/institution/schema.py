import graphene
from graphene_django import DjangoObjectType
from apps.institution.models import Institution
from apps.institution.filters import InstitutionFilter
from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.graphene.pagination import PageGraphqlPaginationWithoutCount
from graphene_django_extras import DjangoObjectField


class InstitutionType(DjangoObjectType):
    class Meta:
        model = Institution

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class InstitutionListType(CustomDjangoListObjectType):
    class Meta:
        model = Institution
        filterset_class = InstitutionFilter


class Query(graphene.ObjectType):
    institution = DjangoObjectField(InstitutionType)
    institutions = DjangoPaginatedListObjectField(
        InstitutionListType,
        pagination=PageGraphqlPaginationWithoutCount(
            page_size_query_param='pageSize'
        )
    )
