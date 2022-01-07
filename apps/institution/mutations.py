from django.utils.translation import gettext
import graphene
from apps.institution.models import Institution
from apps.institution.schema import InstitutionType
from apps.institution.serializers import (
    InstitutionSerializer,
)
from utils.graphene.mutation import generate_input_type_for_serializer
from utils.graphene.error_types import CustomErrorType, mutation_is_not_valid


InstitutionInputType = generate_input_type_for_serializer(
    'InstitutionCreateInputType',
    serializer_class=InstitutionSerializer
)


class CreateInstitute(graphene.Mutation):
    class Arguments:
        data = InstitutionInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(InstitutionType)

    @staticmethod
    def mutate(root, info, data):
        serializer = InstitutionSerializer(data=data, context={'request': info.context.request})
        if errors := mutation_is_not_valid(serializer):
            return CreateInstitute(errors=errors, ok=False)
        instance = serializer.save()
        return CreateInstitute(result=instance, errors=None, ok=True)


class UpdateInstitute(graphene.Mutation):
    class Arguments:
        data = InstitutionInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(InstitutionType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = Institution.objects.get(id=data['id'])
        except Institution.DoesNotExist:
            return UpdateInstitute(errors=[
                dict(field='nonFieldErrors', messages=gettext('Institution does not exist.'))
            ])
        serializer = InstitutionSerializer(
            instance=instance, data=data,
            context={'request': info.context.request}, partial=True
        )
        if errors := mutation_is_not_valid(serializer):
            return UpdateInstitute(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateInstitute(result=instance, errors=None, ok=True)


class DeleteInstitute(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(InstitutionType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = Institution.objects.get(id=id)
        except Institution.DoesNotExist:
            return DeleteInstitute(errors=[
                dict(field='nonFieldErrors', messages=gettext('Institution does not exist.'))
            ])
        instance.delete()
        instance.id = id
        return DeleteInstitute(result=instance, errors=None, ok=True)


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitute.Field()
    update_institution = UpdateInstitute.Field()
    delete_institution = DeleteInstitute.Field()
