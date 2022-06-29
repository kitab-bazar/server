import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination
from django.db.models import Sum, Count, F, Q

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
from apps.order.models import Order, BookOrder, OrderWindow
from apps.package.models import SchoolPackage


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
    name = graphene.String()
    verified_users = graphene.Int()
    unverified_users = graphene.Int()


class BooksOrderedAndIncentivesPerDistrict(graphene.ObjectType):
    name = graphene.String()
    no_of_books_ordered = graphene.Int()
    no_of_incentive_books = graphene.Int()


class DeliveriesPerDistrictType(graphene.ObjectType):
    name = graphene.String()
    school_delivered = graphene.Int()


class PaymentPerOrderWindowType(graphene.ObjectType):
    title = graphene.String()
    payment = graphene.Int()


class BooksPerPublisherType(graphene.ObjectType):
    publisher_name = graphene.String()
    number_of_books = graphene.Int()


class BooksPerCategoryType(graphene.ObjectType):
    category = graphene.String()
    number_of_books = graphene.Int()


class BooksPerGradeType(graphene.ObjectType):
    grade = graphene.String()
    number_of_books = graphene.Int()


class BooksPerLanguageType(graphene.ObjectType):
    language = graphene.String()
    number_of_books = graphene.Int()


class BooksPerPublisherPerCategory(graphene.ObjectType):
    publisher_name = graphene.String()
    categories = graphene.List(BooksPerCategoryType)


class BooksAndCostPerSchool(graphene.ObjectType):
    school_name = graphene.String()
    number_of_books_ordered = graphene.Int()
    total_cost = graphene.Int()


class BookCategoriesPerOrderWindowType(graphene.ObjectType):
    title = graphene.String()
    categories = graphene.List(BooksPerCategoryType)


class ReportType(graphene.ObjectType):
    number_of_schools_registered = graphene.Int(description='Number of school registered')
    number_of_schools_verified = graphene.Int(description='Number of schools verified')
    number_of_schools_unverified = graphene.Int(description='Number of schools unVerfied')
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
    books_ordered_and_incentives_per_district = graphene.List(
        BooksOrderedAndIncentivesPerDistrict,
        description='Number of books ordered and number of books incentive distributed per district'
    )
    deliveries_per_district = graphene.List(
        DeliveriesPerDistrictType,
        description='Number of school deliveries by district'
    )
    payment_per_order_window = graphene.List(
        PaymentPerOrderWindowType,
        description='Total payment per order window'
    )
    books_per_publisher = graphene.List(
        BooksPerPublisherType,
        description='Number of books per publisher'
    )
    books_per_category = graphene.List(
        BooksPerCategoryType,
        description='Number of books per category'
    )
    books_per_grade = graphene.List(
        BooksPerGradeType,
        description='Number of books per grade'
    )
    books_per_language = graphene.List(
        BooksPerLanguageType,
        description='Number of books per language'
    )
    books_per_publisher_per_category = graphene.List(
        BooksPerPublisherPerCategory,
        description='Number of books per category for each publisher',
    )
    books_and_cost_per_school = graphene.List(
        BooksAndCostPerSchool,
        description='Number of books and total cost per school'
    )
    book_categories_per_order_window = graphene.List(
        BookCategoriesPerOrderWindowType,
        description='Number of categories books ordered per order window'
    )


