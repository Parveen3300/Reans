from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from catalogue.models import Category
# import Catalogue models
from catalogue.models import Collection
from catalogue.models import Product
# import Customer models
from customer.models import CustomerProfile

# import abstract models

ADMIN_MODELS = dict(
    RequestProductImage='Request for Additional Image',
    Record='Product record',
    NewsLetterSubscriber='News Letter Subscriber',
    DailyVisitors='Daily Visitors',
    TotalVisitors='Total Visitors',
    CustomerProductActivity='Customer Product Activity'
)


class RequestProductImage(models.Model):
    """
    RequestProductImage Models table
    """
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='request_product_image_customer',
        verbose_name='Customer Details'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='request_product_image_product',
        verbose_name='Product Details',
        limit_choices_to={'is_active': '1'}
    )
    product_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='request_product_image_product_category',
        limit_choices_to={'is_active': '1'}
    )
    product_collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='request_product_image_product_collection',
        null=True, blank=True,
        limit_choices_to={'is_active': '1'}
    )
    request_datetime = models.DateTimeField(verbose_name='Request Date & Time')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
    is_request_proceed = models.BooleanField(
        default=False,
        verbose_name='Request Acknowledged/Closed'
    )
    created_by = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='request_product_image_created_by',
        verbose_name='Requested By'
    )
    completion_datetime = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Completion Date & Time'
    )
    timezone = models.CharField(max_length=30, null=True, blank=True)
    remark = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='Remarks'
    )

    class Meta:
        verbose_name = _('Request for Additional Image')
        verbose_name_plural = _('Request for Additional Image')
        db_table = 'request_product_images'

    def __str__(self):
        return self.costumer.first_name


class ProductRecord(models.Model):
    """
    A record of a how popular a product is.

    This used be auto-merchandising to display the most popular
    products.
    """
    product = models.OneToOneField(
        'catalogue.Product', verbose_name=_("Product"),
        related_name='stats', on_delete=models.CASCADE)

    # Data used for generating a score
    num_views = models.PositiveIntegerField(_('Views'), default=0)
    num_basket_additions = models.PositiveIntegerField(
        _('Basket Additions'), default=0)
    num_purchases = models.PositiveIntegerField(
        _('Purchases'), default=0, db_index=True)

    # Product score - used within search
    score = models.FloatField(_('Score'), default=0.00)

    class Meta:
        ordering = ['-num_purchases']
        verbose_name = _('Product Record')
        verbose_name_plural = _('Product Record')
        db_table = 'product_records'

    def __str__(self):
        return _("Record for '%s'") % self.product


class CustomerRecord(models.Model):
    """
    A record of a user's activity.
    """

    customer = models.ForeignKey(
        CustomerProfile, on_delete=models.CASCADE,
        related_name='customer_records', verbose_name='Customer Details')

    # Browsing stats
    num_product_views = models.PositiveIntegerField(
        _('Product Views'), default=0)
    num_basket_additions = models.PositiveIntegerField(
        _('Basket Additions'), default=0)

    # Order stats
    num_orders = models.PositiveIntegerField(_('Orders'), default=0, db_index=True)
    num_order_lines = models.PositiveIntegerField(_('Order Lines'), default=0, db_index=True)
    num_order_items = models.PositiveIntegerField(_('Order Items'), default=0, db_index=True)
    total_spent = models.DecimalField(
        _('Total Spent'),
        decimal_places=2,
        max_digits=12,
        default=Decimal('0.00')
    )
    date_last_order = models.DateTimeField(
        _('Last Order Date'), blank=True, null=True)

    class Meta:
        abstract = True
        app_label = 'analytics'
        verbose_name = _('Customer record')
        verbose_name_plural = _('Customer record')
        db_table = 'customer_records'

    def __str__(self):
        return self.customer


class CustomerProductView(models.Model):
    """
    Customer Producr view models table
    """
    customer = models.ForeignKey(
        CustomerProfile, on_delete=models.CASCADE,
        related_name='customer_records_view', verbose_name='Customer Details')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"))
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = _('User product view')
        verbose_name_plural = _('User product views')
        db_table = 'customer_product_view'

    def __str__(self):
        return _("%(user)s viewed '%(product)s'") % {
            'user': self.customer,
            'product': self.product
        }


class CustomerSearch(models.Model):
    """
    #: Customer search model level models
    """
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='customer_search_records',
        verbose_name='Customer Details'
    )
    query = models.CharField(_("Search term"), max_length=255, db_index=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta:
        ordering = ['-pk']
        verbose_name = _("Customer search query")
        verbose_name_plural = _("Customer search queries")
        db_table = 'customer_search'

    def __str__(self):
        return _("%(user)s searched for '%(query)s'") % {
            'user': self.user,
            'query': self.query}


class NewsLetterSubscriber(models.Model):
    """
    NewsLetterSubscriber models tables
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name = _("News Letter Subscriber")
        verbose_name_plural = _('News Letter Subscriber')
        db_table = 'news_letter_subscriber'

    def __str__(self):
        return self.name


class DailyVisitors(models.Model):
    """
    Daily visitors model tables
    """
    visitors = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _("Daily Visitors")
        verbose_name_plural = _("Daily Visitors")
        db_table = 'daily_visitors'

    def __str__(self):
        return str(self.id)


class TotalVisitors(models.Model):
    """
    Total Visitors models table
    """
    visitors = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('Total Visitors')
        verbose_name_plural = _('Total Visitors')
        db_table = 'total_visitors'

    def __str__(self):
        return str(self.id)


class Bookmark(models.Model):
    """
    Bookmark model tables
    """
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='bookmark_customer'
    )
    product_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='bookmark_product_category'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='bookmark_product'
    )
    product_collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='bookmark_product_collection'
    )
    is_bookmarked = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date & Time'
    )

    class Meta:
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmark')
        db_table = 'bookmark'

    def __str__(self):
        return str(self.is_bookmarked)


class Wishlist(models.Model):
    """
    Wishlist models tables
    """
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='wishlist_customer'
    )
    product_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='wishlist_product_category'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlist_product'
    )
    product_collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='wishlist_product_collection'
    )
    is_wishlisted = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date & Time'
    )

    class Meta:
        unique_together = ('customer', 'product')
        verbose_name = _('Wishlist')
        verbose_name_plural = _('Wishlist')
        db_table = 'wishlist'

    def __str__(self):
        return str(self.is_wishlisted)


class CustomerProductActivity(models.Model):
    """
    CustomerProductActivity
    """
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='customer_customer_product_activity'
    )
    primary_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_customer_product_activity'
    )
    is_bookmarked = models.BooleanField(default=0)
    is_added_to_cart = models.BooleanField(default=0)
    is_added_to_wishlist = models.BooleanField(default=0)

    class Meta:
        verbose_name = ADMIN_MODELS['CustomerProductActivity']
        verbose_name_plural = ADMIN_MODELS['CustomerProductActivity']
        db_table = 'customer_product_activity'

    def __str__(self):
        return self.primary_product.product_name
