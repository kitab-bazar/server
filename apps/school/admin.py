from django.contrib import admin
from apps.school.models import School


class SchoolAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'email', 'district', 'province',
        'municipality', 'local_address'
    ]
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name', ]
    autocomplete_fields = ['district', 'province', 'municipality']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'district', 'province', 'municipality'
        )


admin.site.register(School, SchoolAdmin)
