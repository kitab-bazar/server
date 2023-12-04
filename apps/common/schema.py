from collections import defaultdict

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
    book_id = graphene.NonNull(graphene.ID)
    title = graphene.NonNull(graphene.String)
    sold_count = graphene.NonNull(graphene.Int)


class TopSchoolType(graphene.ObjectType):
    school_id = graphene.NonNull(graphene.ID)
    school_name = graphene.NonNull(graphene.String)
    book_ordered_count = graphene.NonNull(graphene.Int)


class UserPerDistrictType(graphene.ObjectType):
    district_id = graphene.NonNull(graphene.ID)
    name = graphene.NonNull(graphene.String)
    verified_users = graphene.NonNull(graphene.Int)
    unverified_users = graphene.NonNull(graphene.Int)


class BooksOrderedAndIncentivesPerDistrict(graphene.ObjectType):
    district_id = graphene.NonNull(graphene.ID)
    name = graphene.NonNull(graphene.String)
    no_of_books_ordered = graphene.NonNull(graphene.Int)
    no_of_incentive_books = graphene.NonNull(graphene.Int)


class DeliveriesPerDistrictType(graphene.ObjectType):
    district_id = graphene.NonNull(graphene.ID)
    name = graphene.NonNull(graphene.String)
    school_delivered = graphene.NonNull(graphene.Int)


class PaymentPerOrderWindowType(graphene.ObjectType):
    order_window_id = graphene.NonNull(graphene.ID)
    title = graphene.NonNull(graphene.String)
    payment = graphene.NonNull(graphene.Int)


class BooksPerPublisherType(graphene.ObjectType):
    publisher_id = graphene.NonNull(graphene.ID)
    publisher_name = graphene.NonNull(graphene.String)
    number_of_books = graphene.NonNull(graphene.Int)


class BooksPerCategoryType(graphene.ObjectType):
    category_id = graphene.NonNull(graphene.ID)
    category = graphene.NonNull(graphene.String)
    number_of_books = graphene.NonNull(graphene.Int)


class BooksPerGradeType(graphene.ObjectType):
    grade = graphene.NonNull(graphene.String)
    number_of_books = graphene.NonNull(graphene.Int)


class BooksPerLanguageType(graphene.ObjectType):
    language = graphene.NonNull(graphene.String)
    number_of_books = graphene.NonNull(graphene.Int)


class BooksPerPublisherPerCategory(graphene.ObjectType):
    publisher_id = graphene.NonNull(graphene.ID)
    publisher_name = graphene.NonNull(graphene.String)
    categories = graphene.List(graphene.NonNull(BooksPerCategoryType))


class BooksAndCostPerSchool(graphene.ObjectType):
    school_id = graphene.NonNull(graphene.ID)
    school_name = graphene.NonNull(graphene.String)
    number_of_books_ordered = graphene.NonNull(graphene.Int)
    total_cost = graphene.NonNull(graphene.Int)


class BookCategoriesPerOrderWindowType(graphene.ObjectType):
    order_window_id = graphene.NonNull(graphene.ID)
    title = graphene.NonNull(graphene.String)
    grades = graphene.List(graphene.NonNull(BooksPerGradeType))


class ReportType(graphene.ObjectType):
    number_of_schools_registered = graphene.NonNull(graphene.Int, description='Number of school registered')
    number_of_schools_verified = graphene.NonNull(graphene.Int, description='Number of schools verified')
    number_of_schools_unverified = graphene.NonNull(graphene.Int, description='Number of schools unVerfied')
    number_of_publishers = graphene.NonNull(graphene.Int, description='Number of publishers')
    number_of_books_on_the_platform = graphene.NonNull(graphene.Int, description='Number of books on the Platform')
    number_of_incentive_books = graphene.Int(description='Number of Incentive books')
    number_of_books_ordered = graphene.NonNull(graphene.Int, description='Number of books Ordered')
    number_of_districts_reached = graphene.NonNull(graphene.Int, description='Number of districts reached')
    number_of_municipalities = graphene.NonNull(graphene.Int, description='Number of municipalities')
    number_of_schools_reached = graphene.NonNull(graphene.Int, description='Number of schools reached')
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
    book_grades_per_order_window = graphene.List(
        BookCategoriesPerOrderWindowType,
        description='Number of grades books ordered per order window'
    )


class SchoolReportType(graphene.ObjectType):
    number_of_books_ordered = graphene.Int(description='Number of books Ordered')
    number_of_incentive_books = graphene.Int(description='Number of Incentive books')
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


