import graphene
from typing import Union
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination, DjangoObjectField

from django.db.models import QuerySet, F, Sum
from django.db.models.fields import DateField
from django.db.models.functions import Cast

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField, CustomDjangoListField

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
)
from .enums import OrderStatusEnum


def get_cart_items_qs(info):
    return CartItem.objects.filter(created_by=info.context.user).annotate(
        total_price=F('book__price') * F('quantity')
    )


def get_orders_qs(info):
    def _qs():
        if info.context.user.user_type == User.UserType.PUBLISHER.value:
            return Order.objects.filter(book_order__publisher=info.context.user.publisher)
        elif info.context.user.user_type == User.UserType.MODERATOR.value:
            return Order.objects.all()
        return Order.objects.filter(created_by=info.context.user)
    # Making sure only distinct orders are fetched
    return _qs().distinct()


class OrderWindowType(DjangoObjectType):
    class Meta:
        model = OrderWindow
        fields = ('id', 'title', 'description', 'start_date', 'end_date')


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
    class Meta:
        model = BookOrder
        fields = ('id', 'title', 'price', 'quantity', 'isbn', 'edition', 'price', 'image')
    image = graphene.Field(FileFieldType)


class BookOrderListType(CustomDjangoListObjectType):
    class Meta:
        model = BookOrder
        filterset_class = BookOrderFilterSet


class OrderActivityLogType(DjangoObjectType):
    class Meta:
        model = OrderActivityLog


class OrderType(DjangoObjectType):
    book_orders = DjangoPaginatedListObjectField(
        BookOrderListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    total_quantity = graphene.Int()
    status = graphene.Field(OrderStatusEnum)
    activity_log = graphene.List(graphene.NonNull(OrderActivityLogType))

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
        return root.book_order

    @staticmethod
    def resolve_total_quantity(root, info, **kwargs):
        return root.book_order.aggregate(Sum('quantity'))['quantity__sum']


class OrderListType(CustomDjangoListObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilterSet


class OrderStatisticType(graphene.ObjectType):
    order_placed_at_date = graphene.Date()
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
            order_placed_at__gte=stat_from,
            order_placed_at__lte=stat_to
        ).count()

    @staticmethod
    def resolve_total_books_ordered(root, info, **kwargs):
        '''
        Returns total books ordered in last 3 months
        '''
        stat_from, stat_to = get_stat_daterange()
        return root.filter(
            status=Order.Status.COMPLETED.value,
            order_placed_at__gte=stat_from,
            order_placed_at__lte=stat_to
        ).aggregate(Sum('book_order__quantity'))['book_order__quantity__sum']

    @staticmethod
    def resolve_stat(root, info, **kwargs):
        '''
        Returns order stat of in last 3 months
        '''
        stat_from, stat_to = get_stat_daterange()
        return root.filter(
            status=Order.Status.COMPLETED.value,
            order_placed_at__gte=stat_from,
            order_placed_at__lte=stat_to
        ).annotate(order_placed_at_date=Cast('created_at', DateField())).values('order_placed_at_date').annotate(
            total_quantity=Sum('book_order__quantity')
        ).values('order_placed_at_date', 'total_quantity')


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
    def resolve_order_window_active(root, info, **kwargs) -> Union[None, OrderWindow]:
        return OrderWindow.get_active_window()

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
