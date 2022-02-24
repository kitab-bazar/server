import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination, DjangoObjectField

from django.db.models import QuerySet, Sum

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.graphene.enums import EnumDescription

from apps.user.models import User
from apps.order.models import Order

from .models import Payment
from .filter_set import PaymentFilterSet
from .enums import (
    StatusEnum,
    TransactionTypeEnum,
    PaymentTypeEnum
)


def get_payment_qs(info):
    # NOTE: SCHOOL_ADMIN can see his payement
    # MODERATOR can see all other payment
    if info.context.user.user_type == User.UserType.SCHOOL_ADMIN:
        return Payment.objects.filter(paid_by=info.context.user)
    elif info.context.user.user_type == User.UserType.MODERATOR:
        return Payment.objects.all()
    return Payment.objects.none()


class PaymentType(DjangoObjectType):
    class Meta:
        skip_registry = True
        model = Payment
        fields = (
            'id',
            'created_at',
            'amount',
            'created_by',
            'modified_by',
            'paid_by'
        )
    status = graphene.Field(StatusEnum, required=True)
    transaction_type = graphene.Field(TransactionTypeEnum, required=True)
    payment_type = graphene.Field(PaymentTypeEnum, required=True)

    status_display = EnumDescription(source='get_status_display', required=True)
    transaction_type_display = EnumDescription(source='get_transaction_type_display', required=True)
    payment_type_display = EnumDescription(source='get_payment_type_display', required=True)


class OutStandingBalanceType(graphene.ObjectType):
    outstanding_balance = graphene.Float()

    class Meta:
        fields = ()

    @staticmethod
    def resolve_outstanding_balance(root, info, **kwargs) -> QuerySet:
        payment_credit = get_payment_qs(info).filter(
            transaction_type=Payment.TransactionType.CREDIT.value
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        payment_debit = get_payment_qs(info).filter(
            transaction_type=Payment.TransactionType.DEBIT.value
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        order_price = Order.objects.filter(
            created_by=info.context.user, status__in=[
                Order.Status.PENDING.value, Order.Status.IN_TRANSIT.value, Order.Status.COMPLETED.value
            ]
        ).aggregate(Sum('book_order__price'))['book_order__price__sum'] or 0
        return payment_credit - payment_debit - order_price


class PaymentListType(CustomDjangoListObjectType, OutStandingBalanceType):
    class Meta:
        model = Payment
        filterset_class = PaymentFilterSet
        base_type = PaymentType


class Query(graphene.ObjectType):
    payment = DjangoObjectField(PaymentType)
    payments = DjangoPaginatedListObjectField(
        PaymentListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def resolve_payments(root, info, **kwargs) -> QuerySet:
        return get_payment_qs(info)
