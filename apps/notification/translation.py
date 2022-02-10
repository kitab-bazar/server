from modeltranslation.translator import register, TranslationOptions
from apps.notification.models import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ('title',)
