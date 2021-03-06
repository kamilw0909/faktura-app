from django.db import models
from django.conf import settings
import datetime

class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField('Nazwa', max_length=100,)
    adress = models.CharField('Ulica i numer', max_length=100)
    postal_code = models.CharField('Kod pocztowy i miejscowość', max_length=100)
    nip = models.PositiveIntegerField('NIP')
    bank_name = models.CharField('Nazwa banku', max_length=100)
    account_nr = models.CharField('Numer konta', max_length=26)

    class Meta:
        verbose_name = 'Sprzedawca'
        verbose_name_plural = 'Sprzedawcy'

    def __str__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField('Nazwa', max_length=100)
    adress = models.CharField('Ulica i numer', max_length=100)
    postal_code = models.CharField('Kod pocztowy i miejscowość', max_length=100)
    nip = models.PositiveIntegerField('NIP')

    class Meta:
        verbose_name = 'Nabywca'
        verbose_name_plural = 'Nabywcy'

    def __str__(self):
        return self.name


class Invoice(models.Model):

    PAYMENT_CHOICES = (
        ('Przelew', 'Przelew'),
        ('Gotówka', 'Gotówka'),
    )
    invoice_number = models.CharField('Nr faktury', max_length=8)
    invoice_date = models.CharField('Data i miejsce wystawienia', max_length=20,
                                    default='Warszawa, {}'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
    invoice_sale_date = models.CharField('Data sprzedaży', max_length=10,
                                         default='{}'.format(datetime.datetime.now().strftime('%Y-%m')))
    invoice_payment_date = models.DateField('Termin płatności',
                default='{}'.format((datetime.datetime.now()+datetime.timedelta(days=30)).strftime('%Y-%m-%d')))

    invoice_s_fk = models.ForeignKey(Seller, on_delete=models.CASCADE,
                                     verbose_name='Sprzedawca',)
    invoice_b_fk = models.ForeignKey(Buyer, on_delete=models.CASCADE,
                                     verbose_name='Nabywca')
    payment = models.CharField('Płatność', max_length=10,
                               choices=PAYMENT_CHOICES,
                               default='transfer')
    sign = models.CharField('Wystawca', max_length=250)
    comments = models.TextField('Uwagi', max_length=250,
            default='Faktura za miesiąc {}.'.format(datetime.datetime.now().strftime('%B %Y')))

    @property
    def invoice_sum(self):
        suma = 0
        for item in self.item_set.all():
            suma += item.quantity * item.price
        return '{:.2f}'.format(suma)

    class Meta:
        verbose_name = 'Faktura'
        verbose_name_plural = 'Faktury'
        ordering = ('-invoice_number',)

    def __str__(self):
        return self.invoice_number


class Item(models.Model):
    UNIT_CHOICES = [
        ('h', 'h'),
        ('1h za os.', '1h za os.'),
        ('szt.', 'szt.'),
        ('usł.', 'usł.'),
    ]
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,
                                verbose_name='Usługi')
    product = models.CharField('Nazwa', max_length=300)
    quantity = models.PositiveIntegerField('Ilość', default=1)
    price = models.FloatField('Cena')
    unit = models.CharField('Jednostka', max_length=100,
                            choices=UNIT_CHOICES)
    
    @property
    def item_sum(self): return self.quantity * self.price

    def __str__(self):
        return self.product
