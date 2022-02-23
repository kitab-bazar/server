import django_filters
from utils.graphene.filters import IDListFilter, IDFilter, MultipleInputFilter

from apps.book.models import Book, Tag, Category, Author
from apps.book.enums import BookGradeEnum, LanguageTypeEnum
from django.db.models import Q


class BookFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    categories = IDListFilter(method='filter_categories')
    authors = IDListFilter(method='filter_authors')
    tags = IDListFilter(method='filter_tags')
    publishers = IDFilter(method='filter_publishers')
    is_added_in_wishlist = django_filters.rest_framework.BooleanFilter(
        method='filter_is_added_in_wishlist', initial=False
    )
    grade = MultipleInputFilter(BookGradeEnum)
    language = MultipleInputFilter(LanguageTypeEnum)

    class Meta:
        model = Book
        fields = [
            'categories', 'authors', 'tags', 'publisher'
        ]

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(title_en__icontains=value) |
            Q(title_ne__icontains=value) |
            Q(authors__name__icontains=value)
        )

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


class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Tag
        fields = ['name']

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Category
        fields = ['name']

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)


class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name')

    class Meta:
        model = Author
        fields = ['name']

    def filter_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__icontains=value)
