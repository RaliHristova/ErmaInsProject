from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Insurance


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "policy_num",
        "ins_types",
        "vehicle",
        "vehicle_reg",
        "start_date",
        "end_date",
        "payment_value",
        "rescheduled",
        "rescheduled_date",
    )
    search_fields = ("policy_num", "vehicle__registration_number", "vehicle__vin_num")
    list_filter = ("ins_types", "rescheduled")
    ordering = ("-start_date",)
    readonly_fields = ("rescheduled_date",)


    def vehicle_reg(self, obj):
        return obj.vehicle.registration_number if obj.vehicle_id else "-"
    vehicle_reg.short_description = "Рег. №"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        try:
            obj.regenerate_payments()
        except Exception as e:
            print("Грешка при генариране на плащане за полица:", obj.pk, e)
