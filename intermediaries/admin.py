from django.contrib import admin
from .models import Intermediary


# Register your models here.
@admin.register(Intermediary)
class IntermediaryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'license_no', 'phone', 'email', 'is_active'
    )

    ordering = ("license_no",)
