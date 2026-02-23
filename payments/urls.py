from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("", views.payment_list, name="list"),
    path("<int:pk>/", views.payment_detail, name="detail"),
    path("insurance/<int:insurance_id>/", views.payments_by_insurance, name="by_insurance"),
    path("<int:pk>/mark-paid/", views.payment_mark_paid, name="mark_paid"),
]
