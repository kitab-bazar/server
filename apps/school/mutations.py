from django.utils.translation import gettext
import graphene
from apps.school.models import School
from apps.school.schema import SchoolType
from apps.school.serializers import SchoolSerializer
from utils.mutation import generate_input_type_for_serializer
from utils.error_types import CustomErrorType, mutation_is_not_valid


SchoolInputType = generate_input_type_for_serializer(
    'SchoolCreateInputType',
    serializer_class=SchoolSerializer
)


class CreateSchool(graphene.Mutation):
    class Arguments:
        data = SchoolInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(SchoolType)

    @staticmethod
    def mutate(root, info, data):
        serializer = SchoolSerializer(data=data, context={'request': info.context.request})
        if errors := mutation_is_not_valid(serializer):
            return CreateSchool(errors=errors, ok=False)
        instance = serializer.save()
        return CreateSchool(result=instance, errors=None, ok=True)


class UpdateSchool(graphene.Mutation):
    class Arguments:
        data = SchoolInputType(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(SchoolType)

    @staticmethod
    def mutate(root, info, data):
        try:
            instance = School.objects.get(id=data['id'])
        except School.DoesNotExist:
            return UpdateSchool(errors=[
                dict(field='nonFieldErrors', messages=gettext('School does not exist.'))
            ])
        serializer = SchoolSerializer(
            instance=instance, data=data,
            context={'request': info.context.request}, partial=True
        )
        if errors := mutation_is_not_valid(serializer):
            return UpdateSchool(errors=errors, ok=False)
        instance = serializer.save()
        return UpdateSchool(result=instance, errors=None, ok=True)


class DeleteSchool(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(graphene.NonNull(CustomErrorType))
    ok = graphene.Boolean()
    result = graphene.Field(SchoolType)

    @staticmethod
    def mutate(root, info, id):
        try:
            instance = School.objects.get(id=id)
        except School.DoesNotExist:
            return DeleteSchool(errors=[
                dict(field='nonFieldErrors', messages=gettext('School does not exist.'))
            ])
        instance.delete()
        instance.id = id
        return DeleteSchool(result=instance, errors=None, ok=True)


class Mutation(graphene.ObjectType):
    create_school = CreateSchool.Field()
    update_school = UpdateSchool.Field()
    delete_school = DeleteSchool.Field()
