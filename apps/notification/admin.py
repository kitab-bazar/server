from django.contrib import admin
from apps.notification.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'read', 'recipient', 'notification_type']
    list_display_links = ['id', 'title']
    search_fields = ['id', 'recipient__full_name']
    autocomplete_fields = ['recipient', ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient')


admin.site.register(Notification, NotificationAdmin)
