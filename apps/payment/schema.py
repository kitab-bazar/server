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


def get_payment_qs(info):
    return Payment.objects.all().distinct()


class PaymentType(DjangoObjectType):
    class Meta:
        skip_registry = True
        model = Payment
        fields = (
            'id', 'created_at',
            'amount', 'created_by'
        )
    status = graphene.Field(StatusEnum)
    transaction_type = graphene.Field(TransactionTypeEnum)
    payment_type = graphene.Field(PaymentTypeEnum)


class PaymentListType(CustomDjangoListObjectType):
    class Meta:
        model = Payment
        filterset_class = PaymentFilterSet


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
