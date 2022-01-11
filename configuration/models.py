"""
Configuration Level Models
"""

from django.core.validators import MaxValueValidator
# import django validators
from django.core.validators import MinValueValidator
from django.db import models

from helper.models import AbstractCreatedByUpdatedBy
from helper.models import AbstractDate
from helper.models import AbstractMetaTag
from helper.models import AbstractStatus

ADMIN_MODELS = dict(
    LANGUAGE='Language Configuration',
    CURRENCY_MASTER='Currency Master',
    CONTACT_TYPE_REASON='Contact/Inquiry Type Reasons',
    RATING_PARAMETER='Rating Parameters',
    CANCELLATION_REASON='Cancellation Reasons',
    BUSINESS_TYPE='Business Type',
    PARAMETERS_SETTINGS='Parameter Setting',
    UNIT='  Unit Of Measurement'

)


class Language(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """Language configurations model table
    with abstract all needfull models
    """
    language_code = models.CharField(max_length=70, unique=True)
    language_name = models.CharField(max_length=70, verbose_name='Language', unique=True)

    class Meta:
        verbose_name_plural = verbose_name = ADMIN_MODELS['LANGUAGE']
        db_table = 'language_configuration'

    def __str__(self):
        return self.language_code


class CurrencyMaster(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """currency master model table
    with abstract all needfull models
    """
    currency = models.CharField(max_length=30, unique=True, verbose_name='Currency Name')
    symbol = models.CharField(max_length=30)
    code_iso = models.CharField(
        max_length=30,
        null=True, blank=True,
        verbose_name='Code ISO')
    hex_symbol = models.CharField(max_length=30,
                                  null=True, blank=True,
                                  verbose_name='Hex Code')

    class Meta:
        verbose_name = ADMIN_MODELS['CURRENCY_MASTER']
        verbose_name_plural = ADMIN_MODELS['CURRENCY_MASTER']
        db_table = 'currency_master'

    def __str__(self):
        return self.currency


class ContactTypesReasons(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    Contact Types Reasons model table
    with abstract all needfull models
    """
    contact_reasons = models.CharField(max_length=100,
                                       unique=True,
                                       verbose_name='contact type Reasons')

    class Meta:
        verbose_name = ADMIN_MODELS['CONTACT_TYPE_REASON']
        verbose_name_plural = ADMIN_MODELS['CONTACT_TYPE_REASON']
        db_table = 'contact_types_reasons'

    def __str__(self):
        return str(self.contact_reasons)


class RatingParameter(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    rating parameters for
    candidate and employer with abstract all needfull models
    """
    rating_parameter = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Rating Parameter Name'
    )
    rating_parameter_value = models.IntegerField(
        null=True,
        unique=True,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
        verbose_name='Rating Points'
    )

    class Meta:
        verbose_name = ADMIN_MODELS['RATING_PARAMETER']
        verbose_name_plural = ADMIN_MODELS['RATING_PARAMETER']
        db_table = "rating_parameter_configuration"

    def __str__(self):
        """
        :return: rating parameter name
        """
        return str(self.rating_parameter)


class CancellationReason(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    list of all cancellation reasons with abstract all needfull models
    """
    cancel_reason_name = models.CharField(max_length=100, verbose_name='Cancellation Reason')
    cancel_reason_for = models.CharField(max_length=255)
    cancel_reason_details = models.CharField(max_length=255,
                                             blank=True, null=True,
                                             verbose_name='Description')

    class Meta:
        verbose_name = ADMIN_MODELS['CANCELLATION_REASON']
        verbose_name_plural = ADMIN_MODELS['CANCELLATION_REASON']
        db_table = 'cancellation_reason_configuration'

    def __str__(self):
        return self.cancel_reason_name


class BusinessType(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    BusinessType Model Table
    """
    business_type = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = ADMIN_MODELS['BUSINESS_TYPE']
        verbose_name_plural = ADMIN_MODELS['BUSINESS_TYPE']
        ordering = ['business_type']
        db_table = 'business_type_manager'

    def __str__(self):
        return self.business_type


class ParameterSetting(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    prefix = models.CharField(max_length=4, verbose_name='Inquiry Prefix')

    def __str__(self):
        return self.prefix

    class Meta:
        verbose_name = ADMIN_MODELS['PARAMETERS_SETTINGS']
        verbose_name_plural = ADMIN_MODELS['PARAMETERS_SETTINGS']
        db_table = 'parameter_settings'


class UnitOfMeasurement(
    AbstractCreatedByUpdatedBy,
    AbstractDate,
    AbstractStatus,
    AbstractMetaTag
):
    """
    UnitOfMeasurement
    """
    unit_measurement = models.CharField(max_length=30, unique=True)
    short_form = models.CharField(max_length=10)
    description = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = ADMIN_MODELS['UNIT']
        verbose_name_plural = ADMIN_MODELS['UNIT']
        db_table = 'unit_of_measurement'

    def __str__(self):
        return self.unit_measurement
