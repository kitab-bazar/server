import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination
from django.db.models import QuerySet

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.user.models import User
from apps.helpdesk.models import Faq, ContactMessage
from apps.helpdesk.filters import FaqFilter


def get_contact_messages_qs(info):
    if info.context.user.user_type == User.UserType.ADMIN.value:
        return ContactMessage.objects.all()
    return ContactMessage.objects.none()


def get_faq_qs(info):
    return Faq.objects.filter(publish_type=Faq.PublishType.PUBLISH)


class ContactMessageType(DjangoObjectType):
    class Meta:
        model = ContactMessage
        fields = (
            'id', 'full_name', 'email', 'municipality', 'address', 'message', 'phone_number',
            'message_type'
        )

    @staticmethod
    def get_custom_queryset(queryset, info):
        return get_contact_messages_qs(info)


class ContactMessageListType(CustomDjangoListObjectType):
    class Meta:
        model = ContactMessage


class FaqType(DjangoObjectType):
    class Meta:
        model = Faq
        fields = (
            'id', 'question', 'answer',
        )

    @staticmethod
    def get_custom_queryset(queryset, info):
        return get_faq_qs(info)


class FaqListType(CustomDjangoListObjectType):
    class Meta:
        model = Faq
        filterset_class = FaqFilter


class Query(graphene.ObjectType):
    faq = DjangoObjectField(FaqType)
    faqs = DjangoPaginatedListObjectField(
        FaqListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    contact_message = DjangoObjectField(ContactMessageType)
    contact_messages = DjangoPaginatedListObjectField(
        ContactMessageListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def resolve_faqs(root, info, **kwargs) -> QuerySet:
        return get_faq_qs(info)

    @staticmethod
    def resolve_contact_messages(root, info, **kwargs) -> QuerySet:
        return get_contact_messages_qs(info)
