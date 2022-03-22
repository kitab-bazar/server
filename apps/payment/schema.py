import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination, DjangoObjectField

from django.db.models import QuerySet, Sum, F

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField, CustomDjangoListField
from utils.graphene.enums import EnumDescription

from apps.user.models import User

from .models import Payment, PaymentLog
from .filter_set import PaymentFilterSet, PaymentLogFilterSet
from .enums import (
    StatusEnum,
    TransactionTypeEnum,
    PaymentTypeEnum,
)
from apps.common.schema import ActivityFileType
from apps.order.models import Order


def get_payment_qs(info):
    # NOTE: SCHOOL_ADMIN can see his payement
    # MODERATOR can see all other payment
    if info.context.user.user_type == User.UserType.SCHOOL_ADMIN:
        return Payment.objects.filter(paid_by=info.context.user)
    elif info.context.user.user_type == User.UserType.MODERATOR:
        return Payment.objects.all()
    return Payment.objects.none()


class PaymentLogType(DjangoObjectType):
    files = CustomDjangoListField(ActivityFileType, required=False)

    class Meta:
        model = PaymentLog
        fields = ('comment', 'snapshot', 'id')


class PaymentLogListType(CustomDjangoListObjectType):

    class Meta:
        model = PaymentLog
        filterset_class = PaymentLogFilterSet


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
    payment_log = DjangoPaginatedListObjectField(
        PaymentLogListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )


class PaymentSummaryType(graphene.ObjectType):
    payment_credit_sum = graphene.Float()
    payment_debit_sum = graphene.Float()
    total_verified_payment = graphene.Float()
    total_verified_payment_count = graphene.Float()
    total_unverified_payment = graphene.Float()
    total_unverified_payment_count = graphene.Float()
    outstanding_balance = graphene.Float()

    class Meta:
        fields = ()


class PaymentListType(CustomDjangoListObjectType):
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
    payment_summary = graphene.Field(PaymentSummaryType)

    @staticmethod
    def resolve_payments(root, info, **kwargs) -> QuerySet:
        return get_payment_qs(info)

    @staticmethod
    def resolve_payment_summary(root, info, **kwargs):
        payment_summary = get_payment_qs(info).annotate(
            **User.annotate_user_payment_statement()
        ).aggregate(
            Sum('payment_credit_sum'),
            Sum('payment_debit_sum'),
            Sum('total_verified_payment'),
            Sum('total_verified_payment_count'),
            Sum('total_unverified_payment'),
            Sum('total_unverified_payment_count'),
        )

        total_order_pending_price = Order.objects.filter(
            status=Order.Status.PENDING.value,
            created_by=info.context.user
        ).annotate(grand_total_price=F('book_order__price') * F('book_order__quantity')).aggregate(
            Sum('grand_total_price')
        )['grand_total_price__sum'] or 0

        outstanding_balance = (
            payment_summary['payment_credit_sum__sum'] -
            payment_summary['payment_debit_sum__sum'] -
            total_order_pending_price
        )

        return {
            'payment_credit_sum': payment_summary['payment_credit_sum__sum'],
            'payment_debit_sum': payment_summary['payment_debit_sum__sum'],
            'total_verified_payment': payment_summary['total_verified_payment__sum'],
            'total_verified_payment_count': payment_summary['total_verified_payment_count__sum'],
            'total_unverified_payment': payment_summary['total_unverified_payment__sum'],
            'total_unverified_payment_count': payment_summary['total_unverified_payment_count__sum'],
            'total_order_pending_price': total_order_pending_price,
            'outstanding_balance': outstanding_balance
        }
