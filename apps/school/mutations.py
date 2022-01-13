import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    GrapheneMutation,
    DeleteMutation
)

from apps.school.models import School
from apps.school.schema import SchoolType
from apps.school.serializers import SchoolSerializer


SchoolInputType = generate_input_type_for_serializer(
    'SchoolCreateInputType',
    serializer_class=SchoolSerializer
)


class CreateSchool(GrapheneMutation):
    class Arguments:
        data = SchoolInputType(required=True)
    model = School
    serializer_class = SchoolSerializer
    result = graphene.Field(SchoolType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class UpdateSchool(GrapheneMutation):
    class Arguments:
        data = SchoolInputType(required=True)
        id = graphene.ID(required=True)
    model = School
    serializer_class = SchoolSerializer
    result = graphene.Field(SchoolType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class DeleteSchool(DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = School
    result = graphene.Field(SchoolType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class Mutation(graphene.ObjectType):
    create_school = CreateSchool.Field()
    update_school = UpdateSchool.Field()
    delete_school = DeleteSchool.Field()
