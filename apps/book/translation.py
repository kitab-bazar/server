from modeltranslation.translator import register, TranslationOptions
from apps.book.models import (
    Tag, Category, Author, Book
)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', 'about_author')


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'meta_title', 'meta_keywords', 'meta_description',
        'og_title', 'og_description', 'og_locale', 'og_type'
    )
