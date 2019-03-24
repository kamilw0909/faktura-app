from django.contrib import admin

from .models import Seller, Buyer, Item, Invoice


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    verbose_name = 'Usługi'
    verbose_name_plural = 'Usługi'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    
    fieldsets = (
        ('Dane faktury', {'fields':
                        ('invoice_number', 'invoice_date', 'invoice_sale_date',
                        'invoice_payment_date', 'payment')
        }),
        ('Strony', {'fields':
                    (('invoice_s_fk', 'invoice_b_fk'),)
        }),
        (None, {'fields':
                    ('comments',),
        }),
        (None, {'fields':
                    ('sign',)
        }),
    )
    inlines = [ItemInline]
    raw_id_fields = ('invoice_s_fk', 'invoice_b_fk')
    list_display = ('invoice_number', 'invoice_sale_date',
                    'invoice_s_fk', 'invoice_b_fk')
    list_filter = ('invoice_number', 'invoice_date', 'invoice_s_fk')
    date_hierarchy = 'invoice_sale_date'
    ordering = ['invoice_sale_date']


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'adress', 'postal_code', 'nip')
    ordering = ['name']


admin.site.register(Buyer)


