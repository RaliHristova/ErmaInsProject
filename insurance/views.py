from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect

from .models import Insurance
from .forms import InsuranceForm
from vehicles.models import Vehicle
from payments.models import Payment


def dashboard(request):
    today = date.today()
    in_14 = today + timedelta(days=14)
    registration_number_query = request.GET.get("registration_number", "").strip().upper()

    if registration_number_query:
        vehicle = Vehicle.objects.filter(
            registration_number__iexact=registration_number_query
        ).only("id").first()
        if vehicle:
            return redirect("vehicles:detail", pk=vehicle.pk)

    overdue_payments = (
        Payment.objects
        .select_related("vehicle", "insurance")
        .filter(status="PENDING", due_date__lt=today)
        .order_by("due_date")
    )

    upcoming_payments = (
        Payment.objects
        .select_related("vehicle", "insurance")
        .filter(status="PENDING", due_date__gte=today, due_date__lte=in_14)
        .order_by("due_date")
    )

    expiring_insurances = (
        Insurance.objects
        .select_related("vehicle")
        .filter(end_date__gte=today, end_date__lte=in_14)
        .order_by("end_date")
    )

    if registration_number_query:
        overdue_payments = overdue_payments.filter(
            vehicle__registration_number__iexact=registration_number_query
        )
        upcoming_payments = upcoming_payments.filter(
            vehicle__registration_number__iexact=registration_number_query
        )
        expiring_insurances = expiring_insurances.filter(
            vehicle__registration_number__iexact=registration_number_query
        )

    context = {
        "today": today,
        "overdue_payments": overdue_payments,
        "upcoming_payments": upcoming_payments,
        "expiring_insurances": expiring_insurances,
        "window_days": 14,
        "registration_number_query": registration_number_query,
    }
    return render(request, "insurance/dashboard.html", context)


def insurance_list(request):
    insurances = Insurance.objects.select_related("vehicle").all().order_by("-start_date")
    context = {"insurances": insurances}
    return render(request, "insurance/list.html", context)


def insurance_detail(request, pk):
    insurance = get_object_or_404(Insurance.objects.select_related("vehicle"), pk=pk)
    payments = insurance.payment_set.all().order_by("installment_no")

    context = {"insurance": insurance, "payments": payments}
    return render(request, "insurance/detail.html", context)


def insurance_create(request):
    form = InsuranceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        insurance = form.save()
        insurance.regenerate_payments()
        return redirect("insurance:detail", pk=insurance.pk)

    context = {"form": form}
    return render(request, "insurance/form.html", context)


def insurance_update(request, pk):
    insurance = get_object_or_404(Insurance, pk=pk)
    form = InsuranceForm(request.POST or None, instance=insurance)

    if request.method == "POST" and form.is_valid():
        insurance = form.save()
        insurance.regenerate_payments()
        return redirect("insurance:detail", pk=insurance.pk)

    context = {"form": form, "insurance": insurance}
    return render(request, "insurance/form.html", context)


def insurance_delete(request, pk):
    insurance = get_object_or_404(Insurance, pk=pk)

    if request.method == "POST":
        insurance.delete()
        return redirect("insurance:list")

    context = {"object": insurance}
    return render(request, "insurance/confirm_delete.html", context)


def insurances_by_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    insurances = Insurance.objects.filter(vehicle=vehicle).order_by("-start_date")

    context = {"vehicle": vehicle, "insurances": insurances}
    return render(request, "insurance/list.html", context)


def insurance_expiring(request):
    today = date.today()
    in_14 = today + timedelta(days=14)

    insurances = (
        Insurance.objects
        .select_related("vehicle")
        .filter(end_date__gte=today, end_date__lte=in_14)
        .order_by("end_date")
    )

    context = {"insurances": insurances, "today": today, "window_days": 14}
    return render(request, "insurance/expiring.html", context)
