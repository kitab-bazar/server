import graphene
from typing import Union
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphene_django_extras import PageGraphqlPagination, DjangoObjectField

from django.db.models import QuerySet

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.payment.models import Payment
from apps.payment.enums import (
    StatusEnum,
    TransactionTypeEnum,
    PaymentTypeEnum
)
from apps.payment.filter_set import PaymentFilterSet
from apps.user.models import User


def get_payment_qs(info):
    # NOTE: SCHOOL_ADMIN can see his payement
    # MODERATOR can see all other payment
    if info.context.user.user_type == User.UserType.SCHOOL_ADMIN:
        return Payment.objects.filter(paid_by=info.context.user)
    elif info.context.user.user_type == User.UserType.MODERATOR:
        return Payment.objects.filter(created_by=info.context.user)
    return Payment.objects.all().distinct()


class PaymentType(DjangoObjectType):
    class Meta:
        skip_registry = True
        model = Payment
        fields = (
            'id', 'created_at',
            'amount', 'created_by',
            'modified_by', 'paid_by'
        )
    status = graphene.Field(StatusEnum, required=True)
    transaction_type = graphene.Field(TransactionTypeEnum, required=True)
    payment_type = graphene.Field(PaymentTypeEnum, required=True)


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

    @staticmethod
    def resolve_payments(root, info, **kwargs) -> QuerySet:
        return get_payment_qs(info)
