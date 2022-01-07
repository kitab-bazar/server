import graphene
from graphene_django_extras import DjangoObjectType
from apps.common.models import District, Province, Municipality
from apps.common.filters import DistrictFilter, ProvinceFilter, MunicipalityFilter
from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.pagination import PageGraphqlPaginationWithoutCount
from graphene_django_extras import DjangoObjectField


class ProvinceType(DjangoObjectType):
    class Meta:
        model = Province
        fields = (
            'id',
            'name',
        )

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class ProvinceListType(CustomDjangoListObjectType):
    class Meta:
        model = Province
        filterset_class = ProvinceFilter


class MunicipalityType(DjangoObjectType):
    class Meta:
        model = Municipality
        fields = (
            'id',
            'name',
        )

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class MunicipalityListType(CustomDjangoListObjectType):
    class Meta:
        model = Municipality
        filterset_class = MunicipalityFilter


class DistrictType(DjangoObjectType):
    class Meta:
        model = District
        fields = (
            'id',
            'name',
        )

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class DistrictListType(CustomDjangoListObjectType):
    class Meta:
        model = District
        filterset_class = DistrictFilter


class Query(graphene.ObjectType):
    province = DjangoObjectField(ProvinceType)
    provinces = DjangoPaginatedListObjectField(
        ProvinceListType,
        pagination=PageGraphqlPaginationWithoutCount(
            page_size_query_param='pageSize'
        )
    )
    municipality = DjangoObjectField(MunicipalityType)
    municipalities = DjangoPaginatedListObjectField(
        MunicipalityListType,
        pagination=PageGraphqlPaginationWithoutCount(
            page_size_query_param='pageSize'
        )
    )
    district = DjangoObjectField(DistrictType)
    districts = DjangoPaginatedListObjectField(
        DistrictListType,
        pagination=PageGraphqlPaginationWithoutCount(
            page_size_query_param='pageSize'
        )
    )
