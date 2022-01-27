import graphene
from django.core.exceptions import PermissionDenied

from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.school.models import School
from apps.school.schema import SchoolType
from apps.school.serializers import SchoolSerializer

from apps.user.models import User
from config.permissions import SchoolPermissions


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

    @classmethod
    def check_permissions(cls, info, **_):
        for permission in cls.permissions:
            if not SchoolPermissions.check_permission(info, permission):
                raise PermissionDenied(SchoolPermissions.get_permission_message(permission))
        return False


class CreateSchool(SchoolMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = SchoolInputType(required=True)
    model = School
    serializer_class = SchoolSerializer
    result = graphene.Field(SchoolType)
    permissions = [SchoolPermissions.Permission.CREATE_SCHOOL]


class UpdateSchool(SchoolMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = SchoolInputType(required=True)
        id = graphene.ID(required=True)
    model = School
    serializer_class = SchoolSerializer
    result = graphene.Field(SchoolType)
    permissions = [SchoolPermissions.Permission.UPDATE_SCHOOL]


class DeleteSchool(SchoolMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = School
    result = graphene.Field(SchoolType)
    permissions = [SchoolPermissions.Permission.DELETE_SCHOOL]


class Mutation(graphene.ObjectType):
    create_school = CreateSchool.Field()
    update_school = UpdateSchool.Field()
    delete_school = DeleteSchool.Field()
