from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from import_export.admin import ImportExportModelAdmin

from apps.book.models import Tag, Category, Author, Book, WishList
from apps.book.forms import BookAdminForm, AuthorAdminForm
from apps.book.resources import (
    BookResource, BookCategoryResource, BookAuthorResource, BookTagResource
)


class TagAdmin(TranslationAdmin, ImportExportModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]
    resource_class = BookTagResource


class CategoryAdmin(TranslationAdmin, ImportExportModelAdmin):
    list_display = ['id', 'name', 'parent_category']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]
    resource_class = BookCategoryResource


class AuthorAdmin(TranslationAdmin, ImportExportModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]
    form = AuthorAdminForm
    resource_class = BookAuthorResource


class BookAdmin(TranslationAdmin, ImportExportModelAdmin):
    list_display = ['id', 'title', 'publisher', 'price', 'isbn']
    autocomplete_fields = ('categories', 'tags', 'authors', 'publisher')
    search_fields = [
        'id', 'title', 'authors__name', 'categories__name', 'publisher__name', 'tags__name',
    ]
    list_display_links = ['id', 'title']
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'categories', 'authors', 'tags', 'isbn', 'number_of_pages',
                'language', 'weight', 'published_date', 'edition', 'publisher', 'price',
                'created_by', 'grade',
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
        ('Publish', {
            'fields': (
                'is_published',
            )
        }),
    )
    form = BookAdminForm
    resource_class = BookResource

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'publisher'
        ).prefetch_related('tags', 'authors', 'categories')


class WishListAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'created_by']
    autocomplete_fields = ('created_by', 'book')
    search_fields = ['book__title', 'created_by__full_name']
    list_display_links = ['id']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by', 'book')


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(WishList, WishListAdmin)
