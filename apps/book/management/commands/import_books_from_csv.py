import csv
import tempfile
import requests
# from pathlib import Path
from sys import stdin
from argparse import FileType

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import transaction, models

from apps.book.models import Book, Author, Category
from apps.publisher.models import Publisher


class ModelLookupHelper():
    def __init__(self, model, create_extra_params=None):
        self.model = model
        self.create_extra_params = create_extra_params or {}
        self.refetch()

    def refetch(self):
        self.id_collection_by_name = {
            name: _id
            for _id, name in self.model.objects.values_list('id', 'name')
        }

    def get_id_by_name(self, name, ne=None):
        if name not in self.id_collection_by_name:
            create_params = {
                **self.create_extra_params,
            }
            if ne:
                create_params.update(dict(
                    name_en=name,
                    name_ne=ne,
                ))
            else:
                create_params.update(dict(name=name))
            self.id_collection_by_name[name] = self.model.objects.create(create_params).id
        return self.id_collection_by_name[name]


def fetch_image_from_url(url):
    def _write_file(r, fp):
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                fp.write(chunk)
        return fp
    file = tempfile.NamedTemporaryFile(dir='/tmp')
    response = requests.get(url, stream=True)
    response.raise_for_status()
    _write_file(response, file)
    file.seek(0)
    return file


# Use provided values
GRADE_MAP = {
    '1': Book.Grade.GRADE_1,
    '2': Book.Grade.GRADE_2,
    '3': Book.Grade.GRADE_3,
}

LANGUAGE_MAP = {
    'English': Book.LanguageType.ENGLISH,
    'Nepali': Book.LanguageType.NEPALI,
    'Maithali': Book.LanguageType.MAITHALI,
    'Tharu': Book.LanguageType.THARU,
}


class Command(BaseCommand):
    help = 'Load books from csv'
    """
    # WIP: This is for one time use only.
    docker-compose exec server ./manage.py loaddata provinces districts municipalities
    cat data.csv | docker-compose exec -T server ./manage.py import_books_from_csv http://172.17.0.1:8080
    """

    def add_arguments(self, parser):
        parser.add_argument('input_file', nargs='?', type=FileType('r'), default=stdin)
        parser.add_argument(
            'images_source_uri',
            type=str,
            help=(
                'eg: http://172.17.0.1:8080'
                ', then http://172.17.0.1:8080/<publisher>/<s_n>.jpg will be used to retrive images'
            )
        )

    @transaction.atomic
    def handle(self, *args, **options):
        input_file = options['input_file']
        images_source_uri = options['images_source_uri']

        # create publisher
        default_publisher_params = dict(
            province_id=3,  # Bagmati
            district_id=27,  # Kathmandu
            municipality_id=27006,  # Kathmandu
            ward_number=1,
        )

        category_lookup = ModelLookupHelper(Category)
        author_lookup = ModelLookupHelper(Author)
        publisher_lookup = ModelLookupHelper(Publisher, create_extra_params=default_publisher_params)

        reader = csv.DictReader(input_file)
        for row in reader:
            # This is in nepali eg: 2077, convert to english
            published_date = timezone.datetime(
                year=int(row['Published date']) - 57,
                month=1,
                day=1,
            ).date()
            publisher_name = row['publisher']

            isbn = row['ISBN no'].replace('-', '')
            title_en = row['Title of the book']
            if Book.objects.filter(
                # models.Q(isbn=isbn) |
                models.Q(title_en=title_en, publisher__name=publisher_name)
            ).exists():
                self.stdout.write(
                    self.style.WARNING(f' - Book {title_en}/{isbn} already exists for publisher: {publisher_name}')
                )

            new_book = Book.objects.create(
                title_en=title_en,
                title_ne=row['Title of the book (Nepali)'],
                edition=row['Edition'],
                grade=GRADE_MAP[str(row['Grade'])],
                published_date=published_date,
                description_en=row['About the book'],
                description_ne=row['About the book (Nepali)'],
                isbn=isbn,
                price=row['Price of the book'] or 0,
                number_of_pages=(row['Number of pages'] or '0').replace('+', ''),
                language=LANGUAGE_MAP[str(row['Language'])],
                publisher_id=publisher_lookup.get_id_by_name(publisher_name, ne=row['Publisher (Nepali)']),
                is_published=True,
            )
            new_book.categories.set([
                category_lookup.get_id_by_name(
                    row['Category'],
                    ne=row['Category (Nepali)'],
                ),
            ])
            new_book.authors.set([
                author_lookup.get_id_by_name(
                    row["Author's name"],
                    ne=row['Author’s name (Nepali)']
                )
            ])
            s_n = row['S.N']
            new_book.image.save(
                f'{new_book.title}.jpg',
                fetch_image_from_url(
                    f'{images_source_uri}/{publisher_name}/{s_n}.jpg'
                )
            )
            self.stdout.write(f'- {new_book}')
            new_book.full_clean()

        self.stdout.write(self.style.SUCCESS('Books created.'))
