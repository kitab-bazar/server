import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination
from django.db.models import Sum, Count, F

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.common.models import District, Province, Municipality, ActivityLogFile
from apps.common.filters import (
    DistrictFilter,
    ProvinceFilter,
    MunicipalityFilter,
)
from apps.user.models import User
from apps.book.models import Book
from apps.order.models import Order, BookOrder


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


class TopSellingBookType(graphene.ObjectType):
    title = graphene.String()
    sold_count = graphene.Int()


class TopSchoolType(graphene.ObjectType):
    school_name = graphene.String()
    book_ordered_count = graphene.Int()


class UserPerDistrictType(graphene.ObjectType):
    district_name = graphene.String()
    verified_users = graphene.Int()
    unverified_users = graphene.Int()


class ReportType(graphene.ObjectType):
    number_of_schools_registered = graphene.Int(description='Number of school registered')
    number_of_schools_verified = graphene.Int(description='Number of schools verified')
    number_of_schools_unverfied = graphene.Int(description='Number of schools unVerfied')
    number_of_publishers = graphene.Int(description='Number of publishers')
    number_of_books_on_the_platform = graphene.Int(description='Number of books on the Platform')
    number_of_incentive_books = graphene.Int(description='Number of Incentive books')
    number_of_books_ordered = graphene.Int(description='Number of books Ordered')
    number_of_districts_reached = graphene.Int(description='Number of districts reached')
    number_of_municipalities = graphene.Int(description='Number of municipalities')
    number_of_schools_reached = graphene.Int(description='Number of schools reached')
    top_selling_books = graphene.List(TopSellingBookType, description='Top 5 selling books')
    top_schools = graphene.List(TopSchoolType, description='Top 5 schools/customers with the most books ordered')
    users_per_district = graphene.List(
        UserPerDistrictType, description='Number of uverified users and verified users per district'
    )


class ReportQuery(graphene.ObjectType):
    reports = graphene.Field(ReportType)

    @staticmethod
    def resolve_reports(root, info, **kwargs):
        user_qs = User.objects.all()
        book_qs = Book.objects.filter(is_published=True)
        order_qs = Order.objects.filter(status=Order.Status.COMPLETED.value)

        return {
            'number_of_schools_registered': user_qs.filter(user_type=User.UserType.SCHOOL_ADMIN.value).count(),

            'number_of_schools_verified': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, is_verified=True
            ).count(),

            'number_of_schools_unverfied': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, is_verified=False
            ).count(),

            'number_of_publishers': user_qs.filter(user_type=User.UserType.PUBLISHER.value).count(),

            'number_of_books_on_the_platform': book_qs.count(),

            'number_of_books_ordered': order_qs.aggregate(total=Sum('book_order__quantity'))['total'],

            'number_of_districts_reached': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, order__isnull=False
            ).values('school__district').annotate(total=Count('school__district')).order_by('total').count(),

            'number_of_municipalities': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, order__isnull=False
            ).values('school__municipality').annotate(total=Count('school__municipality')).order_by('total').count(),


            'number_of_schools_reached': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, order__isnull=False
            ).values('school__municipality').annotate(total=Count('school__municipality')).order_by('total').count(),

            'top_selling_books': BookOrder.objects.filter(
                order__status=Order.Status.COMPLETED.value
            ).values('title').annotate(
                sold_count=Count('title')
            ).order_by('-sold_count')[:5],

            'top_schools': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value,
                order__status=Order.Status.COMPLETED.value,
            ).annotate(
                book_ordered_count=Sum('order__book_order__quantity'),
                school_name=F('school__name')
            ).order_by('-book_ordered_count')[:5].values('school_name', 'book_ordered_count'),
        }
