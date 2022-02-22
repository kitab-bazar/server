from django.contrib import admin

from apps.payment.models import Payment, PaymentLog


class PaymentLogAdmin(admin.TabularInline):
    model = PaymentLog
    extra = 0


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    inlines = [PaymentLogAdmin]
