import django_filters
from apps.blog.models import Blog, Tag, Category
from utils.graphene.filters import IDListFilter


class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='filter_title')
    categories = IDListFilter(method='filter_categories')
    tags = IDListFilter(method='filter_tags')

    class Meta:
        model = Blog
        fields = [
            'title', 'categories', 'tags',
        ]

    def filter_title(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(title__icontains=value)

    def filter_categories(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(category__in=value)

    def filter_tags(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(tags__in=value)


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
