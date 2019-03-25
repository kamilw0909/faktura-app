from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
import weasyprint
import datetime

from .to_word import invoice_sum_to_word
from .models import Invoice
from .forms import InvoiceForm, ItemFormSet, BuyerForm


class IndexView(generic.ListView):
    template_name = 'invoice/index.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return Invoice.objects.filter(invoice_s_fk__user__username=self.request.user)


@login_required
def detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    platnosc = invoice_sum_to_word(invoice)
    return render(request,
                  'invoice/detail.html',
                  {'invoice': invoice, 'zlotowki': platnosc[0], 'grosze': platnosc[1]})


@login_required
def edit(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        form_invoice = InvoiceForm(request.POST, instance=invoice)
        formset_item = ItemFormSet(request.POST, request.FILES, instance=invoice)
        if formset_item.is_valid() and form_invoice.is_valid():
            form_invoice.save()
            formset_item.save()
            messages.success(request, 'Poprawki w fakturze %s zostały zapisane.' % invoice.invoice_number)
            return HttpResponseRedirect(reverse('invoice:detail', args=[invoice_id]))
        print('item: ', formset_item.errors, 'invoice: ', form_invoice.errors)
    else:
        form_invoice = InvoiceForm(instance=invoice)
        formset_item = ItemFormSet(instance=invoice)
        form_buyer = BuyerForm(instance=invoice)
    return render(request,
                  'invoice/edit.html',
                  {'form_invoice': form_invoice, 'formset_item': formset_item,
                   'form_buyer': form_buyer, 'invoice': invoice})


@login_required
def new_invoice(request):
    if request.method == 'POST':
        form_invoice = InvoiceForm(request.POST)
        if form_invoice.is_valid():
            form = form_invoice.save(commit=False)
        formset_item = ItemFormSet(request.POST, request.FILES, instance=form)
        if formset_item.is_valid():
            form_invoice.save()
            formset_item.save()
            messages.success(request, 'Faktura %s została dodana.' % form_invoice.cleaned_data['invoice_number'])
            return HttpResponseRedirect(reverse('invoice:index'))
        else: return HttpResponse('invoice: {}<br>items: {}'.format(form_invoice.errors, formset_item.errors))
    else:
        invoices = Invoice.objects.filter(invoice_s_fk__user__username=request.user.username)
        nums = [0]
        for i in invoices:
            nums.append(int(i.invoice_number.split('/')[0]))
        form_invoice = InvoiceForm(initial={'invoice_number': '{:02d}/{}'.format(max(nums)+1, datetime.datetime.now().strftime('%Y'))})
        formset_item = ItemFormSet()
        form_buyer = BuyerForm()
    return render(request,
                  'invoice/new.html',
                  {'form_invoice': form_invoice, 'formset_item': formset_item,
                   'form_buyer': form_buyer})


@login_required
def copied_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    invoice.pk = None
    invoices = Invoice.objects.filter(invoice_s_fk__user__username=request.user.username)
    nums = [0]
    for i in invoices:
        nums.append(int(i.invoice_number.split('/')[0]))
    form_invoice = InvoiceForm(instance=invoice, initial={'invoice_number': '{:02d}/{}'.format(max(nums)+1, datetime.datetime.now().strftime('%Y'))})
    formset_item = ItemFormSet(instance=invoice)
    form_buyer = BuyerForm(instance=invoice)
    return render(request,
                  'invoice/new.html',
                  {'form_invoice': form_invoice, 'formset_item': formset_item,
                   'form_buyer': form_buyer})


def new_buyer(request):
    if request.method == 'POST':
        form_buyer = BuyerForm(request.POST)
        if form_buyer.is_valid():
            form_buyer.save()
            messages.success(request, 'Nowy nabywca został dodany i możesz go wybrać z listy')
        else:
            messages.error('Coś poszło nie tak - nowy nabywca NIE został dodany')
        return HttpResponseRedirect(reverse('invoice:new_invoice'))


@staff_member_required
def download(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    platnosc = invoice_sum_to_word(invoice)
    html = render_to_string('invoice/pdf.html', {'invoice': invoice, 'zlotowki': platnosc[0], 'grosze': platnosc[1]})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="faktura_{}.pdf"'.format(invoice.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/pdf.css')])
    return response
