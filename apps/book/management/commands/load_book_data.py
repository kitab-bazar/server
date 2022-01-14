from django.core.management.base import BaseCommand

from apps.common.models import Municipality
from apps.book.factories import BookFactory, TagFactory, AuthorFactory, CategoryFactory
from apps.publisher.factories import PublisherFactory


class Command(BaseCommand):
    help = 'Create some fake book data'

    def handle(self, *args, **options):
        if Municipality.objects.count() < 0:
            self.stdout.write(self.style.ERROR('Please load province, district, municipality form fixtures.'))
            return
        municipality = Municipality.objects.first()
        # Create tags, authors can categories
        tag1, tag2, tag3 = TagFactory.create_batch(3)
        author1, author2, author3 = AuthorFactory.create_batch(3)
        category1, category2, category3 = CategoryFactory.create_batch(3)
        publisher1, publisher2, publisher3 = PublisherFactory.create_batch(
            3, municipality=municipality
        )

        # Create books
        BookFactory.create_batch(
            20, publisher=publisher1, tags=[tag1],
            categories=[category1], authors=[author1]
        )

        BookFactory.create_batch(
            20, publisher=publisher2, tags=[tag2],
            categories=[category2], authors=[author2]
        )

        BookFactory.create_batch(
            20, publisher=publisher3, tags=[tag3],
            categories=[category3], authors=[author3]
        )
        self.stdout.write(self.style.SUCCESS('Books created.'))
