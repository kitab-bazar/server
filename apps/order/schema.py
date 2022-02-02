import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination

from django.db.models import QuerySet
from django.db.models import F, Sum

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.order.models import CartItem, Order, BookOrder
from apps.order.filters import BookOrderFilterSet, OrderFilterSet


def get_cart_items_qs(info):
    return CartItem.objects.filter(created_by=info.context.user).annotate(
        total_price=F('book__price') * F('quantity')
    )


def get_orders_qs(info):
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

    class Meta:
        fields = (
            'grand_total_price',
        )

    @staticmethod
    def resolve_grand_total_price(root, info, **kwargs) -> QuerySet:
        return get_cart_items_qs(info).aggregate(Sum('total_price'))['total_price__sum']


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

    class Meta:
        model = Order
        fields = ('id', 'order_code', 'total_price', 'created_by', 'status')

    def resolve_book_orders(root, info, **kwargs):
        return root.book_order


class OrderListType(CustomDjangoListObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilterSet


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

    @staticmethod
    def resolve_cart_grand_total_price(root, info, **kwargs) -> QuerySet:
        return get_cart_items_qs(info).aggregate(Sum('total_price'))['total_price__sum']

    @staticmethod
    def resolve_orders(root, info, **kwargs) -> QuerySet:
        return get_orders_qs(info)
