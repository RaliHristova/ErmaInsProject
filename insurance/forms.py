from django import forms


from .models import Insurance

class InsuranceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_date"].input_formats = ["%d/%m/%Y"]
        self.fields["end_date"].input_formats = ["%d/%m/%Y"]
        self.fields["end_date"].required = False
        self.fields["end_date"].disabled = True

    class Meta:
        model = Insurance
        exclude = ('policy_num','rescheduled_date')
        widgets = {
            "start_date": forms.DateInput(
                format="%d/%m/%Y",
                attrs={"type": "text", "placeholder": "ДД/ММ/ГГГГ"},
            ),
            "end_date": forms.DateInput(
                format="%d/%m/%Y",
                attrs={"type": "text"},
            ),
        }
        labels = {
            "ins_types": "Тип застраховка",
            "vehicle": "За автомобил",
            "start_date": "Начална дата",
            "end_date": "Крайна дата",
            "payment_value": "Стойност на застраховката",
            "rescheduled": "Брой вноски",
        }
        help_texts = {
            "end_date": "Изчислява се автоматично: 12 месеца след началната дата.",
        }
