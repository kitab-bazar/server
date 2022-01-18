import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)
from django.db.models import F

from apps.order.models import CartItem
from apps.order.schema import CartItemType
from apps.order.serializers import CartItemSerializer


CartItemInputType = generate_input_type_for_serializer(
    'CartItemInputType',
    serializer_class=CartItemSerializer
)


class CartItemMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        return qs.filter(created_by=info.context.user).annotate(
            total_price=F('book__price') * F('quantity')
        )


class CreateCartItem(CartItemMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = CartItemInputType(required=True)
    model = CartItem
    serializer_class = CartItemSerializer
    result = graphene.Field(CartItemType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class UpdateCartItem(CartItemMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = CartItemInputType(required=True)
        id = graphene.ID(required=True)
    model = CartItem
    serializer_class = CartItemSerializer
    result = graphene.Field(CartItemType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class DeleteCartItem(CartItemMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = CartItem
    result = graphene.Field(CartItemType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class Mutation(graphene.ObjectType):
    create_cart_item = CreateCartItem.Field()
    update_cart_item = UpdateCartItem.Field()
    delete_cart_item = DeleteCartItem.Field()
