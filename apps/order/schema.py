import graphene
from typing import Union
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination, DjangoObjectField

from django.db.models import QuerySet, F, Sum, Count
from django.db.models.fields import DateField
from django.db.models.functions import Cast

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField, CustomDjangoListField
from utils.graphene.enums import EnumDescription

from apps.user.models import User
from apps.book.models import Book

from .models import (
    CartItem,
    Order,
    BookOrder,
    OrderWindow,
    OrderActivityLog,
)
from .filters import (
    BookOrderFilterSet,
    OrderFilterSet,
    OrderWindowFilterSet,
    OrderActivityLogFilterSet,
)
from .enums import OrderStatusEnum, OrderWindowTypeEnum
from apps.book.enums import BookGradeEnum, BookLanguageEnum


def get_cart_items_qs(info):
    return CartItem.objects.filter(created_by=info.context.user).annotate(
        total_price=F('book__price') * F('quantity')
    )


def get_orders_qs(info):
    def _qs():
        if info.context.user.user_type == User.UserType.PUBLISHER.value:
            return Order.objects.filter(
                book_order__publisher=info.context.user.publisher, created_by__is_deactivated=False
            )
        elif info.context.user.user_type == User.UserType.MODERATOR.value:
            return Order.objects.filter(created_by__is_deactivated=False)
        return Order.objects.filter(created_by=info.context.user)
    # Making sure only distinct orders are fetched
    return _qs().distinct()


class OrderWindowType(DjangoObjectType):
    type = graphene.Field(OrderWindowTypeEnum)

    class Meta:
        model = OrderWindow
        fields = ('id', 'title', 'description', 'start_date', 'end_date', 'type')


class OrderWindowListType(CustomDjangoListObjectType):
    class Meta:
        model = OrderWindow
        filterset_class = OrderWindowFilterSet


class CartItemType(DjangoObjectType):
    total_price = graphene.Int()

    class Meta:
        model = CartItem
        fields = ('id', 'book', 'quantity', 'total_price')

    @staticmethod
    def resolve_total_price(root, info, **kwargs) -> QuerySet:
        return info.context.dl.cart_item.total_price.load(root.pk)


class CartGrandTotalType(graphene.ObjectType):
    grand_total_price = graphene.Int()
    total_quantity = graphene.Int()

    class Meta:
        fields = (
            'grand_total_price',
        )

    @staticmethod
    def resolve_grand_total_price(root, info, **kwargs) -> QuerySet:
        return get_cart_items_qs(info).aggregate(Sum('total_price'))['total_price__sum']

    @staticmethod
    def resolve_total_quantity(root, info, **kwargs):
        return get_cart_items_qs(info).aggregate(Sum('quantity'))['quantity__sum']


class CartType(CustomDjangoListObjectType, CartGrandTotalType):
    class Meta:
        model = CartItem


class BookOrderType(DjangoObjectType):
    grade = graphene.Field(BookGradeEnum)
    grade_display = EnumDescription(source='get_grade_display')

    language = graphene.Field(BookLanguageEnum)
    language_display = EnumDescription(source='get_language_display')

    class Meta:
        model = BookOrder
        fields = (
            'id', 'title', 'price', 'quantity', 'isbn',
            'edition', 'price', 'image', 'language', 'grade', 'publisher'
        )
    image = graphene.Field(FileFieldType)


class BookOrderListType(CustomDjangoListObjectType):
    class Meta:
        model = BookOrder
        filterset_class = BookOrderFilterSet


class OrderActivityLogType(DjangoObjectType):
    class Meta:
        model = OrderActivityLog


class OrderActivityLogListType(CustomDjangoListObjectType):
    class Meta:
        model = OrderActivityLog
        filterset_class = OrderActivityLogFilterSet