def get_books_per_publisher_per_category(book_qs, school_report=False):
    if school_report:
        books_per_publishers = book_qs.values('publisher__name').annotate(
            publisher_name=F('publisher__name'),
            number_of_books=Sum('ordered_book__quantity'),
            category=F('categories__name'),
            category_id=F('categories__id'),
            publisher_id=F('publisher__id')
        )
    else:
        books_per_publishers = book_qs.values('publisher__name').annotate(
            publisher_name=F('publisher__name'),
            number_of_books=Count('id'),
            category=F('categories__name'),
            category_id=F('categories__id'),
            publisher_id=F('publisher__id')
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
                publisher['publisher_id'] = books_per_publisher['publisher_id']
                publisher['categories'].append(
                    {
                        'number_of_books': books_per_publisher['number_of_books'],
                        'category': books_per_publisher['category'],
                        'category_id': books_per_publisher['category_id'],
                    }
                )
    return result


def get_book_grades_per_order_window(order_qs, order_window_qs):
    order_window_title_by_id = {
        _id: title
        for _id, title in order_window_qs.values_list('id', 'title').order_by('id')
    }

    order_qs = order_qs.filter(
        book_order__book__grade__isnull=False,
    ).values(
        'assigned_order_window',
        'book_order__book__grade',
    ).annotate(
        number_of_books=Sum('book_order__quantity'),
    ).values_list(
        'assigned_order_window',
        'book_order__book__grade',
        'number_of_books',
    ).order_by(
        'assigned_order_window',
        'book_order__book__grade',
    )

    # Group grades by order_window (Grades are sorted from db)
    grades_by_order_window_id = defaultdict(list)
    for od_id, grade, number_of_books in order_qs:
        grades_by_order_window_id[od_id].append(dict(
            grade=Book.Grade(grade).label,  # Sending label instead of ENUM value
            number_of_books=number_of_books,
        ))

    return [
        # Order Window
        dict(
            order_window_id=order_window_id,
            title=order_window_title,
            grades=grades_by_order_window_id.get(order_window_id, []),
        )
        for order_window_id, order_window_title in order_window_title_by_id.items()
    ]


def get_book_grade_qs(book_qs, school_report=False):
    if school_report:
        grade_data = book_qs.filter(grade__isnull=False).values('grade').annotate(
            number_of_books=Sum('ordered_book__quantity')
        )
    else:
        grade_data = book_qs.filter(grade__isnull=False).values('grade').annotate(
            number_of_books=Count('id')
        )
    formatted_grade_data = [
        {
            'grade': Book.Grade(record['grade']).label,
            'number_of_books': record['number_of_books']
        } for record in grade_data
    ]
    return sorted(formatted_grade_data, key=lambda x: x['grade'])


def get_book_languages(book_qs, school_report=False):
    if school_report:
        languages_data = book_qs.filter(language__isnull=False).values('language').annotate(
            number_of_books=Sum('ordered_book__quantity')
        )
    else:
        languages_data = book_qs.filter(language__isnull=False).values('language').annotate(
            number_of_books=Count('id')
        )
    formatted_languages_data = [
        {
            'language': Book.LanguageType(record['language']).label,
            'number_of_books': record['number_of_books']
        } for record in languages_data
    ]
    return sorted(formatted_languages_data, key=lambda x: x['language'])


class ReportQuery(graphene.ObjectType):
    reports = graphene.Field(ReportType)

    @staticmethod
    def resolve_reports(root, info, **kwargs):
        user_qs = User.objects.filter(is_deactivated=False)
        book_qs = Book.objects.filter(is_published=True)
        order_qs = Order.objects.filter(status=Order.Status.COMPLETED.value)
        school_package_qs = SchoolPackage.objects.filter(status=SchoolPackage.Status.DELIVERED.value)
        district_qs = District.objects.all()
        order_window_qs = OrderWindow.objects.all()

        return {
            'number_of_schools_registered': user_qs.filter(user_type=User.UserType.SCHOOL_ADMIN.value).count(),

            'number_of_schools_verified': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, is_verified=True, is_deactivated=False
            ).count(),

            'number_of_schools_unverified': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, is_verified=False, is_deactivated=False
            ).count(),

            'number_of_publishers': user_qs.filter(user_type=User.UserType.PUBLISHER.value).count(),

            'number_of_books_on_the_platform': book_qs.count(),

            'number_of_incentive_books': school_package_qs.aggregate(
                total_incentive_books=Sum(
                    SchoolPackage.incentive_query_generator()
                )
            )['total_incentive_books'],

            'number_of_books_ordered': order_qs.aggregate(total=Sum('book_order__quantity'))['total'],

            'number_of_districts_reached': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value, order__isnull=False
            ).values('school__district').annotate(total=Count('school__district')).order_by('total').count(),

            'number_of_municipalities': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value,
                order__isnull=False,
                order__status=Order.Status.COMPLETED.value
            ).values('school__municipality').distinct().count(),


            'number_of_schools_reached': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value,
                order__status=Order.Status.COMPLETED.value
            ).distinct().count(),

            'top_selling_books': BookOrder.objects.filter(
                order__status=Order.Status.COMPLETED.value
            ).values('title').annotate(
                sold_count=Count('title'),
                book_id=F('book_id'),
            ).order_by('-sold_count')[:5],

            'top_schools': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value,
                order__status=Order.Status.COMPLETED.value,
            ).annotate(
                book_ordered_count=Sum('order__book_order__quantity'),
                school_name=F('school__name'),
            ).order_by('-book_ordered_count')[:5].values('school_name', 'school_id', 'book_ordered_count'),

            'users_per_district': district_qs.filter(
                schools__school_user__isnull=False, schools__school_user__is_deactivated=False
            ).values('name').annotate(
                district_id=F('id'),
                verified_users=Count('schools__school_user', filter=Q(schools__school_user__is_verified=True)),
                unverified_users=Count('schools__school_user', filter=Q(schools__school_user__is_verified=False)),
            ),

            'books_ordered_and_incentives_per_district': district_qs.filter(
                schools__school_user__school_packages__isnull=False
            ).values('name').annotate(
                no_of_books_ordered=Sum('schools__school_user__school_packages__total_quantity'),
                no_of_incentive_books=Sum(
                    SchoolPackage.incentive_query_generator(prefix='schools__school_user__school_packages__')
                ),
                district_id=F('id')
            ),

            'deliveries_per_district': district_qs.filter(
                schools__school_user__school_packages__isnull=False,
            ).values('name').annotate(
                school_delivered=Count('schools__school_user__school_packages'),
                district_id=F('id')
            ),

            'payment_per_order_window': order_qs.values('assigned_order_window__title').annotate(
                payment=Sum(F('book_order__price') * F('book_order__quantity')),
                order_window_id=F('assigned_order_window__id'),
                title=F('assigned_order_window__title'),
            ).order_by('assigned_order_window__id'),

            'books_per_publisher': book_qs.values('publisher__name').annotate(
                number_of_books=Count('id'),
                publisher_name=F('publisher__name'),
                publisher_id=F('publisher__id')
            ),

            'books_per_category': book_qs.values('categories__name').annotate(
                number_of_books=Count('id'),
                category=F('categories__name'),
                category_id=F('categories__id'),
            ),

            'books_per_grade': get_book_grade_qs(book_qs),

            'books_per_language': get_book_languages(book_qs),
            'books_per_publisher_per_category': get_books_per_publisher_per_category(book_qs),

            'books_and_cost_per_school': user_qs.filter(
                user_type=User.UserType.SCHOOL_ADMIN.value,
                order__status=Order.Status.COMPLETED.value,
            ).values('school__name').annotate(
                number_of_books_ordered=Sum('order__book_order__quantity'),
                school_name=F('school__name'),
                school_id=F('school__id'),
                total_cost=Sum(F('order__book_order__price') * F('order__book_order__quantity'))
            ),

            'book_grades_per_order_window': get_book_grades_per_order_window(order_qs, order_window_qs),
        }


