import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.school.models import School
from apps.user.models import User
from apps.school.filters import SchoolFilter
from apps.payment.schema import Query as PaymentQuery
from apps.common.schema import ScholReportQuery


class SchoolType(DjangoObjectType):
    class Meta:
        model = School
        fields = (
            'id', 'name', 'municipality', 'ward_number', 'local_address',
            'vat_number', 'pan_number', 'school_id'
        )

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class SchoolListType(CustomDjangoListObjectType):
    class Meta:
        model = School
        filterset_class = SchoolFilter


class SchoolQueryType(
    PaymentQuery,
    ScholReportQuery,
):
    pass


class Query(graphene.ObjectType):
    school_query = graphene.Field(SchoolQueryType)
    school = DjangoObjectField(SchoolType)
    schools = DjangoPaginatedListObjectField(
        SchoolListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    def resolve_school_query(parent, info):
        if info.context.user.user_type == User.UserType.SCHOOL_ADMIN:
            return {}
