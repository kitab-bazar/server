import datetime
import pytz
import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
from apps.blog.models import Blog, Tag, Category


class BlogTagFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=10)

    class Meta:
        model = Tag


class BlogCategoryFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=10)

    class Meta:
        model = Category


class BlogFactory(DjangoModelFactory):

    title = fuzzy.FuzzyText(length=100)
    description = fuzzy.FuzzyText(length=500)
    published_date = fuzzy.FuzzyDateTime(
        datetime.datetime(2013, 1, 1, tzinfo=pytz.UTC),
        datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=730),
    )
    category = factory.SubFactory(BlogCategoryFactory)
    blog_publish_type = factory.fuzzy.FuzzyChoice(Blog.BlogPublishType.choices)
    meta_title = fuzzy.FuzzyText(length=15)
    meta_keywords = fuzzy.FuzzyText(length=15)
    meta_description = fuzzy.FuzzyText(length=15)
    og_title = fuzzy.FuzzyText(length=100)
    og_description = fuzzy.FuzzyText(length=100)
    og_locale = fuzzy.FuzzyText(length=15)
    og_type = fuzzy.FuzzyText(length=15)

    class Meta:
        model = Blog

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
