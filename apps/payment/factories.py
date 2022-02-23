import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from apps.user.factories import UserFactory

from .models import (
    Payment
)


class PaymentFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    modified_by = factory.SubFactory(UserFactory)
    paid_by = factory.SubFactory(UserFactory)
    amount = fuzzy.FuzzyInteger(100, 5000)

    class Meta:
        model = Payment
