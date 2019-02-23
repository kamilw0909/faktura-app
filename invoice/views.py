from django.shortcuts import render, get_object_or_404

from .to_word import main
from .models import Invoice

def index(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(  request,
                    'invoices/invoice/index.html',
                    context)


def detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    zloty = int(invoice.invoice_sum.split('.')[0])
    zlotowki = main(zloty)
    grosze = 'zero'
    if int(str(invoice.invoice_sum).split('.')[1]) > 0:
        kwota_gr = int(invoice.invoice_sum.split('.')[1])
        grosze =  main(kwota_gr)      
    return render(  request,
                    'invoices/invoice/detail.html',
                    {'invoice': invoice, 'zlotowki': zlotowki, 'grosze':grosze })
