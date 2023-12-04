import csv
from sys import stdout
from argparse import FileType
from django.conf import settings
from django.core.management import BaseCommand
from django.contrib.postgres.aggregates import StringAgg
from django.db import models

from apps.book.models import Book


class Command(BaseCommand):
    help = 'Export client translation data to csv'

    def add_arguments(self, parser):
        parser.add_argument('output_file', nargs='?', type=FileType('w'), default=stdout)

    def handle(self, *_, **options):
        output_file = options['output_file']

        # TODO: Sync this with export
        headers = [
            'title_en',
            'title_ne',
            'edition',
            'grade',
            'author_name_en',
            'author_name_ne',
            'price',
            'description_en',
            'description_ne',
            'categories_en',
            'categories_ne',
            'isbn',
            'number_of_pages',
            'language',
            'publisher_en',
            'publisher_ne',
            'image',
            'published_date',
            # 'illustrator_name_en',
            # 'illustrator_name_ne',
            # 'editor_en',
            # 'editor_ne',
        ]

        # Collect all data to csv
        writer = csv.DictWriter(output_file, fieldnames=headers)
        writer.writeheader()
        for row in Book.objects.annotate(
            author_name_en=StringAgg('authors__name_en', ',', distinct=True),
            author_name_ne=StringAgg('authors__name_ne', ',', distinct=True),
            categories_en=StringAgg('categories__name_en', ',', distinct=True),
            categories_ne=StringAgg('categories__name_ne', ',', distinct=True),
            publisher_en=models.F('publisher__name_en'),
            publisher_ne=models.F('publisher__name_ne'),
        ).values(*headers).distinct():
            row['image'] = f"https://{settings.DJANGO_API_HOST}{settings.STATIC_URL}{row['image']}"
            writer.writerow(row)