class ReportQuery(graphene.ObjectType):
    reports = graphene.Field(ReportType)

    @staticmethod
    def resolve_reports(root, info, **kwargs):
        user_qs = User.objects.all()
        book_qs = Book.objects.filter(is_published=True)
        order_qs = Order.objects.filter(status=Order.Status.COMPLETED.value)
        school_package_qs = SchoolPackage.objects.filter(status=SchoolPackage.Status.DELIVERED.value)
        district_qs = District.objects.all()
        order_window_qs = OrderWindow.objects.filter(orders__status=Order.Status.COMPLETED.value)

        def get_books_per_publisher_per_category():
            books_per_publishers = book_qs.values('publisher__name').annotate(
                publisher_name=F('publisher__name'),
                number_of_books=Count('id'),
                category=F('categories__name')
            )
            publishers = []
            for item in books_per_publishers:
                publishers.append(item['publisher_name'])
            result = []
            for publisher in list(set(publishers)):
                result.append({'publisher_name': publisher, 'categories': []})
            for publisher in result:
                for books_per_publisher in books_per_publishers:
                    if publisher['publisher_name'] == books_per_publisher['publisher_name']:
                        publisher['categories'].append(
                            {
                                'number_of_books': books_per_publisher['number_of_books'],
                                'category': books_per_publisher['category'],
                            }
                        )
            return result

        def get_book_categories_per_order_window():
            order_windows_qs = order_window_qs.values('title').annotate(
                category=F('orders__book_order__book__categories__name'),
                number_of_books=Count('orders__book_order__book__categories__name'),
            )
            order_windows = []
            for item in order_windows_qs:
                order_windows.append(item['title'])
            result = []
            for order_window in list(set(order_windows)):
                result.append({'title': order_window, 'categories': []})
            for order_window in result:
                for item in order_windows_qs:
                    if order_window['title'] == item['title']:
                        order_window['categories'].append(
                            {
                                'number_of_books': item['number_of_books'],
                                'category': item['category'],
                            }
                        )
            return result

        return {
            'number_of_schools_registered': user_qs.filter(user_type=User.UserType.SCHOOL_ADMIN.value).count(),

            'number_of_schools_verified': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, is_verified=True
            ).count(),

            'number_of_schools_unverified': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, is_verified=False
            ).count(),

            'number_of_publishers': user_qs.filter(user_type=User.UserType.PUBLISHER.value).count(),

            'number_of_books_on_the_platform': book_qs.count(),

            'number_of_incentive_books': school_package_qs.filter(total_quantity__gte=10).aggregate(
                total_incentive_books=Sum(F('total_quantity') * 4)
            )['total_incentive_books'],

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

            'users_per_district': district_qs.filter(
                schools__school_user__isnull=False
            ).values('name').annotate(
                verified_users=Count('schools__school_user', filter=Q(schools__school_user__is_verified=True)),
                unverified_users=Count('schools__school_user', filter=Q(schools__school_user__is_verified=False)),
            ),

            'books_ordered_and_incentives_per_district': district_qs.filter(
                schools__school_user__school_packages__isnull=False
            ).values('name').annotate(
                no_of_books_ordered=Sum('schools__school_user__school_packages__total_quantity'),
                no_of_incentive_books=F('no_of_books_ordered') * 4,
            ),

            'deliveries_per_district': district_qs.filter(
                schools__school_user__school_packages__isnull=False,
            ).values('name').annotate(school_delivered=Count('schools__school_user__school_packages')),

            'payment_per_order_window': order_window_qs.values('title').annotate(
                payment=Sum('orders__book_order__price')
            ),

            'books_per_publisher': book_qs.values('publisher__name').annotate(
                number_of_books=Count('id'), publisher_name=F('publisher__name')
            ),

            'books_per_category': book_qs.values('categories__name').annotate(
                number_of_books=Count('id'), category=F('categories__name')
            ),

            'books_per_grade': book_qs.values('grade').annotate(
                number_of_books=Count('id')
            ),

            'books_per_language': book_qs.values('language').annotate(
                number_of_books=Count('id')
            ),

            'books_per_publisher_per_category': get_books_per_publisher_per_category(),

            'books_and_cost_per_school': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value,
                order__status=Order.Status.COMPLETED.value,
            ).values('school__name').annotate(
                number_of_books_ordered=Sum('order__book_order__quantity'),
                school_name=F('school__name'),
                total_cost=Sum('order__book_order__price')
            ),

            'book_categories_per_order_window': get_book_categories_per_order_window(),
        }
