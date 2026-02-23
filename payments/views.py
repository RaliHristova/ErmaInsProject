from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Payment
from insurance.models import Insurance


def payment_list(request):
    payments = (
        Payment.objects
        .select_related("vehicle", "insurance")
        .all()
        .order_by("due_date", "installment_no")
    )
    context = {"payments": payments}
    return render(request, "payments/list.html", context)


def payment_detail(request, pk):
    payment = get_object_or_404(
        Payment.objects.select_related("vehicle", "insurance"),pk=pk
    )
    context = {"payment": payment}
    return render(request, "payments/detail.html", context)


def payments_by_insurance(request, insurance_id):
    insurance = get_object_or_404(
        Insurance.objects.select_related("vehicle"),pk=insurance_id
    )
    payments = insurance.payment_set.all().order_by("installment_no")
    context = {"insurance": insurance, "payments": payments}
    return render(request, "payments/list.html", context)


def payment_mark_paid(request, pk):
    payment = get_object_or_404(Payment, pk=pk)

    if request.method == "POST":
        payment.status = Payment.Status.PAID
        payment.paid_at = timezone.now()
        payment.save()
        insurance = payment.insurance
        insurance.update_next_due_date()
        Insurance.objects.filter(pk=insurance.pk).update(rescheduled_date=insurance.rescheduled_date)

    return redirect("payments:detail", pk=payment.pk)

