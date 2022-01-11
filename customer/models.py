"""CustomerRelatedModels
"""

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
# import django modules
from django.db import models
# import third party apps
from phonenumber_field.modelfields import PhoneNumberField

# import configuration models
from configuration.models import BusinessType
# import abstract models
from helper.models import AbstractCreatedByUpdatedBy
from helper.models import AbstractDate
from helper.models import AbstractLocationMaster
from helper.models import AbstractStatus

# import location models


ADMIN_MODELS = dict(
    CustomerProfile='Customer Profile',
    CustomerAsCompany='Customer As Company',
    CustomerAddress='Customer Address',
)


class CustomerProfile(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractLocationMaster
):
    # auth user OneToOne for mapped the auth user for authentication
    # and use django auth user security features
    ##############################################
    auth_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile_auth_user'
    )

    # Customer basic details
    ######################### 
    customer_full_name = models.CharField(
        max_length=100,
        verbose_name='Customer Name'
    )
    email = models.EmailField(
        max_length=100,
        verbose_name='Email Id',
        null=True, blank=True
    )
    mobile = models.CharField(max_length=15, verbose_name='Mobile No.', 
                              null=True, blank=True)
    mobile_with_isd = models.CharField(
        max_length=20,
        verbose_name='Mobile No. with ISD Code',
        null=True, blank=True
    )
    isd = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999), MinValueValidator(1)],
        verbose_name='ISD/Country Code',
        null=True, blank=True
    )

    # other details
    ####################
    gender = models.CharField(
        max_length=20,
        blank=True, null=True,
        verbose_name='Gender'
    )
    code = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name='Customer Code'
    )
    designation = models.CharField(
        max_length=100,
        verbose_name='Designation',
        null=True, blank=True
    )
    profile_picture = models.ImageField(
        upload_to='user_profile_images/',
        verbose_name='Customer Profile Pic',
        null=True, blank=True
    )

    # device related data
    #######################
    registration_type = models.CharField(
        max_length=255,
        choices=(('android', 'Mobile/Android'), ('ios', 'Mobile/iOS'), ('web', 'Web')),
        verbose_name='Registration Type'
    )
    device_id = models.CharField(max_length=255, blank=True, null=True)
    imei_no = models.CharField(max_length=100, blank=True, null=True)
    device_name = models.CharField(max_length=100, blank=True, null=True)

    timezone_name = models.CharField(
        max_length=50,
        verbose_name='Timezone',
        blank=True, null=True
    )

    # boolean flag
    ################
    is_mobile_verified = models.BooleanField(default=0)
    is_company_created = models.BooleanField(default=0)

    # def profile_image(self):
    #     if self.profile_picture:
    #         return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.profile_picture))
    #     return 'No Image'
    # profile_image.short_description = 'Customer Profile Pic'

    # def customer_mobile_with_isd(self):
    #   if self.mobile_with_isd:
    #     return "+"+str(self.mobile_with_isd)
    #   return "-"
    # customer_mobile_with_isd.short_description = 'Mobile No. with ISD Code'

    class Meta:
        verbose_name = ADMIN_MODELS['CustomerProfile']
        verbose_name_plural = ADMIN_MODELS['CustomerProfile']
        db_table = 'customer_profile'

    def __str__(self):
        return self.customer_full_name


