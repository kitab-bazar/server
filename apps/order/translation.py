from modeltranslation.translator import register, TranslationOptions
from apps.order.models import BookOrder


@register(BookOrder)
class BookOrderTranslationOptions(TranslationOptions):
    fields = ('title',)
