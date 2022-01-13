import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.publisher.models import Publisher
from apps.publisher.schema import PublisherType
from apps.publisher.serializers import PublisherSerializer


PublisherInputType = generate_input_type_for_serializer(
    'PublisherCreateInputType',
    serializer_class=PublisherSerializer
)


class CreatePublisher(CreateUpdateGrapheneMutation):
    class Arguments:
        data = PublisherInputType(required=True)
    model = Publisher
    serializer_class = PublisherSerializer
    result = graphene.Field(PublisherType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class UpdatePublisher(CreateUpdateGrapheneMutation):
    class Arguments:
        data = PublisherInputType(required=True)
        id = graphene.ID(required=True)
    model = Publisher
    serializer_class = PublisherSerializer
    result = graphene.Field(PublisherType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class DeletePublisher(DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Publisher
    result = graphene.Field(PublisherType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class Mutation(graphene.ObjectType):
    create_publisher = CreatePublisher.Field()
    update_publisher = UpdatePublisher.Field()
    delete_publisher = DeletePublisher.Field()
