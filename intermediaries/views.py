from django.shortcuts import render, get_object_or_404, redirect
from customers.models import Customer
from .models import Intermediary
from .forms import IntermediaryForm


def intermediary_list(request):
    intermediaries = Intermediary.objects.all().order_by("name")
    return render(request, "intermediaries/list.html", {"intermediaries": intermediaries})


def intermediary_detail(request, pk):
    intermediary = get_object_or_404(Intermediary, pk=pk)
    customers = intermediary.customers.all().order_by('first_name', 'last_name')
    return render(
        request,
        "intermediaries/detail.html",
        {"intermediary": intermediary, "customers": customers},
    )


def intermediary_create(request):
    form = IntermediaryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        intermediary = form.save()
        return redirect("intermediaries:detail", pk=intermediary.pk)
    return render(request, "intermediaries/form.html", {"form": form})


def intermediary_update(request, pk):
    intermediary = get_object_or_404(Intermediary, pk=pk)
    form = IntermediaryForm(request.POST or None, instance=intermediary)
    if request.method == "POST" and form.is_valid():
        intermediary = form.save()
        return redirect("intermediaries:detail", pk=intermediary.pk)
    return render(request, "intermediaries/form.html", {"form": form, "intermediary": intermediary})


def intermediary_delete(request, pk):
    intermediary = get_object_or_404(Intermediary, pk=pk)
    if request.method == "POST":
        intermediary.delete()
        return redirect("intermediaries:list")
    return render(request, "intermediaries/confirm_delete.html", {"object": intermediary})








