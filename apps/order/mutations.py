import graphene
from django.db.models import F

from utils.graphene.error_types import CustomErrorType
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
    OrderUpdateSerializer,
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


class CreateCartItem(CartItemMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = CartItemInputType(required=True)
    model = CartItem
    serializer_class = CartItemSerializer
    result = graphene.Field(CartItemType)
    permissions = [UserPermissions.Permission.CAN_CRUD_CART_ITEM]


class UpdateCartItem(CartItemMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = CartItemInputType(required=True)
        id = graphene.ID(required=True)
    model = CartItem
    serializer_class = CartItemSerializer
    result = graphene.Field(CartItemType)
    permissions = [UserPermissions.Permission.CAN_CRUD_CART_ITEM]


class DeleteCartItem(CartItemMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = CartItem
    result = graphene.Field(CartItemType)
    permissions = [UserPermissions.Permission.CAN_CRUD_CART_ITEM]


class CreateOrderFromCart(CreateUpdateGrapheneMutation):
    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(OrderType)
    permissions = [UserPermissions.Permission.CREATE_ORDER]
    serializer_class = CreateOrderFromCartSerializer


class OrderMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        user = info.context.user
        if user.user_type == User.UserType.MODERATOR.value:
            return qs
        elif user.user_type == User.UserType.SCHOOL_ADMIN.value:
            return qs.filter(created_by=user)
        elif user.user_type == User.UserType.INSTITUTIONAL_USER.value:
            return qs.filter(created_by=user)
        return qs.none()


OrderUpdateInputType = generate_input_type_for_serializer(
    'OrderUpdateInputType',
    serializer_class=OrderUpdateSerializer
)


class UpdateOrder(OrderMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = OrderUpdateInputType(required=True)
        id = graphene.ID(required=True)
    model = Order
    serializer_class = OrderUpdateSerializer
    result = graphene.Field(OrderType)
    permissions = [UserPermissions.Permission.UPDATE_ORDER]


class Mutation(graphene.ObjectType):
    create_cart_item = CreateCartItem.Field()
    update_cart_item = UpdateCartItem.Field()
    delete_cart_item = DeleteCartItem.Field()
    create_order_from_cart = CreateOrderFromCart.Field()
    update_order = UpdateOrder.Field()
