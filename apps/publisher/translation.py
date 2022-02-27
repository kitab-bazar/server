from modeltranslation.translator import register, TranslationOptions
from apps.publisher.models import Publisher


@register(Publisher)
class PublisherTranslationOptions(TranslationOptions):
    fields = ('name',)
