from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.conf import settings
from django.utils.translation import gettext as _

from .forms import ClientForm, InvoiceForm, InvoiceItemFormSet
from .models import Invoice
from .pdf import render_invoice_pdf


def index(request):
    invoices = Invoice.objects.select_related('client').all()

    stats = invoices.aggregate(
        paid_count=Count('id', filter=Q(status='paid')),
        unpaid_count=Count('id', filter=Q(status='unpaid')),
    )

    return render(
        request,
        'dashboard/home.html',
        {
            'invoices': invoices,
            'total_count': invoices.count(),
            'paid_count': stats['paid_count'],
            'unpaid_count': stats['unpaid_count'],
        },
    )


def invoice_create(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        invoice_form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)

        if (
            client_form.is_valid()
            and invoice_form.is_valid()
            and formset.is_valid()
        ):
            with transaction.atomic():
                client = client_form.save()

                invoice = invoice_form.save(commit=False)
                invoice.client = client
                invoice.save()

                formset.instance = invoice
                formset.save()

                invoice.recalculate_total()
                invoice.save(update_fields=['total'])

            messages.success(
                request,
                _('Invoice %(number)s was created successfully.')
                % {'number': invoice.number},
            )

            return redirect(
                'InvoiceApp:invoice_detail',
                pk=invoice.pk,
            )

    else:
        client_form = ClientForm()
        invoice_form = InvoiceForm()
        formset = InvoiceItemFormSet()

    return render(
        request,
        'dashboard/invoice_form.html',
        {
            'client_form': client_form,
            'invoice_form': invoice_form,
            'formset': formset,
        },
    )


def invoice_detail(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related('client'),
        pk=pk,
    )

    return render(
        request,
        'dashboard/invoice_detail.html',
        {'invoice': invoice},
    )


def invoice_pdf(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related('client'),
        pk=pk,
    )

    company = {
        'name': settings.COMPANY_NAME,
        'address': settings.COMPANY_ADDRESS,
        'phone': settings.COMPANY_PHONE,
        'email': settings.COMPANY_EMAIL,
        'tax_id': settings.COMPANY_TAX_ID,
        'currency': settings.COMPANY_CURRENCY,
    }

    pdf_bytes = render_invoice_pdf(invoice, company)

    response = HttpResponse(
        pdf_bytes,
        content_type='application/pdf',
    )

    response['Content-Disposition'] = (
        f'attachment; filename="{invoice.number}.pdf"'
    )

    return response


def invoice_toggle_status(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    invoice.status = (
        'paid'
        if invoice.status == 'unpaid'
        else 'unpaid'
    )

    invoice.save(update_fields=['status'])

    return redirect(
        'InvoiceApp:invoice_detail',
        pk=pk,
    )


def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    number = invoice.number

    invoice.delete()

    messages.success(
        request,
        _('Invoice %(number)s was deleted successfully.')
        % {'number': number},
    )

    return redirect('InvoiceApp:index')
