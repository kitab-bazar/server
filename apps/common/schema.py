import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.common.models import District, Province, Municipality, ActivityLogFile
from apps.common.filters import (
    DistrictFilter,
    ProvinceFilter,
    MunicipalityFilter,
)


class ProvinceType(DjangoObjectType):
    class Meta:
        model = Province
        fields = ('id', 'name',)


class ProvinceListType(CustomDjangoListObjectType):
    class Meta:
        model = Province
        filterset_class = ProvinceFilter


class MunicipalityType(DjangoObjectType):
    class Meta:
        model = Municipality
        fields = ('id', 'name', 'province', 'district')

    @staticmethod
    def get_queryset(queryset, info):
        return queryset.select_related('province', 'district')


class MunicipalityListType(CustomDjangoListObjectType):
    class Meta:
        model = Municipality
        filterset_class = MunicipalityFilter


class DistrictType(DjangoObjectType):
    class Meta:
        model = District
        fields = ('id', 'name', 'province',)

    @staticmethod
    def get_queryset(queryset, info):
        return queryset.select_related('province')


class DistrictListType(CustomDjangoListObjectType):
    class Meta:
        model = District
        filterset_class = DistrictFilter


class ActivityFileType(DjangoObjectType):
    class Meta:
        model = ActivityLogFile
        fields = ('id', 'file',)

    file = graphene.Field(FileFieldType)


class Query(graphene.ObjectType):
    province = DjangoObjectField(ProvinceType)
    provinces = DjangoPaginatedListObjectField(
        ProvinceListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    municipality = DjangoObjectField(MunicipalityType)
    municipalities = DjangoPaginatedListObjectField(
        MunicipalityListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    district = DjangoObjectField(DistrictType)
    districts = DjangoPaginatedListObjectField(
        DistrictListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
