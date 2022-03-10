from django.core.management.base import BaseCommand
from apps.book.models import Category
from django.core.files import File
import os
import sys


class Command(BaseCommand):
    help = 'Upload book category images'

    def handle(self, *args, **options):
        ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)
        files = os.listdir(f'{ROOT_DIR}/categories')
        for file_name in files:
            file = open(f'{ROOT_DIR}/categories/{file_name}', 'rb')
            category_name = str(file_name.split('.')[0])
            try:
                catetory = Category.objects.get(name=category_name)
                catetory.image.save(file_name, File(file))
            except Category.DoesNotExist:
                print(f'Category with this file name => {category_name} Does not exist')
