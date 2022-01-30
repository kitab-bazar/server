import graphene
from django.db.models import F

from utils.graphene.error_types import CustomErrorType, mutation_is_not_valid
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)
from config.permissions import UserPermissions

from apps.user.models import User
from apps.order.models import CartItem, Order
from apps.order.schema import CartItemType, OrderType
from apps.order.serializers import (
    CartItemSerializer,
    CreateOrderFromCartSerializer,
    PlaceSingleOrderSerializer,
    OrderStatusUpdateSerializer,
)


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

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class CreateCartItem(CartItemMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = CartItemInputType(required=True)
    model = CartItem
    serializer_class = CartItemSerializer
    result = graphene.Field(CartItemType)


class UpdateCartItem(CartItemMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = CartItemInputType(required=True)
        id = graphene.ID(required=True)
    model = CartItem
    serializer_class = CartItemSerializer
    result = graphene.Field(CartItemType)


class DeleteCartItem(CartItemMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = CartItem
    result = graphene.Field(CartItemType)


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


class OrderMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.PUBLISHER.value:
            return qs.filter(book_order__publisher_id=info.context.user.publisher)
            return qs.none()
        elif info.context.user.user_type == User.UserType.ADMIN.value:
            return qs
        return qs.none()


OrderUpdateInputType = generate_input_type_for_serializer(
    'OrderUpdateInputType',
    serializer_class=OrderStatusUpdateSerializer
)


class UpdateOrder(OrderMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = OrderUpdateInputType(required=True)
        id = graphene.ID(required=True)
    model = Order
    serializer_class = OrderStatusUpdateSerializer
    result = graphene.Field(OrderType)
    permissions = [UserPermissions.Permission.UPDATE_ORDER]


class DeleteOrder(OrderMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Order
    result = graphene.Field(OrderType)
    permissions = [UserPermissions.Permission.DELETE_ORDER]


class Mutation(graphene.ObjectType):
    create_cart_item = CreateCartItem.Field()
    update_cart_item = UpdateCartItem.Field()
    delete_cart_item = DeleteCartItem.Field()
    place_order_from_cart = PlaceOrderFromCart.Field()
    place_single_order = PlaceSingleOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()
