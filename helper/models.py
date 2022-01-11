"""
Helper Level Models
This module used to create ABSTRACT level all database models to reuse the all tables
"""

# import Auth user models
from django.contrib.auth.models import User
# import django models
from django.db import models
# third party smart select models
from smart_selects.db_fields import ChainedForeignKey


class AbstractCreatedByUpdatedBy(models.Model):
    """
    creation updation by abstract model
    created by and updated by inherit with all configuration and need full models
    created by and updated by is a auth user
    """

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='created_%(class)ss',
        verbose_name='Created By',
        limit_choices_to=~models.Q(is_staff=0, is_superuser=0),
        db_column='created_by'
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='updated_%(class)ss',
        verbose_name='Updated By',
        limit_choices_to=~models.Q(is_staff=0, is_superuser=0),
        db_column='updated_by'
    )

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class AbstractDate(models.Model):
    """DateAbstractModel date model
    created_at and updated_at inherit with all configuration and need full models
    created_at and updated_at is a DateTimeField field for track every records by date
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class AbstractStatus(models.Model):
    """status abstract model
    is_active define every records to records is active or not for live application system
    """

    is_active = models.BooleanField(default=True)

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class AbstractMetaTag(models.Model):
    """MetaTagAbstractModel
    Meta Tag Models add in meta tag with all models which need for that
    """
    meta_title = models.CharField(
        max_length=250,
        verbose_name="Meta Title",
        null=True, blank=True
    )
    meta_description = models.TextField(
        verbose_name="Meta Description",
        null=True,
        blank=True
    )
    keywords = models.CharField(
        max_length=250,
        verbose_name="Keyword",
        null=True, blank=True
    )

    class Meta:
        """
        class container with some option attached to the model
        """
        abstract = True


class AbstractLocationMaster(models.Model):
    """Abstract Location Master
    location master abstract model
    This AbstractMetaTag models used to add all location at one time using inherit feature
    country:ForeignKey
    state:ChainedForeignKey
    city: ChainedForeignKey
    ChainedForeignKey used for select the multi select feature with location mappings
    """
    country = models.ForeignKey(
        'location.CountryMaster',
        related_name='country_%(class)ss',
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': '1'},
        db_column='country',
        null=True, blank=True
    )
    state = ChainedForeignKey(
        'location.StateMaster',
        chained_field="country",
        chained_model_field="country",
        limit_choices_to={'is_active': '1'},
        related_name='state_%(class)ss',
        on_delete=models.CASCADE,
        show_all=True, auto_choose=True, sort=True,
        null=True, blank=True,
        db_column='state'
    )
    city = models.CharField(max_length=100, null=True, blank=True)
    # city = ChainedForeignKey(
    #     'location.CityMaster',
    #     chained_field='state',
    #     chained_model_field='state',
    #     limit_choices_to={'is_active': '1'},
    #     related_name='city_%(class)ss',
    #     on_delete=models.CASCADE,
    #     null=True, blank=True,
    #     show_all=True, auto_choose=True, sort=True,
    #     db_column='city'
    # )

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class AbstractLocationMasterMandatory(models.Model):
    """
    location master abstract model Mandatory
    same as AbstractLocationMaster but its also provide with mandotary functionality
    """
    country = models.ForeignKey(
        'location.CountryMaster',
        related_name='country_%(class)ss',
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': '1'},
        db_column='country',
    )
    state = ChainedForeignKey(
        'location.StateMaster',
        chained_field="country",
        chained_model_field="country",
        limit_choices_to={'is_active': '1'},
        related_name='state_%(class)ss',
        on_delete=models.CASCADE,
        show_all=True, auto_choose=True, sort=True,
        db_column='state'
    )
    city = ChainedForeignKey(
        'location.CityMaster',
        chained_field='state',
        chained_model_field='state',
        limit_choices_to={'is_active': '1'},
        related_name='city_%(class)ss',
        on_delete=models.CASCADE,
        show_all=True, auto_choose=True, sort=True,
        db_column='city'
    )

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True


class AbstractColor(models.Model):
    """
    colors AbstractColor model
    color define in product table
    """
    COLOR_CHOICE = (
        ('red', 'red'),
        ('yellow', 'yellow'),
        ('blue', 'blue'),
        ('brown', 'brown'),
        ('green', 'green'),
        ('black', 'black'),
        ('white', 'white')

    )
    

    product_color = models.CharField(max_length=10, choices=COLOR_CHOICE , null=True, blank=True)

    class Meta:
        """
        class container with some options attached to the model
        """
        abstract = True

