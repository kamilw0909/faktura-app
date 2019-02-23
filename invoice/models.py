from django.db import models
from django.utils import timezone
import datetime

class Seller(models.Model):
    name = models.CharField('Nazwa', max_length=100,)
    adress = models.CharField('Ulica i numer', max_length=100)
    postal_code = models.CharField('Kod pocztowy i miejscowość', max_length=100)
    nip = models.PositiveIntegerField('NIP')
    bank_name = models.CharField('Nazwa banku', max_length=100)
    account_nr = models.CharField('Numer konta', max_length=26)

    def __str__(self):
        return self.name

class Buyer(models.Model):
    name = models.CharField('Nazwa', max_length=100)
    adress = models.CharField('Ulica i numer', max_length=100)
    postal_code = models.CharField('Kod pocztowy i miejscowość', max_length=100)
    nip = models.PositiveIntegerField('NIP')
    bank_name = models.CharField('Nazwa banku', max_length=100)
    account_nr = models.CharField('Numer konta', max_length=26)
    
    def __str__(self):
        return self.name

def one_month_hence():
    return timezone.now() + timezone.timedelta(days=30)

class Invoice(models.Model):
    
    PAYMENT_CHOICES = (
        ('przelew', 'przelew'),
        ('gotówka', 'gotówka'),
    )
    invoice_number = models.CharField(  'Numer faktury', max_length=7,
                                        default='{}'.format(datetime.datetime.now().strftime('/%Y')),
                                        unique=True)
    invoice_date = models.CharField('Data i miejsce wystawienia', max_length=20,
                                    default='Warszawa, {}'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
    invoice_sale_date = models.DateField('Data sprzedaży', default=timezone.now)
    invoice_payment_date = models.DateField('Termin płatności', default=one_month_hence)
    payment = models.CharField('Płatność', max_length=10,
                                choices=PAYMENT_CHOICES,
                                default='transfer')
    invoice_s_fk = models.ForeignKey(Seller, on_delete=models.CASCADE,
                                    verbose_name='Sprzedawca',)
    invoice_b_fk = models.ForeignKey(Buyer, on_delete=models.CASCADE,
                                    verbose_name='Nabywca')
    comments = models.TextField('Uwagi', max_length=250)
    sign = models.CharField('Wystawca', max_length=250)
    
    @property
    def invoice_sum(self):
        sum = 0
        for item in self.item_set.all():
            sum += item.quantity * item.price
        return '{:.2f}'.format(sum)

    def __str__(self):
        return self.invoice_number

class Item(models.Model):
    UNIT_CHOICES = [
        ('h', 'h'),
        ('1h x os.', '1h x os.'),
        ('szt.', 'szt.')
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,
                                verbose_name='Usługi')
    product = models.CharField('Nazwa', max_length=250)
    quantity = models.PositiveIntegerField('Ilość', default=1)
    price = models.FloatField('Cena jednostki')
    unit = models.CharField('Jednostka', max_length=100,
                            choices=UNIT_CHOICES)
    
    @property
    def item_sum(self):
       return self.quantity * self.price

    def __str__(self):
        return self.product