from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    date_of_first_registration = forms.DateField(
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(attrs={"type": "text", "placeholder": "ДД/ММ/ГГГГ"}),
        label="Дата на регистрация",
    )

    class Meta:
        model = Vehicle
        fields = [
            "registration_number", "make", "model", "vin_num", "owner",
            "date_of_first_registration", "engine_capacity", "type_of_fuel", "color",
        ]
        labels = {
            "registration_number": "Регистрационен номер",
            "make": "Марка",
            "model": "Модел",
            "vin_num": "Рама",
            "owner": "Собственик",
            "engine_capacity": "Обем на двигател",
            "type_of_fuel": "Вид гориво",
            "color": "Цвят",
        }
        error_messages = {
            "registration_number": {"unique": "Вече съществува автомобил с такъв регистрационен номер"},
            "vin_num": {"unique": "Вече съществува автомобил с такава рама (VIN)"},
        }
