import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination
from django.db.models import QuerySet
from django.db.models import F, Sum

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.order.models import CartItem


def get_cart_items_qs(info):
    return CartItem.objects.filter(created_by=info.context.user).annotate(
        total_price=F('book__price') * F('quantity')
    )


class CartItemType(DjangoObjectType):
    total_price = graphene.Int()

    class Meta:
        model = CartItem
        fields = ('id', 'book', 'quantity', 'total_price')

    @staticmethod
    def get_custom_queryset(queryset, info, **kwargs):
        return get_cart_items_qs(info)

    @staticmethod
    def resolve_total_price(root, info, **kwargs) -> QuerySet:
        return root.total_price


class CartGrandTotalType(graphene.ObjectType):
    grand_total_price = graphene.Int()

    class Meta:
        fields = (
            'grand_total_price'
        )

    @staticmethod
    def resolve_grand_total_price(root, info, **kwargs) -> QuerySet:
        return get_cart_items_qs(info).aggregate(Sum('total_price'))['total_price__sum']


class CartItemListType(CustomDjangoListObjectType):
    class Meta:
        model = CartItem


class CartType(CartItemListType, CartGrandTotalType):
    class Meta:
        model = CartItem


class Query(graphene.ObjectType):
    cart_items = DjangoPaginatedListObjectField(
        CartType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def resolve_cart_items(root, info, **kwargs) -> QuerySet:
        return get_cart_items_qs(info)

    @staticmethod
    def resolve_cart_grand_total_price(root, info, **kwargs) -> QuerySet:
        return get_cart_items_qs(info).aggregate(Sum('total_price'))['total_price__sum']
