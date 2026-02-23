from django.contrib import admin
from django.utils import timezone
from .models import Payment


@admin.action(description="Mark selected payments as PAID")
def mark_paid(modeladmin, request, queryset):
    queryset.update(status="PAID", paid_at=timezone.now())


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "insurance", "vehicle", "installment_no", "due_date", "amount", "status", "paid_at")
    search_fields = ("insurance__policy_num", "vehicle__registration_number", "vehicle__vin_num")
    list_filter = ("status", "due_date")
    ordering = ("due_date", "installment_no")
    actions = [mark_paid]

