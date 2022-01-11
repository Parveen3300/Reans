"""
Location Level Database Models
"""

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
# import django modules
from django.db import models

# import configuration modules
from configuration.models import CurrencyMaster
# import abstract modules
from helper.models import AbstractCreatedByUpdatedBy
from helper.models import AbstractDate
from helper.models import AbstractStatus

"""
Gour@vSh@rm@(^_^)
14 October 2021
Location module models
This model is designed for the manage location in the project.
"""

ADMIN_MODELS = dict(

    COUNTRY_MASTER='  Country Master',
    STATE_MASTER=' State Master',
    CITY_MASTER='City Master',
)


class CountryMaster(AbstractCreatedByUpdatedBy, AbstractDate, AbstractStatus):
    """
    country master table
    """
    country = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='Country'
    )
    isd = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(99999),
            MinValueValidator(1)
        ],
        verbose_name='ISD/Country Code',
        null=True, blank=True,
    )
    mobile_no_digits = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(15),
            MinValueValidator(5)
        ],
        verbose_name='Mobile Number digit',
        null=True, blank=True,
    )
    currency = models.ForeignKey(
        CurrencyMaster,
        on_delete=models.CASCADE,
        related_name='country_master_currency',
        verbose_name='Currency',
        limit_choices_to={'is_active': '1'},
        null=True, blank=True,
    )
    code = models.CharField(
        max_length=10,
        null=True, blank=True,
        verbose_name='ISO Code'
    )
    timezone = models.CharField(
        max_length=100,
        help_text='Please add correct country timezone.',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = ADMIN_MODELS['COUNTRY_MASTER']
        verbose_name_plural = ADMIN_MODELS['COUNTRY_MASTER']
        db_table = "country_master"

    def __str__(self):
        return self.country


class StateMaster(AbstractCreatedByUpdatedBy, AbstractDate, AbstractStatus):
    """
    all states master table
    """
    state = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name='State'
    )
    country = models.ForeignKey(
        CountryMaster,
        on_delete=models.CASCADE,
        verbose_name='Country Name',
        db_column='country',
        limit_choices_to={'is_active': '1'}
    )

    class Meta:
        verbose_name = ADMIN_MODELS['STATE_MASTER']
        verbose_name_plural = ADMIN_MODELS['STATE_MASTER']
        unique_together = ('country', 'state')
        db_table = "state_master"

    def __str__(self):
        return self.state


class CityMaster(AbstractCreatedByUpdatedBy, AbstractDate, AbstractStatus):
    """
    all states master table
    """
    city = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name='City'
    )
    state = models.ForeignKey(
        StateMaster,
        on_delete=models.CASCADE,
        verbose_name='State Name',
        db_column='state',
        limit_choices_to={'is_active': '1'}
    )

    class Meta:
        verbose_name = ADMIN_MODELS['CITY_MASTER']
        verbose_name_plural = ADMIN_MODELS['CITY_MASTER']
        unique_together = ('state', 'city')
        db_table = "city_master"

    def __str__(self):
        return self.city
