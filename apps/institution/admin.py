from django.contrib import admin
from apps.institution.models import Institution


class InstitutionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'institution_name', 'institution_email', 'district', 'province',
        'municipality', 'local_address'
    ]
    list_display_links = ['id', 'institution_name']
    search_fields = ['id', 'institution_name', ]
    autocomplete_fields = ['district', 'province', 'municipality']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'district', 'province', 'municipality'
        )


admin.site.register(Institution, InstitutionAdmin)
