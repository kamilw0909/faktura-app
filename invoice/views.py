from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.forms import inlineformset_factory, modelformset_factory

from .to_word import main
from .models import Invoice, Item
from .forms import InvoiceForm, ItemFormSet


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
    invoice = Invoice.objects.get(pk=invoice_id)
    form_invoice = InvoiceForm(instance=invoice)
    formset_item = ItemFormSet(instance=invoice)
    return render(request,
                  'invoices/invoice/edit.html',
                  {'form_invoice': form_invoice, 'formset_item': formset_item})


def new_invoice(request):
    form_invoice = InvoiceForm()
    formset_item = ItemFormSet()
    return render(request,
                  'invoices/invoice/new.html',
                  {'form_invoice': form_invoice, 'formset_item': formset_item})
