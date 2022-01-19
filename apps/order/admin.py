from django.contrib import admin
from apps.order.models import CartItem, BookOrder, Order


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'created_by', 'quantity']
    list_display_links = ['id', 'book']
    search_fields = ['id', 'book__title', ]
    autocomplete_fields = ['book', 'created_by']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('book', 'created_by')


class BookOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'quantity', 'isbn', 'edition', 'image']
    list_display_links = ['id', 'title']
    search_fields = ['id', 'book__title', ]
    autocomplete_fields = ['book']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'total_price', 'order_code']
    list_display_links = ['id', ]
    search_fields = ['id', 'created_by__full_name', ]
    autocomplete_fields = ['created_by']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(BookOrder, BookOrderAdmin)
admin.site.register(Order, OrderAdmin)
