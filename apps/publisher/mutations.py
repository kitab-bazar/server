from django.utils.translation import gettext
import graphene
from apps.publisher.models import Publisher
from apps.publisher.schema import PublisherType
from apps.publisher.serializers import PublisherSerializer
from utils.graphene.mutation import generate_input_type_for_serializer
from utils.graphene.error_types import CustomErrorType, mutation_is_not_valid


PublisherInputType = generate_input_type_for_serializer(
    'PublisherCreateInputType',
    serializer_class=PublisherSerializer
)


class CreatePublisher(graphene.Mutation):
    class Arguments:
        data = PublisherInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(PublisherType)

    @staticmethod
    def mutate(root, info, data):
        serializer = PublisherSerializer(data=data, context={'request': info.context.request})
        if errors := mutation_is_not_valid(serializer):
            return CreatePublisher(errors=errors, ok=False)
        instance = serializer.save()
        return CreatePublisher(result=instance, errors=None, ok=True)


class UpdatePublisher(graphene.Mutation):
    class Arguments:
        data = PublisherInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(PublisherType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = Publisher.objects.get(id=data['id'])
        except Publisher.DoesNotExist:
            return UpdatePublisher(errors=[
                dict(field='nonFieldErrors', messages=gettext('Publisher does not exist.'))
            ])
        serializer = PublisherSerializer(
            instance=instance, data=data,
            context={'request': info.context.request}, partial=True
        )
        if errors := mutation_is_not_valid(serializer):
            return UpdatePublisher(errors=errors, ok=False)
        instance = serializer.save()
        return UpdatePublisher(result=instance, errors=None, ok=True)


class DeletePublisher(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(PublisherType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = Publisher.objects.get(id=id)
        except Publisher.DoesNotExist:
            return DeletePublisher(errors=[
                dict(field='nonFieldErrors', messages=gettext('Publisher does not exist.'))
            ])
        instance.delete()
        instance.id = id
        return DeletePublisher(result=instance, errors=None, ok=True)


class Mutation(graphene.ObjectType):
    create_publisher = CreatePublisher.Field()
    update_publisher = UpdatePublisher.Field()
    delete_publisher = DeletePublisher.Field()
