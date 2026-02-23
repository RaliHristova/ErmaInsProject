from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    def clean_owner_ucn(self):
        owner_ucn = (self.cleaned_data.get("owner_ucn") or "").strip()
        if not owner_ucn:
            return owner_ucn

        qs = Customer.objects.filter(owner_ucn=owner_ucn)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Вече съществува клиент с такъв ЕГН")
        return owner_ucn

    def clean_intermediaries(self):
        intermediaries = self.cleaned_data.get("intermediaries")
        if not intermediaries:
            return intermediaries


        if intermediaries.filter(is_active=True).exists():
            return intermediaries

        raise forms.ValidationError("Избери поне един активен посредник.")

    class Meta:
        model = Customer
        fields = [
            "first_name", "last_name", "owner_ucn", "email",
            "city", "address", "tel_num", "intermediaries",
        ]
        labels = {
            "first_name": "Име",
            "last_name": "Фамилия",
            "owner_ucn": "ЕГН",
            "email": "Имейл",
            "city": "Град",
            "address": "Адрес",
            "tel_num": "Телефон",
            "intermediaries": "Посредници",
        }
        widgets = {
            "intermediaries": forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            "intermediaries": "Може да изберете повече от един посредник.",
        }
