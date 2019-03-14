from django.forms import ModelForm, inlineformset_factory, Textarea

from .models import Invoice, Item


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'invoice_date', 'invoice_sale_date',
                  'invoice_payment_date', 'payment', 'invoice_s_fk',
                  'invoice_b_fk', 'comments', 'sign']
        widgets = {'comments': Textarea(attrs={'cols': 50, 'rows': 2})}


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ()


ItemFormSet = inlineformset_factory(Invoice, Item,
                                    form=ItemForm,
                                    extra=1,
                                    can_delete=True)



