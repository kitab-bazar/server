from import_export import resources
from apps.book.models import Tag, Category, Author, Book


class BookResource(resources.ModelResource):

    class Meta:
        model = Book


class BookCategoryResource(resources.ModelResource):

    class Meta:
        model = Category


class BookAuthorResource(resources.ModelResource):

    class Meta:
        model = Author


class BookTagResource(resources.ModelResource):

    class Meta:
        model = Tag
