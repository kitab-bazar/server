import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)
from django.db.models import F

from apps.order.models import CartItem
from apps.order.schema import CartItemType, OrderType
from apps.order.serializers import (
    CartItemSerializer,
    CreateOrderFromCartSerializer,
    PlaceSingleOrderSerializer
)
from utils.graphene.error_types import CustomErrorType, mutation_is_not_valid


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


class PlaceOrderFromCart(graphene.Mutation):
    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info):
        serializer = CreateOrderFromCartSerializer(data=dict(), context={'request': info.context.request})
        if errors := mutation_is_not_valid(serializer):
            return PlaceOrderFromCart(errors=errors, ok=False)
        instance = serializer.save()
        return PlaceOrderFromCart(result=instance, errors=None, ok=True)


PlaceSingleOrderInputType = generate_input_type_for_serializer(
    'PlaceSingleOrderInputType',
    serializer_class=PlaceSingleOrderSerializer
)


class PlaceSingleOrder(graphene.Mutation):
    class Arguments:
        data = PlaceSingleOrderInputType(required=True)
    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info, data):
        serializer = PlaceSingleOrderSerializer(data=data, context={'request': info.context.request})
        if errors := mutation_is_not_valid(serializer):
            return PlaceSingleOrder(errors=errors, ok=False)
        instance = serializer.save()
        return PlaceSingleOrder(result=instance, errors=None, ok=True)


class Mutation(graphene.ObjectType):
    create_cart_item = CreateCartItem.Field()
    update_cart_item = UpdateCartItem.Field()
    delete_cart_item = DeleteCartItem.Field()
    place_order_from_cart = PlaceOrderFromCart.Field()
    place_single_order = PlaceSingleOrder.Field()
