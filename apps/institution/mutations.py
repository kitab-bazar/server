import graphene
from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.institution.models import Institution
from apps.institution.schema import InstitutionType
from apps.institution.serializers import (
    InstitutionSerializer,
)


InstitutionInputType = generate_input_type_for_serializer(
    'InstitutionCreateInputType',
    serializer_class=InstitutionSerializer
)


class CreateInstitution(CreateUpdateGrapheneMutation):
    class Arguments:
        data = InstitutionInputType(required=True)
    model = Institution
    serializer_class = InstitutionSerializer
    result = graphene.Field(InstitutionType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class UpdateInstitution(CreateUpdateGrapheneMutation):
    class Arguments:
        data = InstitutionInputType(required=True)
        id = graphene.ID(required=True)
    model = Institution
    serializer_class = InstitutionSerializer
    result = graphene.Field(InstitutionType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class DeleteInstitution(DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Institution
    result = graphene.Field(InstitutionType)

    @classmethod
    def check_permissions(cls, *args, **_):
        return True


class Mutation(graphene.ObjectType):
    create_institution = CreateInstitution.Field()
    update_institution = UpdateInstitution.Field()
    delete_institution = DeleteInstitution.Field()
