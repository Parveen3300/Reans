

from django.db import models



# import django validators
from django.core.validators import MaxValueValidator
from django.core.validators import RegexValidator

# import abstract models
from helper.models import AbstractCreatedByUpdatedBy
from helper.models import AbstractDate
from helper.models import AbstractLocationMaster
from helper.models import AbstractStatus

# import configuration models
from configuration.models import CurrencyMaster

# import Customer models
from customer.models import CustomerProfile




# Create your models here.


class MinMaxFloat(models.FloatField):
    """
    MinMaxFloat
    """

    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(MinMaxFloat, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(MinMaxFloat, self).formfield(**defaults)



class PaymentMethodOption(AbstractCreatedByUpdatedBy, AbstractDate, AbstractStatus):
    """
    PaymentMethodOption
    this models used to configure to payment option of pocket in
    """
    payment_methods_name = models.CharField(max_length=30)

    class Meta:
        verbose_name = '      Payment Methods Option'
        verbose_name_plural = '      Payment Methods Option'

    def __str__(self):
        return str(self.payment_methods_name)


class PaymentMethodConfiguration(AbstractCreatedByUpdatedBy, AbstractStatus):
    """
    EmployerPaymentMethod
    """
    payment_option = models.ForeignKey(
        PaymentMethodOption,
        on_delete=models.CASCADE,
        related_name='customer_payment_option',
        verbose_name='Payment Method Name',
        null=True
    )
    pay_pal_id = models.CharField(
        max_length=255, 
        null=True, blank=True,
        verbose_name='Payment Id'
    )
    pay_pal_name = models.CharField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='customer_profile_payment_method',
        null=True, blank=True, verbose_name='Company Details')
    credit_card_type = models.CharField(max_length=50, null=True, blank=True)
    credit_card_no = models.BigIntegerField(verbose_name='Card Number')
    cvv_no = models.IntegerField(verbose_name='CVV Number', null=True, blank=True)
    expiry_date = models.DateTimeField(auto_now_add=True)
    expiry_year = models.IntegerField(null=True, blank=True)
    expiry_month = models.IntegerField(null=True, blank=True)
    card_name = models.CharField(max_length=35, verbose_name='Card Name', null=True, blank=True)
    default_payment_method = models.IntegerField(
        verbose_name='Default Payment card Number', 
        null=True, blank=True
    )
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "      Payment Card Details"
        verbose_name_plural = "     Payment Card Details"

    def __str__(self):
        return str(self.card_name)


class PaymentTransaction(models.Model):
    """
    Payment Transaction
    """
    invoice_number = models.CharField(
        max_length=100,
        verbose_name='Invoice No.',
        blank=True, null=True
    )
    currency = models.ForeignKey(
        CurrencyMaster, 
        verbose_name='Currency Details',
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    payment_datetime = models.DateTimeField(auto_now_add=True)
    payment_type = models.ForeignKey(
        PaymentMethodConfiguration,
        verbose_name='Company Payment Type',
        on_delete=models.CASCADE,
        related_name='employer_profile_payment_option',
        null=True)
    amount_type = models.CharField(max_length=15, null=True, blank=True)
    amount_regex = RegexValidator(
        regex=r'^[0-9]+\.[0-9]{2}$',
        message="Amount must be up to 9 digits and 2 decimal places."
    )
    amount = MinMaxFloat(min_value=0.1, 
                         max_value=999999.99, 
                         null=True, blank=True, default=0,
                         verbose_name='Amount (in $)')
    initiated_by = models.CharField(
        max_length=100, 
        verbose_name='Initiated By', 
        null=True, blank=True
    )
    payment_status = models.CharField(
        max_length=150, 
        verbose_name='Payment Status', 
        null=True, blank=True
    )
    payment_status_count = models.CharField(max_length=150, 
                                            verbose_name='Payment Status Count', 
                                            null=True, blank=True)
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='customer_profile_payment_transaction',
        null=True, blank=True, 
        verbose_name='Company Details')
    is_active = models.BooleanField(default=False)
    order_no = models.ForeignKey(
        'order.Order',
        related_name='service_order_customer_transaction',
        on_delete=models.CASCADE,
        null=True)
    transaction_id = models.CharField(
        max_length=50,
        null=True, 
        verbose_name='Transaction Payment ID'
    )
    payment_gateway_amount = MinMaxFloat(
        min_value=0.1, max_value=999999.99,
        null=True, blank=True, default=0,
        verbose_name='Gate way Amount (in $)')

    class Meta:
        verbose_name = "    Company Payment Transaction History"
        verbose_name_plural = "    Company Payment Transaction History"

    def __str__(self):
        return str(self.payment_type.payment_option.payment_methods_name) + ' - ' + str(self.amount)