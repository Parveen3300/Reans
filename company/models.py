"""

Company Level Database models

"""

# import validator models
from django.core.validators import FileExtensionValidator
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.db import models
# third party smart select models
from smart_selects.db_fields import ChainedForeignKey

# import Global messages
from helper.messages import MODEL_MSG
# import abstract modules
from helper.models import AbstractCreatedByUpdatedBy
from helper.models import AbstractDate
from helper.models import AbstractLocationMaster
from helper.models import AbstractStatus


# Create your models here.

class Company(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractLocationMaster
):
    """
    company details model table
    with abstract all need full models and with location master to define company locations
    """
    # phone regex validator
    ############################
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{8,15}$',
        message=MODEL_MSG['PHONENOMSG']
    )

    # comapny basic details
    ############################
    company_name = models.CharField(
        max_length=50, verbose_name='Company', unique=True)
    business_nature = models.CharField(max_length=100)
    address = models.TextField()
    zip_code = models.CharField(
        validators=[
            RegexValidator(regex=r'^[a-zA-Z0-9]+$', message=MODEL_MSG['ZIPCODEMSG']),
            MinLengthValidator(3)
        ],
        max_length=6,
        verbose_name='Zip Code'
    )
    owner_name = models.CharField(max_length=50, null=True)
    owner_email = models.EmailField(unique=True, verbose_name='Owner Email id')
    company_email_id = models.EmailField(unique=True)
    company_registration_no = models.CharField(max_length=200)
    owner_phone = models.CharField(
        max_length=15,
        verbose_name='Owner Mobile No.',
        validators=[phone_regex],
    )
    company_logo = models.FileField(
        upload_to='company_logo',
        null=True, blank=True,
        verbose_name='Company logo',
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])]
    )
    company_contact_no = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='Support company Mobile No.',
        validators=[phone_regex],
    )

    # contact person details
    ############################
    currency = models.ForeignKey(
        'configuration.CurrencyMaster',
        related_name='company_currency',
        on_delete=models.CASCADE,
        verbose_name='Currency',
        limit_choices_to={'is_active': '1'}
    )

    contact_person = models.CharField(
        max_length=100,
        verbose_name='Support Person Name'
    )
    contact_person_mobile_no = models.CharField(
        validators=[phone_regex], max_length=15, unique=True,
        verbose_name='Support Mobile No.')

    contact_person_email_id = models.EmailField(
        unique=True,
        verbose_name='Support Email ID'
    )

    # Company Billing Address
    ############################
    billing_address = models.CharField(
        max_length=100, verbose_name='Billing Address',
        null=True, blank=True)

    billing_country = models.ForeignKey(
        'location.CountryMaster',
        related_name='billing_country',
        on_delete=models.CASCADE,
        db_column='billing_country',
        null=True, blank=True,
        limit_choices_to={'is_active': '1'}
    )
    billing_state = ChainedForeignKey(
        'location.StateMaster',
        chained_field="billing_country",
        chained_model_field="country",
        db_column='billing_state',
        related_name='billing_state',
        on_delete=models.CASCADE,
        null=True, blank=True,
        show_all=True, auto_choose=True, sort=True,
        limit_choices_to={'is_active': '1'}
    )
    billing_city = ChainedForeignKey(
        'location.CityMaster',
        chained_field='billing_state',
        chained_model_field='state',
        related_name='billing_city',
        on_delete=models.CASCADE,
        db_column='billing_city',
        null=True, blank=True,
        show_all=True, auto_choose=True, sort=True,
        limit_choices_to={'is_active': '1'}
    )
    billing_currency = models.ForeignKey(
        'configuration.CurrencyMaster',
        related_name='billing_currency',
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': '1'},
        blank=True, null=True,
        verbose_name='Billing Currency'
    )

    # Website path location
    ############################
    website = models.URLField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = ' Company Master'
        verbose_name_plural = ' Company Master'
        db_table = 'company_master'

    def __str__(self):
        return self.company_name
