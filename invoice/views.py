from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect

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
    if request.method == 'POST':
        form_invoice = InvoiceForm(request.POST)
        if form_invoice.is_valid():
            form = form_invoice.save(commit=False)
        formset_item = ItemFormSet(request.POST, request.FILES, instance=form)
        if formset_item.is_valid():
            form_invoice.save()
            formset_item.save()
            return HttpResponseRedirect('/')
    else:
        form_invoice = InvoiceForm()
        formset_item = ItemFormSet()
    return render(request,
                  'invoices/invoice/new.html',
                  {'form_invoice': form_invoice, 'formset_item': formset_item})
