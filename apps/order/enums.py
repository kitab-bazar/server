from utils.graphene.enums import (
    convert_enum_to_graphene_enum,
    get_enum_name_from_django_field,
)

from .models import Order, OrderWindow

OrderStatusEnum = convert_enum_to_graphene_enum(Order.Status, name='OrderStatusEnum')
OrderWindowTypeEnum = convert_enum_to_graphene_enum(OrderWindow.OrderWindowType, name='OrderWindowTypeEnum')

enum_map = {
    get_enum_name_from_django_field(field): enum
    for field, enum in (
        (Order.status, OrderStatusEnum),
        (OrderWindow.type, OrderWindowTypeEnum),
    )
}
