import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from apps.helpdesk.models import Faq, ContactMessage
from apps.common.factories import MunicipalityFactory


class FaqFactory(DjangoModelFactory):
    question = fuzzy.FuzzyText(length=100)
    answer = fuzzy.FuzzyText(length=100)

    class Meta:
        model = Faq


class ContactMessageFactory(DjangoModelFactory):
    full_name = fuzzy.FuzzyText(length=20)
    email = fuzzy.FuzzyText(length=15)
    municipality = factory.SubFactory(MunicipalityFactory)
    address = fuzzy.FuzzyText(length=15)
    message_type = factory.fuzzy.FuzzyChoice(ContactMessage.MessageType.choices)

    class Meta:
        model = ContactMessage