class ScholReportQuery(graphene.ObjectType):
    reports = graphene.Field(SchoolReportType)

    @staticmethod
    def resolve_reports(root, info, **kwargs):
        order_qs = Order.objects.filter(created_by=info.context.user, status=Order.Status.COMPLETED.value)
        school_package_qs = SchoolPackage.objects.filter(
            status=SchoolPackage.Status.DELIVERED.value,
            school=info.context.user
        )
        order_window_qs = OrderWindow.objects.filter(
            orders__status=Order.Status.COMPLETED.value,
            orders__created_by=info.context.user
        )
        book_qs = Book.objects.filter(
            is_published=True,
            ordered_book__order__status=Order.Status.COMPLETED.value,
            ordered_book__order__created_by=info.context.user
        )

        return {
            'number_of_books_ordered': order_qs.aggregate(total=Sum('book_order__quantity'))['total'],
            'number_of_incentive_books': school_package_qs.aggregate(
                total_incentive_books=Sum(
                    SchoolPackage.incentive_query_generator()
                ),
            )['total_incentive_books'],
            'payment_per_order_window': order_window_qs.values('title').annotate(
                payment=Sum(F('orders__book_order__price') * F('orders__book_order__quantity')),
                order_window_id=F('id')
            ),
            'books_per_publisher': book_qs.values('publisher__name').annotate(
                number_of_books=Sum('ordered_book__quantity'),
                publisher_name=F('publisher__name'),
                publisher_id=F('publisher__id')
            ),

            'books_per_category': book_qs.values('categories__name').annotate(
                number_of_books=Sum('ordered_book__quantity'),
                category=F('categories__name'),
                category_id=F('categories__id'),
            ),

            'books_per_grade': get_book_grade_qs(book_qs, school_report=True),

            'books_per_language': get_book_languages(book_qs, school_report=True),

            'books_per_publisher_per_category': get_books_per_publisher_per_category(book_qs, school_report=True),
        }
