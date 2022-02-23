from utils.graphene.enums import (
    convert_enum_to_graphene_enum,
    get_enum_name_from_django_field,
)

from .models import Payment

StatusEnum = convert_enum_to_graphene_enum(Payment.Status, name='StatusEnum')
PaymentTypeEnum = convert_enum_to_graphene_enum(Payment.PaymentType, name='PaymentTypeEnum')
TransactionTypeEnum = convert_enum_to_graphene_enum(Payment.TransactionType, name='TransactionTypeEnum')

enum_map = {
    get_enum_name_from_django_field(field): enum
    for field, enum in (
        (Payment.status, StatusEnum),
        (Payment.transaction_type, TransactionTypeEnum),
        (Payment.payment_type, PaymentTypeEnum)
    )
}
