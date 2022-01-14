from django.contrib import admin

from apps.user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'phone_number']
    search_fields = ['id', 'full_name', 'phone_number']
    list_display_links = ['id', 'full_name']


admin.site.register(User, UserAdmin)
