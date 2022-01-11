from django.db import models
from django.utils.translation import gettext_lazy as _

# import Customer models
from customer.models import CustomerProfile


# Create your models here.


class Basket(models.Model):
    """
    Basket object
    """
    # Baskets can be anonymously owned - hence this field is nullable.  When a
    # anon user signs in, their two baskets are merged.
    owner = models.ForeignKey(
        CustomerProfile,
        null=True, blank=True,
        related_name='baskets',
        on_delete=models.CASCADE,
        verbose_name=_("Owner"))

    # Basket statuses
    # - Frozen is for when a basket is in the process of being submitted
    #   and we need to prevent any changes to it.
    OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
        "Open", "Merged", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN, _("Open - currently active")),
        (MERGED, _("Merged - superceded by another basket")),
        (SAVED, _("Saved - for items to be purchased later")),
        (FROZEN, _("Frozen - the basket cannot be modified")),
        (SUBMITTED, _("Submitted - has been ordered at the checkout")),
    )
    status = models.CharField(
        _("Status"), max_length=128, default=OPEN, choices=STATUS_CHOICES)

    # A basket can have many vouchers attached to it.  However, it is common
    # for sites to only allow one voucher per basket - this will need to be
    # enforced in the project's codebase.
    vouchers = models.ManyToManyField(
        'offer_coupon_voucher.Voucher', verbose_name=_("Vouchers"),
        blank=True, null=True)

    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_merged = models.DateTimeField(_("Date merged"), null=True, blank=True)
    date_submitted = models.DateTimeField(_("Date submitted"), null=True,
                                          blank=True)

    # Only if a basket is in one of these statuses can it be edited
    editable_statuses = (OPEN, SAVED)

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')
        db_table = 'basket'

    def __str__(self):
        # return _(
        #     "%(status)s basket (owner: %(owner)s, lines: %(num_lines)d)") \
        #        % {'status': self.status,
        #           'owner': self.owner,
        #           'num_lines': self.num_lines}

        return str(self.owner)

class BasketProductLine(models.Model):
    """A line of a basket (product and a quantity)

    Common approaches on ordering basket lines:

        a) First added at top. That's the history-like approach; new items are
           added to the bottom of the list. Changing quantities doesn't impact
           position.
           Oscar does this by default. It just sorts by Line.pk, which is
           guaranteed to increment after each creation.

        b) Last modified at top. That means items move to the top when you add
           another one, and new items are added to the top as well.  Amazon
           mostly does this, but doesn't change the position when you update
           the quantity in the basket view.
           To get this behaviour, change Meta.ordering and optionally do
           something similar on wishlist lines. Order lines should already
           be created in the order of the basket lines, and are sorted by
           their primary key, so no changes should be necessary there.

    """
    basket = models.ForeignKey(
        'basket.Basket',
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name=_("Basket")
    )

    # This is to determine which products belong to the same line
    # We can't just use product.id as you can have customised products
    # which should be treated as separate lines.  Set as a
    # SlugField as it is included in the path for certain views.
    line_reference = models.CharField(_("Line Reference"), max_length=128, db_index=True)

    # product = models.ManyToManyField('catalogue.Product', verbose_name=_("Product"))

    product = models.ForeignKey('catalogue.Product',
                                on_delete=models.CASCADE,
                                related_name='cart_product')
    category = models.ForeignKey('catalogue.Category',
                                 on_delete=models.CASCADE,
                                 related_name='cart_category',
                                 null=True, blank=True)
    collection = models.ForeignKey('catalogue.Collection',
                                   on_delete=models.CASCADE,
                                   related_name='cart_collection',
                                   null=True, blank=True)

    # We store the stockrecord that should be used to fulfil this line.
    # stockrecord = models.ForeignKey(
    #     'partner.StockRecord',
    #     on_delete=models.CASCADE,
    #     related_name='basket_lines',
    #     null=True, blank=True)

    quantity = models.PositiveIntegerField(_('Quantity'), default=1)

    # We store the unit price incl tax of the product when it is first added to
    # the basket.  This allows us to tell if a product has changed price since
    # a person first added it to their basket.
    price_currency = models.CharField(
        _("Currency"), max_length=12, default='INR')
    price_excl_tax = models.DecimalField(
        _('Price excl. Tax'), decimal_places=2, max_digits=12,
        null=True, blank=True)
    price_incl_tax = models.DecimalField(
        _('Price incl. Tax'), decimal_places=2, max_digits=12, null=True, blank=True)
    payable_amount = models.DecimalField(max_digits=10, default=0, decimal_places=2)

    # Track date of first addition
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, db_index=True)

    class Meta:
        # Enforce sorting by order of creation.
        ordering = ['date_created', 'pk']
        # unique_together = ("basket", "line_reference")
        verbose_name = _('Basket line')
        verbose_name_plural = _('Basket lines')
        db_table = 'Basket Product Lines'

    def __str__(self):
        return _(
            "Basket #%(basket_id)d, Product #%(product_id)d, quantity"
            " %(quantity)d") % {'basket_id': self.basket.id,
                                'product_id': self.product.id,
                                'quantity': self.quantity}

    # def save(self, *args, **kwargs):
    #     if not self.basket.can_be_edited:
    #         raise PermissionDenied(
    #             _("You cannot modify a %s basket") % (
    #                 self.basket.status.lower(),))
    #     return super().save(*args, **kwargs)
