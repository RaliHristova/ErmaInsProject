import calendar
from decimal import Decimal, ROUND_HALF_UP
from datetime import date as dt_date
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction
from django.db.models import Max
from payments.models import Payment



def add_months(d: dt_date, months: int) -> dt_date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    last_day = calendar.monthrange(y, m)[1]
    return dt_date(y, m, min(d.day, last_day))


class Insurance(models.Model):
    class InsTypes(models.TextChoices):
        GO = 'GO', 'ГО'
        KASKO = 'KASKO', 'Каско'
        ROBBERY = 'ROBBERY', 'Кражба'
        OTHER = 'OTHER', 'Друго'

    class Installments(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"

    policy_num = models.CharField(max_length=6, unique=True, blank=True, null=True)
    ins_types = models.CharField(max_length=10, choices=InsTypes.choices, default=InsTypes.OTHER)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, related_name='insurances')
    start_date = models.DateField()
    end_date = models.DateField()
    payment_value = models.DecimalField(max_digits=7, decimal_places=2)
    rescheduled = models.IntegerField(choices=Installments.choices, default=Installments.ONE)
    rescheduled_date = models.DateField(blank=True, null=True)

    def _next_policy_num(self) -> str:
        max_policy = self.__class__.objects.aggregate(max_policy=Max("policy_num"))["max_policy"]
        max_int = int(max_policy) if max_policy else 0
        return f"{max_int + 1:06d}"

    def step_months(self) -> int:
        return {1: 0, 2: 6, 3: 4, 4: 3}[int(self.rescheduled)]

    def compute_due_dates(self):
        n = int(self.rescheduled)
        if n == 1:
            return [self.start_date]

        step = self.step_months()
        dates = [add_months(self.end_date, -step * (n - i + 1)) for i in range(1, n + 1)]
        dates[0] = self.start_date
        return dates

    def split_amounts_accounting(self):
        n = int(self.rescheduled)
        total = Decimal(self.payment_value).quantize(Decimal("0.01"))
        if n == 1:
            return [total]

        base = (total / Decimal(n)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        amounts = [base] * (n - 1)
        last = total - sum(amounts)
        amounts.append(last)
        return amounts

    def update_next_due_date(self):
        due_dates = self.compute_due_dates()
        if not due_dates:
            self.rescheduled_date = None
            return
        if self.pk:
            pending_qs = self.payment_set.filter(status="PENDING").order_by("due_date", "installment_no")
            if int(self.rescheduled) > 1:
                next_after_start = pending_qs.filter(due_date__gt=self.start_date).first()
                if next_after_start:
                    self.rescheduled_date = next_after_start.due_date
                    return

            next_pending = pending_qs.first()
            if next_pending:
                self.rescheduled_date = next_pending.due_date
                return
        if int(self.rescheduled) > 1 and len(due_dates) > 1:
            self.rescheduled_date = due_dates[1]
            return

        self.rescheduled_date = due_dates[0]

    def clean(self):
        super().clean()
        if self.start_date:
            expected = add_months(self.start_date, 12)
            if self.end_date and self.end_date != expected:
                raise ValidationError({
                    "end_date": "Крайната дата се изчислява автоматично (12 месеца след началната)."
                })
            self.end_date = expected

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.start_date and self.end_date and self.payment_value and self.rescheduled:
            self.update_next_due_date()
        should_generate_policy_num = self.pk is None and not self.policy_num
        if not should_generate_policy_num:
            return super().save(*args, **kwargs)

        for _ in range(4):
            self.policy_num = self._next_policy_num()
            try:
                with transaction.atomic():
                    return super().save(*args, **kwargs)
            except IntegrityError:
                self.policy_num = None

        raise IntegrityError("Не може да се генерира уникален номер на полица.")


    def regenerate_payments(self):
        if not self.pk:
            raise ValueError("Съхрани застраховката преди да генерираш плащане.")

        self.payment_set.all().delete()

        due_dates = self.compute_due_dates()
        amounts = self.split_amounts_accounting()

        for i, (d, a) in enumerate(zip(due_dates, amounts), start=1):
            Payment.objects.create(
                insurance=self,
                vehicle=self.vehicle,
                installment_no=i,
                due_date=d,
                amount=a,
            )
