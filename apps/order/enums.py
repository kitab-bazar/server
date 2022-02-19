from utils.graphene.enums import (
    convert_enum_to_graphene_enum,
    get_enum_name_from_django_field,
)

from .models import Order

OrderStatusEnum = convert_enum_to_graphene_enum(Order.Status, name='OrderStatusEnum')

enum_map = {
    get_enum_name_from_django_field(field): enum
    for field, enum in (
        (Order.status, OrderStatusEnum),
    )
}
