from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.user.models import User


class UserAdmin(DjangoUserAdmin):
    list_display = ['id', 'full_name', 'email', 'phone_number']
    search_fields = ['id', 'full_name', 'phone_number']
    list_display_links = ['id', 'full_name']
    ordering = ['id', 'email']

    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, UserAdmin)
