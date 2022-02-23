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
    transaction_type = factory.fuzzy.FuzzyChoice(Payment.TransactionType.choices, getter=lambda c: c[0])
    payment_type = factory.fuzzy.FuzzyChoice(Payment.PaymentType.choices, getter=lambda c: c[0])

    class Meta:
        model = Payment
