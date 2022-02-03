from modeltranslation.translator import register, TranslationOptions
from apps.blog.models import (
    Tag, Category, Blog
)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Blog)
class BookTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'meta_title', 'meta_keywords', 'meta_description',
        'og_title', 'og_description', 'og_locale', 'og_type'
    )
