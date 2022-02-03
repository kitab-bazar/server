from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.blog.models import Tag, Category, Blog
from apps.blog.forms import BlogAdminForm


class TagAdmin(TranslationAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]


class CategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'parent_category']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]


class BlogAdmin(TranslationAdmin):
    list_display = ['id', 'title']
    autocomplete_fields = ('category', 'tags',)
    search_fields = [
        'id', 'title', 'category__name', 'tags__name',
    ]
    list_display_links = ['id', 'title']
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'category', 'tags', 'published_date'
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
                'publish_type',
            )
        }),
    )
    form = BlogAdminForm

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'category'
        ).prefetch_related('tags')


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
