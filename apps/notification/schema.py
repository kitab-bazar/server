import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination
from typing import Union

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.notification.models import Notification
from apps.notification.filters import NotificationFilter
from apps.order.schema import OrderType
from apps.order.models import Order


def get_notification_qs(info):
    return Notification.objects.filter(recipient=info.context.user)


class NotificationType(DjangoObjectType):
    order = graphene.Field(OrderType)

    class Meta:
        model = Notification
        fields = (
            'id', 'read', 'message', 'created_at',
            'notification_type'
        )

    @staticmethod
    def get_custom_queryset(queryset, info, **kwargs):
        return get_notification_qs(info)

    @staticmethod
    def resolve_order(root, info, **kwargs) -> Union[Order, None]:
        return info.context.dl.notification.order.load(root.pk)


class NotificationWithCountType(graphene.ObjectType):
    read_count = graphene.Int()
    unread_count = graphene.Int()

    class Meta:
        fields = ('read_count', 'unread_count')

    @staticmethod
    def resolve_read_count(root, info, **kwargs) -> int:
        return get_notification_qs(info).filter(read=True).count()

    @staticmethod
    def resolve_unread_count(root, info, **kwargs) -> int:
        return get_notification_qs(info).filter(read=False).count()


class NotificationListType(CustomDjangoListObjectType, NotificationWithCountType):
    class Meta:
        model = Notification
        filterset_class = NotificationFilter


class Query(graphene.ObjectType):
    notification = DjangoObjectField(NotificationType)
    notifications = DjangoPaginatedListObjectField(
        NotificationListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def resolve_notifications(root, info, **kwargs) -> int:
        return get_notification_qs(info)
