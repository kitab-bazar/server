from django.core.management.base import BaseCommand

from apps.common.models import Province, District, Municipality
from apps.book.factories import BookFactory, TagFactory, AuthorFactory, CategoryFactory
from apps.publisher.factories import PublisherFactory


class Command(BaseCommand):
    help = 'Create some fake book data'

    def handle(self, *args, **options):
        tag1 = TagFactory.create()
        tag2 = TagFactory.create()
        tag3 = TagFactory.create()

        author1 = AuthorFactory.create()
        author2 = AuthorFactory.create()
        author3 = AuthorFactory.create()

        category1 = CategoryFactory.create()
        category2 = CategoryFactory.create()
        category3 = CategoryFactory.create()

        province = Province.objects.first()
        district = District.objects.first()
        municipality = Municipality.objects.first()

        publisher1 = PublisherFactory.create(province=province, district=district, municipality=municipality)
        publisher2 = PublisherFactory.create(province=province, district=district, municipality=municipality)
        publisher3 = PublisherFactory.create(province=province, district=district, municipality=municipality)

        # Create books
        for i in range(20):
            book = BookFactory.create(publisher=publisher1)
            book.tags.add(tag1)
            book.authors.add(author1)
            book.categories.add(category1)
            book.publisher = publisher1
            book.save()

        for i in range(20):
            book = BookFactory.create(publisher=publisher3)
            book.tags.add(tag2)
            book.authors.add(author2)
            book.categories.add(category2)
            book.save()

        for i in range(20):
            book = BookFactory.create(publisher=publisher2)
            book.tags.add(tag3)
            book.authors.add(author3)
            book.categories.add(category3)
            book.save()
        self.stdout.write(self.style.SUCCESS('Books created.'))
