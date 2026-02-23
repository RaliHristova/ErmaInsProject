from django import forms
from .models import Intermediary


class IntermediaryForm(forms.ModelForm):
    class Meta:
        model = Intermediary
        fields = "__all__"
        labels = {
            "name": "Име",
            "license_no": "Лиценз №",
            "phone": "Телефон",
            "email": "Имейл",
            "is_active": "Активен",
        }
        ordering = ("license_no",)



