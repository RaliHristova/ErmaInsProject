from django.contrib import admin

from customers.models import Customer


# Register your models here.

from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "owner_ucn", "tel_num", "city", "email")
    search_fields = ("first_name", "last_name", "owner_ucn", "tel_num", "city")
    list_filter = ("first_name", "last_name")
    ordering = ("id",)
