import datetime
import pytz
import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from apps.book.models import Book, Tag, Author, Category, WishList
from apps.user.factories import UserFactory


class TagFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=10)

    class Meta:
        model = Tag


class AuthorFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=20)

    class Meta:
        model = Author


class CategoryFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=10)

    class Meta:
        model = Category


class BookFactory(DjangoModelFactory):

    isbn = fuzzy.FuzzyText(length=13)
    number_of_pages = fuzzy.FuzzyInteger(1, 20)
    price = fuzzy.FuzzyInteger(1, 20)
    language = Book.LanguageType.ENGLISH.value
    weight = fuzzy.FuzzyInteger(1, 20)
    published_date = fuzzy.FuzzyDateTime(
        datetime.datetime(2013, 1, 1, tzinfo=pytz.UTC),
        datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=730),
    )
    edition = fuzzy.FuzzyText(length=15)
    meta_title = fuzzy.FuzzyText(length=15)
    meta_keywords = fuzzy.FuzzyText(length=15)
    meta_description = fuzzy.FuzzyText(length=15)
    og_title = fuzzy.FuzzyText(length=100)
    og_description = fuzzy.FuzzyText(length=100)
    og_locale = fuzzy.FuzzyText(length=15)
    og_type = fuzzy.FuzzyText(length=15)
    title = fuzzy.FuzzyText(length=100)
    description = fuzzy.FuzzyText(length=500)

    class Meta:
        model = Book

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for author in extracted:
                self.authors.add(author)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)


class WishListFactory(DjangoModelFactory):
    book = factory.SubFactory(BookFactory)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = WishList
