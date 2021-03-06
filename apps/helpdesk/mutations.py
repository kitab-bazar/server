import graphene
from django.core.exceptions import PermissionDenied

from utils.graphene.mutation import (
    generate_input_type_for_serializer,
    CreateUpdateGrapheneMutation,
    DeleteMutation
)

from apps.helpdesk.models import Faq, ContactMessage
from apps.helpdesk.schema import FaqType, ContactMessageType
from apps.helpdesk.serializers import FaqSerializer, ContactMessageSerializer

from apps.user.models import User
from config.permissions import UserPermissions


FaqInputType = generate_input_type_for_serializer(
    'FaqCreateInputType',
    serializer_class=FaqSerializer
)


class FaqMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.MODERATOR.value:
            return qs
        return qs.none()


class CreateFaq(FaqMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = FaqInputType(required=True)
    model = Faq
    serializer_class = FaqSerializer
    result = graphene.Field(FaqType)
    permissions = [UserPermissions.Permission.CREATE_FAQ]


class UpdateFaq(FaqMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = FaqInputType(required=True)
        id = graphene.ID(required=True)
    model = Faq
    serializer_class = FaqSerializer
    result = graphene.Field(FaqType)
    permissions = [UserPermissions.Permission.UPDATE_FAQ]


class DeleteFaq(FaqMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = Faq
    result = graphene.Field(FaqType)
    permissions = [UserPermissions.Permission.DELETE_FAQ]


ContactMessageInputType = generate_input_type_for_serializer(
    'ContactMessageInputType',
    serializer_class=ContactMessageSerializer
)


class ContactMessageMutationMixin():
    @classmethod
    def filter_queryset(cls, qs, info):
        if info.context.user.user_type == User.UserType.MODERATOR.value:
            return qs
        return qs.none()

    @classmethod
    def check_permissions(cls, info, **_):
        # TODO: Find better way to handle this
        # FIXME: Improve this
        if info.context.user.is_anonymous and cls.__name__ == 'CreateContactMessage':
            return True
        for permission in cls.permissions:
            if not UserPermissions.check_permission(info, permission):
                raise PermissionDenied(UserPermissions.get_permission_message(permission))
        return False


class CreateContactMessage(ContactMessageMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = ContactMessageInputType(required=True)
    model = ContactMessage
    serializer_class = ContactMessageSerializer
    result = graphene.Field(ContactMessageType)
    permissions = [UserPermissions.Permission.CREATE_CONTACT_MESSAGE]


class UpdateContactMessage(ContactMessageMutationMixin, CreateUpdateGrapheneMutation):
    class Arguments:
        data = ContactMessageInputType(required=True)
        id = graphene.ID(required=True)
    model = ContactMessage
    serializer_class = ContactMessageSerializer
    result = graphene.Field(ContactMessageType)
    permissions = [UserPermissions.Permission.UPDATE_CONTACT_MESSAGE]


class DeleteContactMessage(ContactMessageMutationMixin, DeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)
    model = ContactMessage
    result = graphene.Field(ContactMessageType)
    permissions = [UserPermissions.Permission.DELETE_CONTACT_MESSAGE]


class Mutation(graphene.ObjectType):
    create_faq = CreateFaq.Field()
    update_faq = UpdateFaq.Field()
    delete_faq = DeleteFaq.Field()
    create_contact_message = CreateContactMessage.Field()
    update_contact_message = UpdateContactMessage.Field()
    delete_contact_message = DeleteContactMessage.Field()
