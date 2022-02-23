import graphene

from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation
)
from config.permissions import UserPermissions

from apps.payment.serializers import PaymentSerializer
from apps.payment.models import Payment
from apps.payment.schema import PaymentType


PaymentInputType = generate_input_type_for_serializer(
    'PaymentInputType',
    serializer_class=PaymentSerializer
)


class PaymentMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        return qs.filter(created_by=info.context.user)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class CreatePayment(PaymentMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = PaymentInputType(required=True)

    model = Payment
    serializer_class = PaymentSerializer
    result = graphene.Field(PaymentType)
    permissions = [UserPermissions.Permission.CAN_CREATE_PAYMENT]


class UpdatePayment(PaymentMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = PaymentInputType(required=True)
        id = graphene.ID(required=True)

    model = Payment
    serializer_class = PaymentSerializer
    result = graphene.Field(PaymentType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_PAYMENT]


class Mutation():
    create_payment = CreatePayment.Field()
    update_payment = UpdatePayment.Field()
