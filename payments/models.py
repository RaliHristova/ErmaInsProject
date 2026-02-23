from django.db import models

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Очаква плащане"
        PAID = "PAID", "Платено"

    insurance = models.ForeignKey("insurance.Insurance", on_delete=models.CASCADE)
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.CASCADE)

    installment_no = models.PositiveSmallIntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.insurance_id and getattr(self.insurance, "vehicle_id", None):
            self.vehicle_id = self.insurance.vehicle_id
        super().save(*args, **kwargs)

