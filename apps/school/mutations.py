import graphene

from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.school.models import School
from apps.school.schema import SchoolType
from apps.school.serializers import SchoolSerializer

from apps.user.models import User
from config.permissions import UserPermissions


SchoolInputType = generate_input_type_for_serializer(
    'SchoolCreateInputType',
    serializer_class=SchoolSerializer
)


class SchoolMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.SCHOOL_ADMIN.value:
            return qs.filter(id=info.context.user.school_id)
        elif info.context.user.user_type == User.UserType.ADMIN.value:
            return qs
        return School.objects.none()


class CreateSchool(SchoolMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = SchoolInputType(required=True)
    model = School
    serializer_class = SchoolSerializer
    result = graphene.Field(SchoolType)
    permissions = [UserPermissions.Permission.CAN_CREATE_SCHOOL]


class UpdateSchool(SchoolMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = SchoolInputType(required=True)
        id = graphene.ID(required=True)
    model = School
    serializer_class = SchoolSerializer
    result = graphene.Field(SchoolType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_SCHOOL]


class DeleteSchool(SchoolMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = School
    result = graphene.Field(SchoolType)
    permissions = [UserPermissions.Permission.CAN_DELETE_SCHOOL]


class Mutation(graphene.ObjectType):
    create_school = CreateSchool.Field()
    update_school = UpdateSchool.Field()
    delete_school = DeleteSchool.Field()
