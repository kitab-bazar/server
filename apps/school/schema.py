import graphene
from graphene_django import DjangoObjectType
from apps.school.models import School
from apps.school.filters import SchoolFilter
from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination


class SchoolType(DjangoObjectType):
    class Meta:
        model = School
        fields = (
            'id', 'school_name', 'school_email', 'province', 'district',
            'municipality', 'ward_number', 'local_address', 'vat_number', 'pan_number'
        )

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class SchoolListType(CustomDjangoListObjectType):
    class Meta:
        model = School
        filterset_class = SchoolFilter


class Query(graphene.ObjectType):
    school = DjangoObjectField(SchoolType)
    schools = DjangoPaginatedListObjectField(
        SchoolListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )