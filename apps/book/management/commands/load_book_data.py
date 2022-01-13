from django.core.management.base import BaseCommand

from apps.common.models import Province, District, Municipality
from apps.book.factories import BookFactory, TagFactory, AuthorFactory, CategoryFactory
from apps.publisher.factories import PublisherFactory


class Command(BaseCommand):
    help = 'Create some fake book data'

    def handle(self, *args, **options):
        # Create tags, authors can categories
        tag1, tag2, tag3 = TagFactory.create_batch(3)
        author1, author2, author3 = AuthorFactory.create_batch(3)
        category1, category2, category3 = CategoryFactory.create_batch(3)

        # Get province, district, municipality, make sure geo data is loaded
        province = Province.objects.first()
        district = District.objects.first()
        municipality = Municipality.objects.first()
        publisher1, publisher2, publisher3 = PublisherFactory.create_batch(
            3, province=province, district=district, municipality=municipality
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
            20, publisher=publisher2, tags=[tag2],
            categories=[category2], authors=[author2]
        )
        self.stdout.write(self.style.SUCCESS('Books created.'))
