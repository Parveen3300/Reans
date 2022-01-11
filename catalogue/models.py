"""catalogue Models
"""

from ckeditor.fields import RichTextField

from django.core.validators import MaxValueValidator
# import django validators
from django.core.validators import MinValueValidator
from django.db import models


# import configuration models
from configuration.models import UnitOfMeasurement
# import abstract models
from helper.models import AbstractCreatedByUpdatedBy
from helper.models import AbstractDate
from helper.models import AbstractMetaTag
from helper.models import AbstractStatus
from helper.models import AbstractColor
# import utils helper
from helper.utils import current_year


# Create your models here.


ADMIN_MODELS = dict(
    Collection='Collection',
    Category='Category',
    PrimaryCategoryMapping='Primary Category Mapping',
    Product='Product Master',
    Feature='Feature',
    Specification='Specification',
    CollectionProductMapping='Collection Product Mapping',
    CategoryProductMapping='Category Product Mapping',
    ProductImages='Product Images',
    ProductVariant='Product Variant',


)


class Collection(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    Collection Model table
    """
    collection_name = models.CharField(max_length=100)
    collection_code = models.CharField(max_length=20, null=True, blank=True)
    collection_desc = models.CharField(
        max_length=200,
        null=True, blank=True,
        verbose_name='Description')
    collection_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1970),
            MaxValueValidator(2100)
        ],
        default=current_year,
        verbose_name='Collection Year')
    from_date = models.DateField(
        verbose_name='Collection Applicable From Date')
    to_date = models.DateField(verbose_name='Collection Applicable To Date')

    class Meta:
        verbose_name = ADMIN_MODELS['Collection']
        verbose_name_plural = ADMIN_MODELS['Collection']
        db_table = 'collection'
        # unique_together = ('collection_name', 'collection_year')

    def __str__(self):
        return self.collection_name


class Category(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    Category Models Tables
    """
    category_name = models.CharField(max_length=50, unique=True)

    category_non_common_dict = {
        'max_length': 200,
        'null': True,
        'blank': True
    }
    category_code = models.CharField(**category_non_common_dict)
    description = models.CharField(**category_non_common_dict)

    # is application or order-ring
    is_color_variant_applicable = models.BooleanField(
        default=False,
        verbose_name='Is Color Variant Applicable'
    )
    is_shape_applicable = models.BooleanField(
        default=False,
        verbose_name='Is Shape Variant Applicable'
    )
    ordering = models.PositiveIntegerField(null=True, blank=True)

    # category short, icon, and large images
    short_image = models.ImageField(
        upload_to='product_category/short_images',
        verbose_name='Category Image (Short image)',
        null=True, blank=True
    )
    image_icon = models.ImageField(
        upload_to='product_category/image_icon',
        verbose_name='Category Image (Icon)',
        null=True, blank=True
    )
    long_image = models.ImageField(
        upload_to='product_category/long_image',
        verbose_name='Category Image (Large Image)',
        null=True, blank=True
    )

    class Meta:
        verbose_name = ADMIN_MODELS['Category']
        verbose_name_plural = ADMIN_MODELS['Category']
        db_table = 'product_category'

    def __str__(self):
        return str(self.category_name)


class PrimaryCategoryMapping(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    ProductCategoryMapping
    """
    primary_category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        unique=True,
        related_name='product_category_mapping_primary_category',
        verbose_name="Primary Category",
        limit_choices_to={'is_active': '1'}
    )
    matching_category = models.ManyToManyField(
        Category,
        limit_choices_to={'is_active': '1'},
        verbose_name="Matching Category(s)"
    )
    is_all_matching = models.BooleanField(
        default=False, verbose_name="Is all matching")

    class Meta:
        verbose_name = ADMIN_MODELS['PrimaryCategoryMapping']
        verbose_name_plural = ADMIN_MODELS['PrimaryCategoryMapping']
        db_table = 'primary_category_mapping'

    # def primary_mode_detail(self):
    #   if self.primary_mode:
    #     primary_mode = ProductDetails(product_mode=self.primary_mode)
    #     return primary_mode()[1]
    # primary_mode_detail.short_description = 'Primary Mode'

    # def product_mode_details(self):
    #   if self.matching_mode:
    #     product_mode_details = ProductModeAllDetails(instance = self.matching_mode)
    #     return product_mode_details()
    # product_mode_details.short_description = 'Matching Mode(s)'

    def __str__(self):
        if self.primary_category:
            return str(self.primary_category.category_name)
        return '-'


class Product(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag,
    AbstractColor
):
    """
    Product models tables
    """
    PRODUCT_SIZES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )


    product_name = models.CharField(max_length=100, unique=True)
    product_alias_name = models.CharField(max_length=100, unique=True)
    product_code = models.CharField(max_length=20, null=True, blank=True)
    product_desc = models.CharField(max_length=200, null=True, blank=True)
    product_size = models.CharField(max_length=10, choices=PRODUCT_SIZES , null=True, blank=True)
    # content = QuillField()
    content = RichTextField(null=True, blank=True)
    sku = models.CharField(max_length=64, null=True, blank=True, default='NA')
    unit_of_measurment = models.ForeignKey(
        UnitOfMeasurement,
        related_name='product_unit_of_measurements',
        on_delete=models.CASCADE,
        verbose_name='Unit of Measurement',
        limit_choices_to={'is_active': '1'},
        blank=True, null=True
    )
    min_order_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(999999)],
        default=10,
        verbose_name='Min Order Quantity'
    )
    product_category = models.ManyToManyField(
        Category,
        limit_choices_to={'is_active': '1'},
        verbose_name='Product Category(s)',
        blank=True, null=True
    )
    product_collection = models.ManyToManyField(
        Collection,
        limit_choices_to={'is_active': '1'},
        verbose_name='Product Collection(s)',
        blank=True, null=True
    )

    price = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    is_promoted = models.BooleanField(default=False)
    is_show_on_home = models.BooleanField(default=False)

    image_help_text_string = "<h1 style='font-size: 12px; " \
                             "margin-left: 12rem; color: #ce8c95;'>" \
                             " width:440px height:440px </h1>"

    image_1 = models.ImageField(
        upload_to='product/',
        help_text=image_help_text_string,
        max_length=255
    )
    alt_1 = models.CharField(max_length=255, null=True, blank=True)
    image_2 = models.ImageField(
        upload_to='product/',
        help_text=image_help_text_string,
        max_length=255, null=True, blank=True
    )
    alt_2 = models.CharField(max_length=255, null=True, blank=True)
    image_3 = models.ImageField(
        upload_to='product/',
        help_text=image_help_text_string,
        max_length=255, null=True, blank=True
    )
    alt_3 = models.CharField(max_length=255, null=True, blank=True)
    image_4 = models.ImageField(
        upload_to='product/',
        help_text=image_help_text_string,
        max_length=255, null=True, blank=True
    )
    alt_4 = models.CharField(max_length=255, null=True, blank=True)
    image_5 = models.ImageField(
        upload_to='product/',
        help_text=image_help_text_string,
        max_length=255, null=True, blank=True
    )
    alt_5 = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = ADMIN_MODELS['Product']
        verbose_name_plural = ADMIN_MODELS['Product']
        db_table = 'product_master'

    def __str__(self):
        return self.product_name


class Feature(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    Feature model tables
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='features'
    )
    feature = models.CharField(max_length=255)

    class Meta:
        verbose_name = ADMIN_MODELS['Feature']
        verbose_name_plural = ADMIN_MODELS['Feature']
        db_table = 'product_feature'

    def __str__(self):
        return str(self.feature)


class Specification(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    Specification level models
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specifications'
    )
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = ADMIN_MODELS['Specification']
        verbose_name_plural = ADMIN_MODELS['Specification']
        db_table = 'product_specification'

    def __str__(self):
        return str(self.name)


class CollectionProductMapping(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    CollectionProductMapping
    """
    collection = models.OneToOneField(
        Collection,
        on_delete=models.CASCADE,
        related_name='collection_product_mapping_collection',
        verbose_name='Collection',
        unique=True,
        limit_choices_to={'is_active': '1'}
    )
    mapped_products = models.ManyToManyField(
        Product,
        limit_choices_to={'is_active': '1'},
        verbose_name='Mapped Product(s)'
    )

    class Meta:
        verbose_name = ADMIN_MODELS['CollectionProductMapping']
        verbose_name_plural = ADMIN_MODELS['CollectionProductMapping']
        db_table = 'collection_product_mapping'

    # def collection_details(self):
    #     if self.collection:
    #       product_collection = ProductDetails(product_collection=self.collection)
    #       return product_collection()[2]
    # collection_details.short_description = 'Collection Name'

    # def mapped_products_details(self):
    #     mapped_products_details = ProductAllDetails(instance = self.mapped_products)
    #     return mapped_products_details()
    # mapped_products_details.short_description = 'Mapped Product(s)'

    def __str__(self):
        return self.collection.collection_name


class CategoryProductMapping(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    category product mapping
    """
    category = models.OneToOneField(
        Category, on_delete=models.CASCADE,
        related_name='category_product_mapping_category',
        verbose_name='Category',
        unique=True,
        limit_choices_to={'is_active': '1'}
    )
    mapped_products = models.ManyToManyField(
        Product,
        limit_choices_to={'is_active': '1'},
        verbose_name='Mapped Product(s)'
    )

    class Meta:
        verbose_name = ADMIN_MODELS['CategoryProductMapping']
        verbose_name_plural = ADMIN_MODELS['CategoryProductMapping']
        db_table = 'category_product_mapping'

    # def mode_details(self):
    #   if self.mode:
    #     product_mode = ProductDetails(product_mode=self.mode)
    #     return product_mode()[1]
    # mode_details.short_description = 'Mode Name'

    # def mapped_products_details(self):
    #   mapped_products_details = ProductAllDetails(instance = self.mapped_products)
    #   return mapped_products_details()
    # mapped_products_details.short_description = 'Mapped Product(s)'


def __str__(self):
    return self.mode.mode_name


class ProductImages(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    ProductImages
    """
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='product_images_product',
        verbose_name='Product Details',
        limit_choices_to={'is_active': '1'}
    )
    short_image = models.ImageField(
        upload_to='product/short_images',
        verbose_name='Product Image (Small)'
    )
    large_image = models.ImageField(
        upload_to='product/large_image',
        verbose_name='Product Image (Large)'
    )


class Meta:
    verbose_name = ADMIN_MODELS['ProductImages']
    verbose_name_plural = ADMIN_MODELS['ProductImages']
    db_table = 'product_images'

    # def product_details(self):
    #   if self.product:
    #     product_details = ProductDetails(product=self.product)
    #     return product_details()[0][0]
    # product_details.short_description = 'Product Name'

    # def product_short_image(self):
    #   if self.short_image:
    #     return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.short_image))
    #   return 'No Image'
    # product_short_image.short_description = 'Product Image (Small)'

    # def product_large_image(self):
    #   if self.large_image:
    #     return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.large_image))
    #   return 'No Image'
    # product_large_image.short_description = 'Product Image (Large)'


def __str__(self):
    return self.product.product_name


class ProductVariant(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    ProductVariant
    """
    primary_product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='product_variant_primary_product',
        verbose_name='Primary Product Details',
        limit_choices_to={'status': '1', 'active_status': '1'}
    )
    matching_product = models.ManyToManyField(
        Product,
        limit_choices_to={'status': '1', 'active_status': '1'},
        verbose_name='Matching Product Detail(s)'
    )

    class Meta:
        verbose_name = ADMIN_MODELS['ProductVariant']
        verbose_name_plural = ADMIN_MODELS['ProductVariant']
        db_table = 'product_variant'

    # def product_details(self):
    # if self.primary_product:
    #   product_details = ProductDetails(product=self.primary_product)
    #   return product_details()[0][0]
    # product_details.short_description = 'Primary Product Name'

    # def product_image(self):
    # if self.primary_product:
    #   product_image_instance = ProductImages.objects.filter(product=self.primary_product.id,
    #         status=1, active_status=1).first()
    #   if product_image_instance:
    #     return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (product_image_instance.short_image))
    # return 'No Image'
    # product_image.short_description = 'Product Image'

    # def matching_product_details(self):
    # matching_product_details = ProductAllDetails(instance = self.matching_product)
    # return matching_product_details()
    # matching_product_details.short_description = 'Matching Product Detail(s)'

    def __str__(self):
        return self.primary_product.product_name



class Review(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="review")
    name = models.CharField(max_length=255)
    review_title = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    rating = models.PositiveIntegerField()
    remark = models.TextField()

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.name
