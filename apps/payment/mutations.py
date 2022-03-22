import graphene

from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation
)
from config.permissions import UserPermissions

from apps.payment.serializers import PaymentSerializer, PaymentUpdateSerializer
from apps.payment.models import Payment
from apps.payment.schema import PaymentType
from apps.user.models import User


PaymentInputType = generate_input_type_for_serializer(
    'PaymentInputType',
    serializer_class=PaymentSerializer
)

PaymentUpdateInputType = generate_input_type_for_serializer(
    'PaymentUpdateInputType',
    serializer_class=PaymentUpdateSerializer
)


class PaymentMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.MODERATOR.value:
            return qs
        return qs.none()


class CreatePayment(PaymentMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = PaymentInputType(required=True)

    model = Payment
    serializer_class = PaymentSerializer
    result = graphene.Field(PaymentType)
    permissions = [UserPermissions.Permission.CAN_CREATE_PAYMENT]


class UpdatePayment(PaymentMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = PaymentUpdateInputType(required=True)
        id = graphene.ID(required=True)

    model = Payment
    serializer_class = PaymentUpdateSerializer
    result = graphene.Field(PaymentType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_PAYMENT]


class Mutation():
    create_payment = CreatePayment.Field()
    update_payment = UpdatePayment.Field()