class CustomerAsCompany(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractLocationMaster
):
    # customer profile one to one field
    # mapped the customer company data
    ##################################
    customer = models.OneToOneField(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='customer_company_customer',
        verbose_name='Customer Details'
    )

    # Company Basic Details
    #######################
    customer_company_name = models.CharField(
        max_length=30,
        verbose_name='Customers’ Company Name',
    )
    brand = models.CharField(max_length=30, null=True, blank=True)
    business_type = models.ForeignKey(
        BusinessType,
        on_delete=models.CASCADE,
        related_name='customer_company_business_type',
        verbose_name='Business Type',
        null=True, blank=True
    )
    isd = models.PositiveIntegerField(
        validators=[MaxValueValidator(99999), MinValueValidator(1)],
        verbose_name='ISD/ Country Code'
    )
    contact_no = models.CharField(
        max_length=15,
        verbose_name='Company’s Mobile No. w/o ISD Code',
        null=True, blank=True
    )
    gst_no = models.CharField(
        max_length=15,
        verbose_name='GST Number',
        null=True, blank=True
    )
    pan_no = models.CharField(
        max_length=15,
        verbose_name='Pan Card Number',
        null=True, blank=True
    )
    aadhaar_no = models.CharField(
        max_length=15,
        verbose_name='Aadhaar Number',
        null=True, blank=True
    )
    mobile_with_isd = models.CharField(
        max_length=20,
        verbose_name='Company’s Mobile No. with ISD Code',
        null=True, blank=True
    )
    email_id = models.EmailField(
        max_length=70,
        verbose_name='Email Id',
        null=True, blank=True
    )

    # Company Address
    ##################
    is_existing_cx = models.BooleanField(
        default=False,
        verbose_name='Is existing Customer'
    )
    company_address = models.CharField(
        max_length=255,
        verbose_name='Address',
        blank=True, null=True
    )
    postcode = models.CharField(
        max_length=64,
        blank=True, null=True,
        verbose_name='ZIP Code'
    )
    latitude = models.CharField(
        max_length=30, null=True, blank=True,
        verbose_name='Latitude'
    )
    longitude = models.CharField(
        max_length=30, null=True, blank=True,
        verbose_name='Longitude'
    )
    landmark = models.CharField(max_length=255, blank=True, null=True)

    # Company Website link
    ###########################
    website = models.URLField(
        max_length=50,
        blank=True, null=True,
        verbose_name='Website'
    )

    # def customer_first_name(self):
    #   if self.customer.first_name:
    #     return self.customer.first_name
    #   return "-"
    # customer_first_name.short_description = 'Customer First Name'

    # def customer_last_name(self):
    #   if self.customer.last_name:
    #     return self.customer.last_name
    #   return "-"
    # customer_last_name.short_description = 'Customer Last Name'

    # def customer_mobile_with_isd(self):
    #   if self.customer.mobile_with_isd:
    #     return "+"+str(self.customer.mobile_with_isd)
    #   return "-"
    # customer_mobile_with_isd.short_description = 'Customer Mobile'

    # def customer_email(self):
    #   if self.customer.email:
    #     return self.customer.email
    #   return "-"
    # customer_email.short_description = 'Customer Email'

    # def company_mobile_with_isd(self):
    #   if self.mobile_with_isd:
    #     return "+"+str(self.mobile_with_isd)
    #   return "-"
    # company_mobile_with_isd.short_description = 'Company’s Mobile No. with ISD Code'

    class Meta:
        verbose_name = ADMIN_MODELS['CustomerAsCompany']
        verbose_name_plural = ADMIN_MODELS['CustomerAsCompany']

    def __str__(self):
        return self.customer_company_name


class CustomerAddress(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractLocationMaster
):
    """
    Customer Address model tables
    """

    # customer profile one to one field 
    # mapped the customer company data
    ##################################
    customer = models.OneToOneField(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='customer_address_master',
        verbose_name='Customer Details'
    )
    customer_address_type = models.CharField(
        max_length=30,
        verbose_name='Address Type',
        choices=[('billing', 'Billing'), ('shipping', 'Shipping')]
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    line1 = models.CharField(max_length=255, null=True, blank=True)
    line2 = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.PositiveIntegerField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    is_same = models.BooleanField(null=True,blank=True)

    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profile'

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = ADMIN_MODELS['CustomerAddress']
        verbose_name_plural = ADMIN_MODELS['CustomerAddress']

    def __str__(self):
        return str(self.line1)
