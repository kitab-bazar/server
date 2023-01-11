import csv
import tempfile
import requests
# from pathlib import Path
from sys import stdin
from argparse import FileType

from datetime import datetime
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
            self.id_collection_by_name[name] = self.model.objects.create(**create_params).id
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
    'ECD': Book.Grade.ECD,
    '1': Book.Grade.GRADE_1,
    '2': Book.Grade.GRADE_2,
    '3': Book.Grade.GRADE_3,
}

LANGUAGE_MAP = {
    'English': Book.LanguageType.ENGLISH,
    'Nepali': Book.LanguageType.NEPALI,
    'Maithali': Book.LanguageType.MAITHALI,
    'Tharu': Book.LanguageType.THARU,
    'Bilingual': Book.LanguageType.BILINGUAL,
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
            publisher_name = row['Publisher']
            if row.get('published_date'):
                # Assuming published date should be in AD not BS
                published_date = datetime.strptime(row['published_date'], '%Y-%m-%d')
            else:
                self.stdout.write(
                    self.style.WARNING('Published date is not provied, default published date will be today.')
                )
                published_date = datetime.now()
            isbn = row['isbn'].replace('-', '')
            title_en = row['title_en']
            if Book.objects.filter(
                # models.Q(isbn=isbn) |
                models.Q(title_en=title_en, publisher__name=publisher_name)
            ).exists():
                self.stdout.write(
                    self.style.WARNING(f' - Book {title_en}/{isbn} already exists for publisher: {publisher_name}')
                )

            new_book = Book.objects.create(
                title_en=title_en.strip(),
                published_date=published_date,
                title_ne=row['title_en'].strip(),
                edition=row['edition'],
                grade=GRADE_MAP[str(row['grade'])],
                description_en=row['description_en'].strip(),
                description_ne=row['description_ne'].strip(),
                isbn=isbn,
                price=int(float(row['price'])) or 0,
                number_of_pages=(row['number_of_pages'] or '0').replace('+', ''),
                language=LANGUAGE_MAP[str(row['language'].strip())],
                publisher_id=publisher_lookup.get_id_by_name(publisher_name, ne=row['Publisher']),
                is_published=True,
            )
            new_book.categories.set([
                category_lookup.get_id_by_name(
                    row['categories_en'].strip(),
                    ne=row['categories_ne'].strip(),
                ),
            ])
            new_book.authors.set([
                author_lookup.get_id_by_name(
                    row["author_name_en"].strip(),
                    ne=row['author_name_ne'].strip()
                )
            ])
            new_book.image.save(
                row['image'],
                fetch_image_from_url(f"{images_source_uri}/{row['image']}")
            )
            self.stdout.write(f'- {new_book}')
            new_book.full_clean()

        self.stdout.write(self.style.SUCCESS('Books created.'))
