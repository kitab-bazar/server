import graphene
import datetime
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination

from django.db.models import QuerySet
from django.db.models import F, Sum

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField, CustomDjangoListField

from apps.order.models import CartItem, Order, BookOrder
from apps.order.filters import BookOrderFilterSet, OrderFilterSet
from apps.user.models import User
from apps.book.models import Book


def get_cart_items_qs(info):
    return CartItem.objects.filter(created_by=info.context.user).annotate(
        total_price=F('book__price') * F('quantity')
    )


def get_orders_qs(info):
    if info.context.user.user_type == User.UserType.PUBLISHER.value:
        return Order.objects.filter(book_order__publisher=info.context.user.publisher)
    elif info.context.user.user_type == User.UserType.ADMIN.value:
        return Order.objects.all()
    return Order.objects.filter(created_by=info.context.user)


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


class OrderType(DjangoObjectType):
    book_orders = DjangoPaginatedListObjectField(
        BookOrderListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    total_quantity = graphene.Int()

    class Meta:
        model = Order
        fields = ('id', 'order_code', 'total_price', 'created_by', 'status')

    def resolve_book_orders(root, info, **kwargs):
        return root.book_order

    def resolve_total_quantity(root, info, **kwargs):
        return root.book_order.aggregate(Sum('quantity'))['quantity__sum']


class OrderListType(CustomDjangoListObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilterSet


class OrderStatisticType(graphene.ObjectType):
    id = graphene.Int()
    total_price = graphene.Int()
    total_quantity = graphene.Int()


class OrderStatType(graphene.ObjectType):
    books_uploaded_count = graphene.Int(description='Total books upload count')
    orders_completed_count = graphene.Int(description='Total orders completed count in last 3 months')
    books_ordered_count = graphene.Int(description='Total books ordered count in last 3 months')
    stat = CustomDjangoListField(OrderStatisticType)

    class Meta:
        fields = ()

    @staticmethod
    def resolve_books_uploaded_count(root, info, **kwargs):
        '''
        Returns total books uploaded count
        '''
        if info.context.user.user_type == User.UserType.ADMIN.value:
            return Book.objects.count()
        elif info.context.user.user_type == User.UserType.PUBLISHER.value:
            return Book.objects.filter(publisher=info.context.user.publisher).count()
        return Book.objects.filter(created_by=info.context.user).count()

    @staticmethod
    def resolve_orders_completed_count(root, info, **kwargs):
        '''
        Returns total orders completed in last 3 months
        '''
        stat_to = datetime.date.today()
        stat_from = stat_to - datetime.timedelta(30)
        return root.filter(
            status=Order.OrderStatus.COMPLETED.value,
            order_placed_at__gte=stat_from,
            order_placed_at__lte=stat_to
        ).count()

    @staticmethod
    def resolve_books_ordered_count(root, info, **kwargs):
        '''
        Returns total books ordered in last 3 months
        '''
        stat_to = datetime.date.today()
        stat_from = stat_to - datetime.timedelta(30)
        return root.filter(
            status=Order.OrderStatus.COMPLETED.value,
            order_placed_at__gte=stat_from,
            order_placed_at__lte=stat_to
        ).count()

    @staticmethod
    def resolve_stat(root, info, **kwargs):
        '''
        Returns order stat of in last 3 months
        '''
        stat_to = datetime.date.today()
        stat_from = stat_to - datetime.timedelta(30)
        return root.filter(
            status=Order.OrderStatus.COMPLETED.value,
            order_placed_at__gte=stat_from,
            order_placed_at__lte=stat_to
        ).annotate(
            total_quantity=Sum('book_order__quantity')
        ).values('id', 'total_price', 'total_quantity')


class Query(graphene.ObjectType):
    cart_items = DjangoPaginatedListObjectField(
        CartType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    orders = DjangoPaginatedListObjectField(
        OrderListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    order_stat = graphene.Field(OrderStatType)

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
