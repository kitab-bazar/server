from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from apps.helpdesk.models import Faq, ContactMessage


class FaqAdmin(TranslationAdmin):
    list_display = ('id', 'question', 'answer')
    search_fields = ('id', 'question', 'answer',)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'message_type')
    link_display = ('id', 'full_name')
    search_fields = ('id', 'full_name',)


admin.site.register(Faq, FaqAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
