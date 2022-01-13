from django.contrib import admin

from apps.institution.models import Institution


class InstitutionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'district', 'province',
        'municipality', 'local_address'
    ]
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]
    autocomplete_fields = ['district', 'province', 'municipality']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'district', 'province', 'municipality'
        )


admin.site.register(Institution, InstitutionAdmin)
