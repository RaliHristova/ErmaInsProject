from django.db import models


# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    owner_ucn = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=50, blank=True)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=100, blank=True)
    tel_num = models.CharField(max_length=10, unique=True)

    intermediaries = models.ManyToManyField(
        "intermediaries.Intermediary",
        related_name="customers",
        blank=True,
    )


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


