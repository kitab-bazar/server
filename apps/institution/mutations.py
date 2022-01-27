import graphene
from django.core.exceptions import PermissionDenied

from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.institution.models import Institution
from apps.institution.schema import InstitutionType
from apps.institution.serializers import InstitutionSerializer
from apps.user.models import User
from config.permissions import InstitutionPermissions


InstitutionInputType = generate_input_type_for_serializer(
    'InstitutionCreateInputType',
    serializer_class=InstitutionSerializer
)


class InstitutionMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.INSTITUTIONAL_USER.value:
            return qs.filter(id=info.context.user.institution_id)
        elif info.context.user.user_type == User.UserType.ADMIN.value:
            return qs
        return Institution.objects.none()

    @classmethod
    def check_permissions(cls, info, **_):
        for permission in cls.permissions:
            if not InstitutionPermissions.check_permission(info, permission):
                raise PermissionDenied(InstitutionPermissions.get_permission_message(permission))
        return False


class CreateInstitution(InstitutionMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = InstitutionInputType(required=True)
    model = Institution
    serializer_class = InstitutionSerializer
    result = graphene.Field(InstitutionType)
    permissions = [InstitutionPermissions.Permission.CREATE_INSTITUTION]


class UpdateInstitution(CreateUpdateGrapheneMutation):
    class Arguments:
        data = InstitutionInputType(required=True)
        id = graphene.ID(required=True)
    model = Institution
    serializer_class = InstitutionSerializer
    result = graphene.Field(InstitutionType)
    permissions = [InstitutionPermissions.Permission.UPDATE_INSTITUTION]


class DeleteInstitution(InstitutionMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Institution
    result = graphene.Field(InstitutionType)
    permissions = [InstitutionPermissions.Permission.DELETE_INSTITUTION]

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()
    delete_institution = DeleteInstitution.Field()
