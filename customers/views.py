from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm


def customer_list(request):
    customers = (
        Customer.objects.prefetch_related("intermediaries")
        .all()
        .order_by("last_name", "first_name")
    )
    context = {"customers": customers}
    return render(request, "customers/list.html", context)


def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    vehicles = customer.vehicle_set.all().order_by("registration_number")

    context = {"customer": customer, "vehicles": vehicles}
    return render(request, "customers/detail.html", context)


def customer_create(request):
    form = CustomerForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        customer = form.save()
        return redirect("customers:detail", pk=customer.pk)

    context = {"form": form}
    return render(request, "customers/form.html", context)


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)

    if request.method == "POST" and form.is_valid():
        customer = form.save()
        return redirect("customers:detail", pk=customer.pk)

    context = {"form": form, "customer": customer}
    return render(request, "customers/form.html", context)


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        customer.delete()
        return redirect("customers:list")

    context = {"object": customer}
    return render(request, "customers/confirm_delete.html", context)