class OrderType(DjangoObjectType):
    book_orders = DjangoPaginatedListObjectField(
        BookOrderListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    total_quantity = graphene.Int()
    activity_log = graphene.List(graphene.NonNull(OrderActivityLogType))

    status = graphene.Field(OrderStatusEnum)
    status_display = EnumDescription(source='get_status_display')

    class Meta:
        model = Order
        fields = ('id', 'order_code', 'total_price', 'created_by', 'status', 'created_at')

    @staticmethod
    def get_custom_queryset(queryset, info):
        return get_orders_qs(info)

    @staticmethod
    def resolve_activity_log(root, info, **kwargs):
        # FIXME: Use dataloader
        return root.activity_logs.all()

    @staticmethod
    def resolve_book_orders(root, info, **kwargs):
        return root.book_order.select_related('publisher')

    @staticmethod
    def resolve_total_quantity(root, info, **kwargs):
        return root.book_order.aggregate(Sum('quantity'))['quantity__sum']


class OrderListType(CustomDjangoListObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilterSet


class OrderStatisticType(graphene.ObjectType):
    created_at_date = graphene.Date()
    total_quantity = graphene.Int()


def get_stat_daterange():
    stat_to = timezone.now()
    return stat_to - timezone.timedelta(90), stat_to


class OrderStatType(graphene.ObjectType):
    total_books_uploaded = graphene.Int(description='Total books upload count')
    orders_completed_count = graphene.Int(description='Total orders completed count in last 3 months')
    total_books_ordered = graphene.Int(description='Total books ordered count in last 3 months')
    stat = CustomDjangoListField(OrderStatisticType)

    class Meta:
        fields = ()

    @staticmethod
    def resolve_total_books_uploaded(root, info, **kwargs):
        '''
        Returns total books uploaded count
        '''
        if info.context.user.user_type == User.UserType.MODERATOR.value:
            return Book.objects.count()
        elif info.context.user.user_type == User.UserType.PUBLISHER.value:
            return Book.objects.filter(publisher=info.context.user.publisher).count()
        return Book.objects.filter(created_by=info.context.user).count()

    @staticmethod
    def resolve_orders_completed_count(root, info, **kwargs):
        '''
        Returns total orders completed in last 3 months
        '''
        stat_from, stat_to = get_stat_daterange()
        return root.filter(
            status=Order.Status.COMPLETED.value,
            created_at__gte=stat_from,
            created_at__lte=stat_to
        ).count()

    @staticmethod
    def resolve_total_books_ordered(root, info, **kwargs):
        '''
        Returns total books ordered in last 3 months
        '''
        stat_from, stat_to = get_stat_daterange()
        return root.filter(
            status=Order.Status.COMPLETED.value,
            created_at__gte=stat_from,
            created_at__lte=stat_to
        ).aggregate(Sum('book_order__quantity'))['book_order__quantity__sum']

    @staticmethod
    def resolve_stat(root, info, **kwargs):
        '''
        Returns order stat of in last 3 months
        '''
        stat_from, stat_to = get_stat_daterange()
        return root.filter(
            status=Order.Status.COMPLETED.value,
            created_at__gte=stat_from,
            created_at__lte=stat_to
        ).annotate(created_at_date=Cast('created_at', DateField())).values('created_at_date').annotate(
            total_quantity=Sum('book_order__quantity')
        ).values('created_at_date', 'total_quantity')


class OrderSummaryType(graphene.ObjectType):
    """
    Order summary for current user's pending orders
    """
    total_books = graphene.Int(description='Total books count (Unique book count)')
    total_books_quantity = graphene.Int(description='Total books quantity count. (Order quantity sum)')
    total_price = graphene.Int(description='Total price. (Order price sum)')

    class Meta:
        fields = ()


class Query(graphene.ObjectType):
    cart_items = DjangoPaginatedListObjectField(
        CartType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    order = DjangoObjectField(OrderType)
    orders = DjangoPaginatedListObjectField(
        OrderListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    order_stat = graphene.Field(OrderStatType)
    order_summary = graphene.Field(OrderSummaryType)
    # Order window
    order_window_active = graphene.Field(OrderWindowType)
    order_window = DjangoObjectField(OrderWindowType)
    order_windows = DjangoPaginatedListObjectField(
        OrderWindowListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def resolve_order_summary(root, info, **kwargs):
        current_user = info.context.user
        if current_user.user_type == User.UserType.SCHOOL_ADMIN:
            order_qs = Order.objects.filter(created_by=current_user, status=Order.Status.PENDING)
            return order_qs.aggregate(
                total_books=Count('book_order__book', distinct=True),
                total_books_quantity=Sum('book_order__quantity'),
                total_price=Sum('book_order__total_price'),
            )

    @staticmethod
    def resolve_order_window_active(root, info, **kwargs) -> Union[None, OrderWindow]:
        return OrderWindow.get_active_window(info.context.user)

    @staticmethod
    def resolve_cart_grand_total_price(root, info, **kwargs) -> QuerySet:
        return get_cart_items_qs(info).aggregate(Sum('total_price'))['total_price__sum']

    @staticmethod
    def resolve_orders(root, info, **kwargs) -> QuerySet:
        return get_orders_qs(info)

    @staticmethod
    def resolve_cart_items(root, info, **kwargs) -> QuerySet:
        return get_cart_items_qs(info)

    def resolve_order_stat(root, info, **kwargs):
        if info.context.user.is_authenticated:
            return get_orders_qs(info)
        return None


class OrderActivityLogQuery(graphene.ObjectType):
    order_activity_log = DjangoObjectField(OrderActivityLogType)
    order_activity_logs = DjangoPaginatedListObjectField(
        OrderActivityLogListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
