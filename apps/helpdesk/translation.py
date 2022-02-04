from modeltranslation.translator import register, TranslationOptions
from apps.helpdesk.models import Faq


@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    fields = ('question', 'answer',)
