from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.common.models import (
    Province,
    District,
    Municipality,
)


class ProvinceAdmin(TranslationAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]

    def has_delete_permission(self, request, obj=None):
        return False


class DistrictAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'province']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', 'province__name']
    autocomplete_fields = ['province']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('province')

    def has_delete_permission(self, request, obj=None):
        return False


class MunicipalityAdmin(TranslationAdmin):
    list_display = ['id', 'name', 'province', 'district']
    list_display_links = ['id', 'name', 'province', 'district']
    search_fields = ['id', 'name', 'province__name', 'district__name']
    autocomplete_fields = ['province', 'district']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('province', 'district')

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
