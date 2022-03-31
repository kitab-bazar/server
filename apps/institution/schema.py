import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.institution.models import Institution
from apps.institution.filters import InstitutionFilter


class InstitutionType(DjangoObjectType):
    class Meta:
        model = Institution
        fields = (
            'id', 'name', 'municipality', 'ward_number', 'local_address',
            'vat_number', 'pan_number', 'logo_url', 'website_url', 'library_url',
        )

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
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
