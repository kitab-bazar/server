from django.contrib import admin
from apps.school.models import School


class SchoolAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'school_name', 'school_email', 'district', 'province',
        'municipality', 'local_address'
    ]
    list_display_links = ['id', 'school_name']
    search_fields = ['id', 'school_name', ]
    autocomplete_fields = ['district', 'province', 'municipality']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'district', 'province', 'municipality'
        )


admin.site.register(School, SchoolAdmin)
