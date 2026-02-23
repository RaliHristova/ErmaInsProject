from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "registration_number", "make", "model","vin_num", "type_of_fuel", "owner")
    search_fields = ("registration_number", "vin_num", "make", "model", "owner__first_name", "owner__last_name", "owner__owner_ucn")
    list_filter = ("make", "model", "registration_number")
    ordering = ("registration_number",)
