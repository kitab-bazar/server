import csv
import tempfile
import requests
from pathlib import Path

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.book.models import Book, Author, Category
from apps.publisher.models import Publisher


class ModelLookupHelper():
    def __init__(self, model, auto_create=True):
        self.model = model
        self.auto_create = auto_create
        self.refetch()

    def refetch(self):
        self.id_collection_by_name = {
            name: _id
            for _id, name in self.model.objects.values_list('id', 'name')
        }

    def get_id_by_name(self, name, ne=None):
        if name not in self.id_collection_by_name and self.auto_create:
            if ne:
                self.id_collection_by_name[name] = self.model.objects.create(name_en=name, name_ne=ne).id
            else:
                self.id_collection_by_name[name] = self.model.objects.create(name=name).id
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


IMAGES_SOURCE_BASE_URL = 'http://172.17.0.1:8080'

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
    help = 'Load book from csv'
    """
    # WIP: This is for one time use only.
    docker-compose exec server ./manage.py import_book_from_csv /code/kitab.csv
    docker-compose exec server ./manage.py loaddata provinces districts municipalities
    """

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=Path)

    @transaction.atomic
    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        category_lookup = ModelLookupHelper(Category)
        author_lookup = ModelLookupHelper(Author)
        publisher_lookup = ModelLookupHelper(Publisher, auto_create=False)

        # create publisher
        default_publisher_params = dict(
            province_id=3,  # Bagmati
            district_id=27,  # Kathmandu
            municipality_id=27006,  # Kathmandu
            ward_number=1,
        )
        for publisher_name in ['Bhundipuran', 'Ekta', 'Kathalaya', 'Parichaya']:
            if publisher_name not in publisher_lookup.id_collection_by_name:
                Publisher.objects.create(
                    name=publisher_name,
                    **default_publisher_params,
                )
        publisher_lookup.refetch()

        with open(csv_file_path) as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                # This is in nepali eg: 2077
                published_date = timezone.datetime(
                    year=int(row['Published date']),
                    month=1,
                    day=1,
                ).date()
                publisher_name = row['publisher']

                title_en = row['Title of the book (English)']
                if Book.objects.filter(title_en=title_en, publisher__name=publisher_name).exists():
                    self.stdout.write(self.style.WARNING(f'Book {title_en} already exists for publisher: {publisher_name}'))

                new_book = Book.objects.create(
                    title_en=title_en,
                    title_ne=row['Title of the book(Nepali)'],
                    edition=row['Edition - Optional'],
                    grade=GRADE_MAP[str(row['Grade'])],
                    published_date=published_date,
                    description_en=row['About the book (English)'],
                    description_ne=row['About the book (Nepali)'],
                    isbn=row['ISBN no'].replace('-', ''),
                    price=row['Price of the book'] or 0,
                    number_of_pages=(row['Number of pages'] or '0').replace('+', ''),
                    language=LANGUAGE_MAP[str(row['Language'])],
                    publisher_id=publisher_lookup.get_id_by_name(publisher_name),
                    is_published=True,
                )
                new_book.categories.set([
                    category_lookup.get_id_by_name(row['Category']),
                ])
                new_book.authors.set([
                    author_lookup.get_id_by_name(
                        row['Author’s name (English)'],
                        ne=row['Author’s name (Nepali)']
                    )
                ])
                s_n = row['S.N']
                new_book.image.save(
                    f'{new_book.title}.jpg',
                    fetch_image_from_url(
                        f'{IMAGES_SOURCE_BASE_URL}/{publisher_name}/{s_n}.jpg'
                    )
                )
                print(' -', new_book)
                new_book.full_clean()

        self.stdout.write(self.style.SUCCESS('Books created.'))
