import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination

from utils.graphene.types import CustomDjangoListObjectType
from utils.graphene.fields import DjangoPaginatedListObjectField

from apps.book.models import Book, Tag, Category, Author
from apps.book.filters import BookFilter, TagFilter, CategoryFilter, AuthorFilter


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = (
            'id', 'name'
        )


class TagListType(CustomDjangoListObjectType):
    class Meta:
        model = Tag
        filterset_class = TagFilter


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'parent_category'
        )


class CategoryListType(CustomDjangoListObjectType):
    class Meta:
        model = Category
        filterset_class = CategoryFilter


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = (
            'id', 'name',
        )


class AuthorListType(DjangoObjectType):
    class Meta:
        model = Author
        filterset_class = AuthorFilter


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = (
            'categories', 'authors', 'tags', 'isbn', 'number_of_pages', 'price'
            'language', 'weight', 'published_date', 'edition', 'publisher',
            'meta_title', 'meta_keywords', 'meta_description', 'og_title', 'og_description',
            'og_image', 'og_locale', 'og_type', 'title', 'description'
        )

    @staticmethod
    def get_queryset(queryset, info):
        return queryset


class BookListType(CustomDjangoListObjectType):
    class Meta:
        model = Book
        filterset_class = BookFilter


class Query(graphene.ObjectType):
    book = DjangoObjectField(BookType)
    books = DjangoPaginatedListObjectField(
        BookListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    tags = DjangoPaginatedListObjectField(
        TagListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    authors = DjangoPaginatedListObjectField(
        AuthorListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
