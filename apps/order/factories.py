import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from apps.user.factories import UserFactory
from apps.book.factories import BookFactory

from .models import (
    BookOrder,
    CartItem,
    Order,
    OrderWindow,
)


class CartItemFactory(DjangoModelFactory):
    book = factory.SubFactory(BookFactory)
    created_by = factory.SubFactory(UserFactory)
    quantity = fuzzy.FuzzyInteger(200, 5000)

    class Meta:
        model = CartItem


class OrderFactory(DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    total_price = fuzzy.FuzzyInteger(50000, 2000000)
    status = factory.fuzzy.FuzzyChoice(Order.Status.choices)

    class Meta:
        model = Order


class BookOrderFactory(DjangoModelFactory):
    title = fuzzy.FuzzyText(length=15)
    price = fuzzy.FuzzyInteger(500, 2000)
    quantity = fuzzy.FuzzyInteger(3, 10)
    isbn = fuzzy.FuzzyText(length=13)
    edition = fuzzy.FuzzyInteger(1, 9)
    total_price = fuzzy.FuzzyInteger(5000, 500000)
    book = factory.SubFactory(BookFactory)
    order = factory.SubFactory(OrderFactory)

    class Meta:
        model = BookOrder


class OrderWindowFactory(DjangoModelFactory):
    title = fuzzy.FuzzyText(length=15)
    description = fuzzy.FuzzyText(length=200)

    class Meta:
        model = OrderWindow
