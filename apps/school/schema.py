import graphene
from graphene_django_extras import DjangoObjectType
from apps.school.models import School
from apps.school.filters import SchoolFilter
from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.pagination import PageGraphqlPaginationWithoutCount
from graphene_django_extras import DjangoObjectField


class SchoolType(DjangoObjectType):
    class Meta:
        model = School

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
        pagination=PageGraphqlPaginationWithoutCount(
            page_size_query_param='pageSize'
        )
    )
