"""CMS Models
"""

# import RichTextFields models
from ckeditor.fields import RichTextField

from django.db import models

# import helper models
from helper.models import AbstractCreatedByUpdatedBy
from helper.models import AbstractDate
from helper.models import AbstractMetaTag
from helper.models import AbstractStatus
from phonenumber_field.modelfields import PhoneNumberField


ADMIN_MODELS = dict(
    COMPANY_BANNER='Company Banner',
    PRODUCT_BANNER='Product Banner',
    HOME_PAGE_BANNER=' Product Banner/Home Page',
    CompanyLogo='Company Logo',
    DealOfTheDayProduct='Deal Of The Day Product',


)


# banner sequence
class CompanyBanner(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    COMPANY Banner Models Tables
    """
    banner_title = models.CharField(max_length=30, verbose_name='Banner Name')
    banner_image = models.ImageField(
        upload_to='company/banner_images',
        verbose_name='Banner Image (small)')
    banner_image_large = models.ImageField(
        upload_to='company/banner_images_large',
        verbose_name='Banner Image (large)')

    class Meta:
        verbose_name = ADMIN_MODELS['COMPANY_BANNER']
        verbose_name_plural = ADMIN_MODELS['COMPANY_BANNER']
        db_table = 'company_banner'

    def __str__(self):
        return self.banner_title


# def banner_small(self):
#   if self.banner_image:
#       return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.banner_image))
#       logo.allow_tags = True
#       #logo.short_description = 'Company Logo'
#   else:
#       return 'No Image'
# banner_small.short_description = 'Banner Image (small)'

# def banner_large(self):
#   if self.banner_image_large:
#       return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.banner_image_large))
#       logo.allow_tags = True
#       #logo.short_description = 'Company Logo'
#   else:
#       return 'No Image'
# banner_large.short_description = 'Banner Image (large)'


# banner sequence
class ProductBanner(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    ProductBanner
    """
    banner_title = models.CharField(max_length=30, verbose_name='Banner Name')
    banner_image = models.ImageField(
        upload_to='product/banner_images',
        verbose_name='Banner Image (small)')
    banner_image_large = models.ImageField(
        upload_to='product/banner_images_large',
        verbose_name='Banner Image (large)')


class Meta:
    verbose_name = ADMIN_MODELS['PRODUCT_BANNER']
    verbose_name_plural = ADMIN_MODELS['PRODUCT_BANNER']
    db_table = 'product_banner'


def __str__(self):
    return self.banner_title


# def banner_small(self):
#   if self.banner_image:
#       return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.banner_image))
#       logo.allow_tags = True
#       #logo.short_description = 'Company Logo'
#   else:
#       return 'No Image'
# banner_small.short_description = 'Banner Image (small)'

# def banner_large(self):
#   if self.banner_image_large:
#       return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.banner_image_large))
#       logo.allow_tags = True
#       #logo.short_description = 'Company Logo'
#   else:
#       return 'No Image'
# banner_large.short_description = 'Banner Image (large)'


# banner sequence
class HomePageBanner(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    HomePageBanner
    """
    banner_title = models.CharField(max_length=30, verbose_name='Home Name')
    banner_image = models.ImageField(
        upload_to='product/banner_images',
        verbose_name='Home Image (small)')
    banner_image_large = models.ImageField(
        upload_to='product/banner_images_large',
        verbose_name='Home Image (large)')


class Meta:
    verbose_name = ADMIN_MODELS['HOME_PAGE_BANNER']
    verbose_name_plural = ADMIN_MODELS['HOME_PAGE_BANNER']
    db_table = 'home_page_banner'


def __str__(self):
    return self.banner_title

# def banner_small(self):
#   if self.banner_image:
#       return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.banner_image))
#       logo.allow_tags = True
#       #logo.short_description = 'Company Logo'
#   else:
#       return 'No Image'
# banner_small.short_description = 'Home Banner Image (small)'

# def banner_large(self):
#   if self.banner_image_large:
#       return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.banner_image_large))
#       logo.allow_tags = True
#       #logo.short_description = 'Company Logo'
#   else:
#       return 'No Image'
# banner_large.short_description = 'Home Banner Image (large)'


# banner sequence
class WebsiteCompanyLogo(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    HomePageBanner
    """
    logo_title = models.CharField(max_length=30, verbose_name='Home Name')
    logo_image = models.ImageField(
        upload_to='company/logo_images',
        verbose_name='Logo Image (small)')
    logo_image_large = models.ImageField(
        upload_to='company/logo_images_large',
        verbose_name='Logo Image (large)')


class Meta:
    verbose_name = ADMIN_MODELS['CompanyLogo']
    verbose_name_plural = ADMIN_MODELS['CompanyLogo']
    db_table = 'website_logo'


def __str__(self):
    return self.banner_title


# banner sequence
class DealOfTheDayProduct(AbstractCreatedByUpdatedBy, AbstractDate, 
                          AbstractStatus, AbstractMetaTag):
    """
    HomePageBanner
    """
    title = models.CharField(max_length=30, verbose_name='Home Name')
    image = models.ImageField(
        upload_to='company/images',
        verbose_name='Logo Image',
        null=True, blank=True)
    short_description = models.TextField()
    content = RichTextField(null=True, blank=True)
    product = models.ForeignKey(
        'catalogue.Product',
        related_name='deal_product',
        on_delete=models.CASCADE,
        verbose_name='Deal Products',
        limit_choices_to={'is_active': '1'},
        blank=True, null=True
    )


class Meta:
    verbose_name = ADMIN_MODELS['DealOfTheDayProduct']
    verbose_name_plural = ADMIN_MODELS['DealOfTheDayProduct']
    db_table = 'deal_of_the_day_product'


def __str__(self):
    return self.banner_title



class TermsConditions(AbstractMetaTag,AbstractDate,AbstractStatus):
   
    terms_conditions = RichTextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Terms & Conditions"
        verbose_name_plural = "Terms & Conditions"


class ReplacementCancellationPolicy(AbstractMetaTag,AbstractDate,AbstractStatus):

    policy = RichTextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Replacement & Cancellation Policy"
        verbose_name_plural = "Replacement & Cancellation Policy"


class WebsitePolicy(AbstractMetaTag,AbstractDate,AbstractStatus):
   
    policy = RichTextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Website Policy"
        verbose_name_plural = "Website Policy"


class WebsiteCookiesPolicy(AbstractMetaTag,AbstractDate,AbstractStatus):
    
    policy = RichTextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Website Cookies Policy"
        verbose_name_plural = "Website Cookies Policy"


class AboutUs(AbstractMetaTag):

    body= RichTextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"



class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = PhoneNumberField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

