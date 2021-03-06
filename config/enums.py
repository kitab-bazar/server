from apps.book.enums import enum_map as book_enum_map
from apps.order.enums import enum_map as order_enum_map
from apps.payment.enums import enum_map as payment_enum_map
from apps.package.enums import enum_map as package_enum_map

ENUM_TO_GRAPHENE_ENUM_MAP = {
    **book_enum_map,
    **order_enum_map,
    **payment_enum_map,
    **package_enum_map,
}
