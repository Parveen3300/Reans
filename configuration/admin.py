from django.contrib import admin
from datetime import datetime
from .models import (Language, CurrencyMaster, 
                    ContactTypesReasons, RatingParameter,
                    CancellationReason,
                    BusinessType, ParameterSetting, UnitOfMeasurement)
# Register your models here.


def make_active_data(modeladmin, request, queryset):
    """
    make_active_data:
    activate the data from admin side.
    """
    queryset.update(is_active='1', updated_at=datetime.now())


make_active_data.short_description = "Move Items to Active"


# function of deactivate the data for all project records
def make_deactive_data(modeladmin, request, queryset):
    """
    make_deactive_data:
    deactivate the data from admin side.
    """
    queryset.update(is_active='0', updated_at=datetime.now())


make_deactive_data.short_description = "Move Items to Deactive"


class LanguageAdmin(admin.ModelAdmin):
    """
    LanguageAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['language_code', 'language_name']
    list_filter = [
        'language_name',
        'language_code',
    ]

    list_display = [
        'language_name',
        'language_code',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    ]

    exclude = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'is_active'
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return True

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission
        used to add and not add permission in admin panel.
        """
        return True

    def save_model(self, request, obj, form, change):
        """
        save_model
        used to change and update activity from admin panel.
        """
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()


class CurrencyMasterAdmin(admin.ModelAdmin):
    """
    CurrencyMasterAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['currency', 'code_iso']
    list_filter = [
        'currency',
        'code_iso',
    ]

    list_display = [
        'currency',
        'code_iso',
        'hex_symbol',
        'symbol',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    ]

    exclude = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'is_active',
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return True

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission
        used to add and not add permission in admin panel.
        """
        return True

    def save_model(self, request, obj, form, change):
        """
        save_model
        used to change and update activity from admin panel.
        """
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()


class ContactTypesReasonsAdmin(admin.ModelAdmin):
    """
    ContactTypesReasonsAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['contact_reasons']
    list_filter = [
        'contact_reasons'
    ]

    list_display = [
        'contact_reasons',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    ]

    exclude = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'is_active'
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return True

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission
        used to add and not add permission in admin panel.
        """
        return True

    def save_model(self, request, obj, form, change):
        """
        save_model
        used to change and update activity from admin panel.
        """
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()


class RatingParameterAdmin(admin.ModelAdmin):
    """
    RatingParameterAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['rating_parameter', 'rating_parameter_value']
    list_filter = [
        'rating_parameter',
        'rating_parameter_value',
    ]

    list_display = [
        'rating_parameter',
        'rating_parameter_value',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    ]

    exclude = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'is_active'
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return True

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission
        used to add and not add permission in admin panel.
        """
        return True

    def save_model(self, request, obj, form, change):
        """
        save_model
        used to change and update activity from admin panel.
        """
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()


class CancellationReasonAdmin(admin.ModelAdmin):
    """
    CancellationReasonAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['cancel_reason_name', 'cancel_reason_for']
    list_filter = [
        'cancel_reason_name',
        'cancel_reason_for',
    ]

    list_display = [
        'cancel_reason_name',
        'cancel_reason_for',
        'cancel_reason_details',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    ]

    exclude = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'is_active'
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return True

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission
        used to add and not add permission in admin panel.
        """
        return True

    def save_model(self, request, obj, form, change):
        """
        save_model
        used to change and update activity from admin panel.
        """
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()

class BusinessTypeAdmin(admin.ModelAdmin):
    """
    BusinessTypeAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['business_type']
    list_filter = [
        'business_type'
    ]

    list_display = [
        'business_type',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    ]

    exclude = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'is_active'
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return True

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission
        used to add and not add permission in admin panel.
        """
        return True

    def save_model(self, request, obj, form, change):
        """
        save_model
        used to change and update activity from admin panel.
        """
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()

class ParameterSettingAdmin(admin.ModelAdmin):
    """
    ParameterSettingAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['prefix']
    list_filter = [
        'prefix'
    ]

    list_display = [
        'prefix',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    ]

    exclude = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'is_active'
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return True

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission
        used to add and not add permission in admin panel.
        """
        return True

    def save_model(self, request, obj, form, change):
        """
        save_model
        used to change and update activity from admin panel.
        """
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save() 

class UnitOfMeasurementAdmin(admin.ModelAdmin):
    """
    UnitOfMeasurementAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['unit_measurement', 'short_form']
    list_filter = [
        'unit_measurement'
    ]

    list_display = [
        'unit_measurement',
        'short_form',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    ]

    exclude = [
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'is_active'
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return True

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission
        used to add and not add permission in admin panel.
        """
        return True

    def save_model(self, request, obj, form, change):
        """
        save_model
        used to change and update activity from admin panel.
        """
        if not change:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        obj.save()                


admin.site.register(Language, LanguageAdmin)
admin.site.register(CurrencyMaster, CurrencyMasterAdmin)
admin.site.register(ContactTypesReasons, ContactTypesReasonsAdmin)
admin.site.register(RatingParameter, RatingParameterAdmin)
admin.site.register(CancellationReason, CancellationReasonAdmin)
admin.site.register(BusinessType, BusinessTypeAdmin)
admin.site.register(ParameterSetting, ParameterSettingAdmin)
admin.site.register(UnitOfMeasurement, UnitOfMeasurementAdmin)

