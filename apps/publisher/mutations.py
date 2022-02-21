import graphene

from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.publisher.models import Publisher
from apps.publisher.schema import PublisherType
from apps.publisher.serializers import PublisherSerializer
from apps.user.models import User
from config.permissions import UserPermissions


PublisherInputType = generate_input_type_for_serializer(
    'PublisherCreateInputType',
    serializer_class=PublisherSerializer
)


class PublisherMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.PUBLISHER.value:
            return qs.filter(id=info.context.user.publisher_id)
        elif info.context.user.user_type == User.UserType.MODERATOR.value:
            return qs
        return Publisher.objects.none()


class CreatePublisher(PublisherMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = PublisherInputType(required=True)
    model = Publisher
    serializer_class = PublisherSerializer
    result = graphene.Field(PublisherType)
    permissions = [UserPermissions.Permission.CAN_CREATE_PUBLISHER]


class UpdatePublisher(PublisherMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = PublisherInputType(required=True)
        id = graphene.ID(required=True)
    model = Publisher
    serializer_class = PublisherSerializer
    result = graphene.Field(PublisherType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_PUBLISHER]


class DeletePublisher(PublisherMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Publisher
    result = graphene.Field(PublisherType)
    permissions = [UserPermissions.Permission.CAN_DELETE_PUBLISHER]


class Mutation(graphene.ObjectType):
    create_publisher = CreatePublisher.Field()
    update_publisher = UpdatePublisher.Field()
    delete_publisher = DeletePublisher.Field()
