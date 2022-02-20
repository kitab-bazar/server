import graphene

from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.institution.models import Institution
from apps.institution.schema import InstitutionType
from apps.institution.serializers import InstitutionSerializer
from apps.user.models import User
from config.permissions import UserPermissions


InstitutionInputType = generate_input_type_for_serializer(
    'InstitutionCreateInputType',
    serializer_class=InstitutionSerializer
)


class InstitutionMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.INSTITUTIONAL_USER.value:
            return qs.filter(id=info.context.user.institution_id)
        elif info.context.user.user_type == User.UserType.MODERATOR.value:
            return qs
        return Institution.objects.none()


class CreateInstitution(InstitutionMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = InstitutionInputType(required=True)
    model = Institution
    serializer_class = InstitutionSerializer
    result = graphene.Field(InstitutionType)
    permissions = [UserPermissions.Permission.CAN_CREATE_INSTITUTION]


class UpdateInstitution(InstitutionMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = InstitutionInputType(required=True)
        id = graphene.ID(required=True)
    model = Institution
    serializer_class = InstitutionSerializer
    result = graphene.Field(InstitutionType)
    permissions = [UserPermissions.Permission.CAN_UPDATE_INSTITUTION]


class DeleteInstitution(InstitutionMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Institution
    result = graphene.Field(InstitutionType)
    permissions = [UserPermissions.Permission.CAN_DELETE_INSTITUTION]


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()
    delete_institution = DeleteInstitution.Field()
