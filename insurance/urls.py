from django.urls import path
from . import views

app_name = "insurance"

urlpatterns = [
    path("", views.insurance_list, name="list"),
    path("create/", views.insurance_create, name="create"),
    path("<int:pk>/", views.insurance_detail, name="detail"),
    path("<int:pk>/edit/", views.insurance_update, name="edit"),
    path("<int:pk>/delete/", views.insurance_delete, name="delete"),
    path("expiring/", views.insurance_expiring, name="expiring"),
    path("vehicle/<int:vehicle_id>/", views.insurances_by_vehicle, name="by_vehicle"),

]
