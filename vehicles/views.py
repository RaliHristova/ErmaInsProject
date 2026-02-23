from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle
from .forms import VehicleForm


def vehicle_list(request):
    vehicles = Vehicle.objects.select_related("owner").all().order_by("registration_number")
    context = {"vehicles": vehicles}
    return render(request, "vehicles/list.html", context)


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle.objects.select_related("owner"), pk=pk)

    insurances = vehicle.insurances.all().order_by("-start_date")
    payments = vehicle.payment_set.all().order_by("due_date")

    context = {
        "vehicle": vehicle,
        "insurances": insurances,
        "payments": payments,
    }
    return render(request, "vehicles/detail.html", context)


def vehicle_create(request):
    form = VehicleForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        vehicle = form.save()
        return redirect("vehicles:detail", pk=vehicle.pk)

    context = {"form": form}
    return render(request, "vehicles/form.html", context)


def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    form = VehicleForm(request.POST or None, instance=vehicle)

    if request.method == "POST" and form.is_valid():
        vehicle = form.save()
        return redirect("vehicles:detail", pk=vehicle.pk)

    context = {"form": form, "vehicle": vehicle}
    return render(request, "vehicles/form.html", context)


def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == "POST":
        vehicle.delete()
        return redirect("vehicles:list")

    context = {"object": vehicle}
    return render(request, "vehicles/confirm_delete.html", context)



