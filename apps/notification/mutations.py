import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.notification.models import Notification
from apps.notification.schema import NotificationType
from apps.notification.serializers import ToggleNotificationSerializer


ToggleNotificationInputType = generate_input_type_for_serializer(
    'ToggleNotificationInputType',
    serializer_class=ToggleNotificationSerializer
)


class NotificationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        return qs.filter(recipient=info.context.user)


class ToggleNotificationReadStatus(NotificationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        id = graphene.ID(required=True)
        data = ToggleNotificationInputType(required=True)
    model = Notification
    serializer_class = ToggleNotificationSerializer
    result = graphene.Field(NotificationType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class DeleteNotification(NotificationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Notification
    result = graphene.Field(NotificationType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class Mutation(graphene.ObjectType):
    toggle_notification = ToggleNotificationReadStatus.Field()
    delete_notification = DeleteNotification.Field()
