from django.db import models

# Create your models here.
class Vehicle(models.Model):
    class FuelTypes(models.TextChoices):
        PETROL = 'Petrol', 'Бензин'
        Diesel = 'Diesel', 'Дизел'
        Hybrid = 'Hybrid', 'Хибрид'
        Electric = 'Electric', 'Електрическа'
    registration_number = models.CharField(max_length=10, unique=True)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    vin_num = models.CharField(max_length=17, unique=True)
    owner = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    date_of_first_registration = models.DateField()
    engine_capacity = models.IntegerField()
    type_of_fuel = models.CharField(max_length=15, choices=FuelTypes.choices)
    color = models.CharField(max_length=15, default='without')

    def __str__(self):
        owner_name = f"{self.owner.first_name} {self.owner.last_name}" if self.owner_id else "Без собственик."
        return f"{self.registration_number} — {owner_name}"