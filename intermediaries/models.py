from django.db import models


class Intermediary(models.Model):
    name = models.CharField(max_length=100)
    license_no = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.license_no})"


