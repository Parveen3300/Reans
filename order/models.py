from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """
    The main order model
    """
    order_number = models.CharField(
        _("Order number"), max_length=128, db_index=True, unique=True)

    basket = models.ForeignKey(
        'basket.Basket', verbose_name=_("Basket"),
        null=True, blank=True, on_delete=models.SET_NULL)

    # Orders can be placed without the user authenticating so we don't always
    # have a customer ID.
    customer = models.ForeignKey('customer.customerProfile',
                                 related_name='orders_user',
                                 verbose_name=_("User"),
                                 on_delete=models.CASCADE)

    # Billing address is not always required (eg paying by gift card)
    billing_address = models.ForeignKey(
        'customer.CustomerAddress', null=True, blank=True,
        related_name='order_billing_address',
        verbose_name=_("Billing Address"),
        on_delete=models.SET_NULL)

    # Total price looks like it could be calculated by adding up the
    # prices of the associated lines, but in some circumstances extra
    # order-level charges are added and so we need to store it separately
    currency = models.CharField(
        _("Currency"), max_length=12, default='INR')
    total_incl_tax = models.DecimalField(
        _("Order total (inc. tax)"), decimal_places=2, max_digits=12)
    total_excl_tax = models.DecimalField(
        _("Order total (excl. tax)"), decimal_places=2, max_digits=12)

    # Shipping charges
    shipping_incl_tax = models.DecimalField(
        _("Shipping charge (inc. tax)"), decimal_places=2, max_digits=12,
        default=0)
    shipping_excl_tax = models.DecimalField(
        _("Shipping charge (excl. tax)"), decimal_places=2, max_digits=12,
        default=0)
    # Not all lines are actually shipped (such as downloads), hence shipping
    # address is not mandatory.
    shipping_address = models.ForeignKey(
        'customer.CustomerAddress', null=True, blank=True,
        verbose_name=_("Shipping Address"),
        related_name='order_shipping_address',
        on_delete=models.SET_NULL)
    shipping_method = models.CharField(
        _("Shipping method"), max_length=128, blank=True, null=True, )

    # Identifies shipping code
    shipping_code = models.CharField(blank=True, max_length=128, default="")

    # Use this field to indicate that an order is on hold / awaiting payment
    status = models.CharField(_("Status"), max_length=100, blank=True)
    guest_email = models.EmailField(_("Guest email address"), blank=True)

    # Index added to this field for reporting
    date_placed = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_placed']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return "#%s" % (self.order_number,)
