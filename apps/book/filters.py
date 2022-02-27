import django_filters
from utils.graphene.filters import IDListFilter, MultipleInputFilter

from apps.common.filters import SearchFilterMixin
from apps.book.models import Book, Tag, Category, Author
from apps.book.enums import BookGradeEnum, BookLanguageEnum


class BookFilter(SearchFilterMixin, django_filters.FilterSet):
    categories = IDListFilter(method='filter_categories')
    authors = IDListFilter(method='filter_authors')
    tags = IDListFilter(method='filter_tags')
    publishers = IDListFilter(method='filter_publishers')
    is_added_in_wishlist = django_filters.rest_framework.BooleanFilter(
        method='filter_is_added_in_wishlist', initial=False
    )
    grade = MultipleInputFilter(BookGradeEnum)
    language = MultipleInputFilter(BookLanguageEnum)

    class Meta:
        model = Book
        fields = [
            'categories', 'authors', 'tags', 'publisher'
        ]
        search_fields = ('title', 'authors__name')

    def filter_categories(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(categories__in=value)

    def filter_authors(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(authors__in=value)

    def filter_tags(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(tags__in=value)

    def filter_publishers(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(publisher__in=value)

    def filter_is_added_in_wishlist(self, queryset, name, value):
        if value is True:
            return queryset.filter(book_wish_list__isnull=False)
        if value is False:
            return queryset.filter(book_wish_list__isnull=True)


class TagFilter(SearchFilterMixin, django_filters.FilterSet):
    class Meta:
        model = Tag
        fields = ()
        search_fields = ('name',)


class CategoryFilter(SearchFilterMixin, django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ()
        search_fields = ['name']


class AuthorFilter(SearchFilterMixin, django_filters.FilterSet):
    class Meta:
        model = Author
        fields = ()
        search_fields = ['name']
