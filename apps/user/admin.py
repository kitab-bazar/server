from django.contrib import admin
from django.core.cache import cache
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.core.exceptions import PermissionDenied


from apps.user.models import User


def enable_disable_captcha(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if cache.get('enable_captcha') in [True, None]:
        cache.set('enable_captcha', False)
        messages.add_message(request, messages.INFO, mark_safe("Captchad Disabled"))
    else:
        cache.set('enable_captcha', True)
        messages.add_message(request, messages.INFO, mark_safe("Captcha Enabled"))
    return HttpResponseRedirect(reverse('admin:user_user_changelist'))


class UserAdmin(DjangoUserAdmin):
    list_display = ['id', 'full_name', 'email', 'phone_number']
    search_fields = ['id', 'full_name', 'phone_number']
    list_display_links = ['id', 'full_name']
    ordering = ['id', 'email']
    change_list_template = "custom_user_page.html"

    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "user_type")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    'is_verified',
                    'is_deactivated',
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
