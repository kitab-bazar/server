import graphene
from graphene_django import DjangoObjectType
from graphene_django_extras import DjangoObjectField, PageGraphqlPagination
from django.db.models import QuerySet

from utils.graphene.types import CustomDjangoListObjectType, FileFieldType
from utils.graphene.fields import DjangoPaginatedListObjectField
from utils.graphene.enums import EnumDescription

from apps.book.models import Book, Tag, Category, Author, WishList
from apps.book.filters import BookFilter, TagFilter, CategoryFilter, AuthorFilter
from apps.book.enums import BookGradeEnum, BookLanguageEnum
from apps.order.schema import CartItemType


def book_qs(info):
    return Book.objects.filter(is_published=True)


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'name_en', 'name_ne'
        )


class TagListType(CustomDjangoListObjectType):
    class Meta:
        model = Tag
        filterset_class = TagFilter


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'parent_category', 'name_en', 'name_ne'
            'id', 'name', 'parent_category', 'image',
        )
    image = graphene.Field(FileFieldType)


class CategoryListType(CustomDjangoListObjectType):
    class Meta:
        model = Category
        filterset_class = CategoryFilter


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = (
            'id', 'name', 'about_author',
            'name_en', 'name_ne',
            'about_author_en', 'about_author_ne'
        )


class AuthorListType(CustomDjangoListObjectType):
    class Meta:
        model = Author
        filterset_class = AuthorFilter


class BookType(DjangoObjectType):
    wishlist_id = graphene.ID()
    cart_details = graphene.Field(CartItemType)

    grade = graphene.Field(BookGradeEnum)
    grade_display = EnumDescription(source='get_grade_display')

    language = graphene.Field(BookLanguageEnum)
    language_display = EnumDescription(source='get_language_display')

    class Meta:
        model = Book
        fields = (
            'id', 'categories', 'authors', 'tags', 'isbn', 'number_of_pages', 'price',
            'image', 'language', 'weight', 'published_date', 'edition', 'publisher',
            'meta_title', 'meta_keywords', 'meta_description', 'og_title',
            'og_description', 'og_image', 'og_locale', 'og_type', 'title', 'description',
            'grade', 'is_published',

            # English fields
            'title_en', 'description_en', 'meta_title_en', 'meta_keywords_en', 'meta_description_en',
            'og_title_en', 'og_description_en', 'og_locale_en', 'og_type_en',

            # Nepali fields
            'title_ne', 'description_ne', 'meta_title_ne', 'meta_keywords_ne', 'meta_description_ne',
            'og_title_ne', 'og_description_ne', 'og_locale_ne', 'og_type_ne',

        )

    image = graphene.Field(FileFieldType)
    og_image = graphene.Field(FileFieldType)

    @staticmethod
    def get_custom_queryset(queryset, info):
        return book_qs(info)

    @staticmethod
    def resolve_wishlist_id(root, info, **kwargs) -> int:
        return info.context.dl.book.wishlist_id.load(root.pk)

    @staticmethod
    def resolve_cart_details(root, info, **kwargs) -> QuerySet:
        if info.context.user.is_anonymous:
            return None
        return root.book_cart_item.all().filter(created_by=info.context.user).first()


class BookListType(CustomDjangoListObjectType):
    class Meta:
        model = Book
        filterset_class = BookFilter


def get_wish_list_qs(info):
    return WishList.objects.filter(created_by=info.context.user)


class WishListType(DjangoObjectType):
    class Meta:
        model = WishList
        fields = ('id', 'book')

    @staticmethod
    def get_custom_queryset(queryset, info, **kwargs):
        return get_wish_list_qs(info)


class WishListListType(CustomDjangoListObjectType):
    class Meta:
        model = WishList


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
    categories = DjangoPaginatedListObjectField(
        CategoryListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )
    wish_list = DjangoPaginatedListObjectField(
        WishListListType,
        pagination=PageGraphqlPagination(
            page_size_query_param='pageSize'
        )
    )

    @staticmethod
    def resolve_wish_list(root, info, **kwargs) -> QuerySet:
        return get_wish_list_qs(info)

    @staticmethod
    def resolve_books(root, info, **kwargs) -> QuerySet:
        return book_qs(info)
