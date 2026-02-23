from django.urls import path
from . import views

app_name = "intermediaries"

urlpatterns = [
    path("", views.intermediary_list, name="list"),
    path("create/", views.intermediary_create, name="create"),
    path("<int:pk>/", views.intermediary_detail, name="detail"),
    path("<int:pk>/edit/", views.intermediary_update, name="update"),
    path("<int:pk>/delete/", views.intermediary_delete, name="delete"),



]
