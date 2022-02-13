import django_filters
from apps.book.models import Book, Tag, Category, Author
from utils.graphene.filters import IDListFilter, IDFilter, StringListFilter


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_title')
    categories = IDListFilter(method='filter_categories')
    authors = IDListFilter(method='filter_authors')
    tags = IDListFilter(method='filter_tags')
    publisher = IDFilter(method='filter_publisher')
    is_added_in_wishlist = django_filters.rest_framework.BooleanFilter(
        method='filter_is_added_in_wishlist', initial=False
    )
    grade = StringListFilter(method='filter_grade')

    class Meta:
        model = Book
        fields = [
            'title', 'categories', 'authors', 'tags', 'publisher'
        ]

    def filter_title(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(title__icontains=value)

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

    def filter_publisher(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(publisher=value)

    def filter_is_added_in_wishlist(self, queryset, name, value):
        if value is True:
            return queryset.filter(book_wish_list__isnull=False)
        if value is False:
            return queryset.filter(book_wish_list__isnull=True)

    def filter_grade(self, queryset, name, value):
        if not value:
            return queryset
        grade_list = list(map(str.lower, value))
        return queryset.filter(grade__in=grade_list)


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
