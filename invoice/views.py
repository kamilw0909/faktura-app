from django.shortcuts import render, get_object_or_404
from django.views import generic

from .to_word import main
from .models import Invoice


class IndexView(generic.ListView):
    template_name = 'invoices/invoice/index.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.all()


def detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    zloty = int(invoice.invoice_sum.split('.')[0])
    zlotowki = main(zloty)
    grosze = 'zero'
    if int(str(invoice.invoice_sum).split('.')[1]) > 0:
        kwota_gr = int(invoice.invoice_sum.split('.')[1])
        grosze = main(kwota_gr)
    return render(request,
                  'invoices/invoice/detail.html',
                  {'invoice': invoice, 'zlotowki': zlotowki, 'grosze': grosze})


def edit(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request,
                  'invoices/invoice/edit.html',
                  {'invoice': invoice})


def new_invoice(request):
    return render(request,
                  'invoices/invoice/new.html')
