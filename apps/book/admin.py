from django.contrib import admin
from apps.book.models import Tag, Category, Author, Book
from modeltranslation.admin import TranslationAdmin


class TagAdmin(TranslationAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]


class CategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'parent_category']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]


class AuthorAdmin(TranslationAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]


class BookAdmin(TranslationAdmin):
    list_display = ['id', 'title', 'book_authors', 'book_tags', 'book_categories', 'publisher']
    autocomplete_fields = ('categories', 'tags', 'authors', 'publisher')
    search_fields = [
        'id', 'title', 'authors__name', 'categories__name', 'publisher__name', 'tags__name',
    ]
    list_display_links = ['id', 'title']
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'categories', 'authors', 'tags', 'isbn', 'number_of_pages',
                'language', 'weight', 'published_date', 'edition', 'publisher', 'price'
            )
        }),
        ('Content', {
            'fields': ('title', 'image', 'description')
        }),
        ('SEO information', {
            'fields': (
                'meta_title', 'meta_keywords', 'meta_description', 'og_title', 'og_description',
                'og_image', 'og_locale', 'og_type'
            )
        }),
    )

    def book_authors(self, obj):
        return ", ".join([aurhor.name for aurhor in obj.authors.all()])

    def book_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    def book_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'publisher'
        ).prefetch_related('tags', 'authors', 'categories')


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
