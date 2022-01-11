from django.contrib import admin
from datetime import datetime
from .models import Offer, VoucherSetConfiguration, Voucher, VoucherApplication


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



class OfferAdmin(admin.ModelAdmin):
    """
    OfferAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['name','offer_type','offer_price_type']
    list_filter = [
		'name',
        'offer_type',
        'offer_price_type',
        'is_location_applicable',
        'updated_by',
        'updated_at',
        'created_by',
        'created_at'
	]

    list_display = [
		'name',
        'offer_type',
        'offer_price_type',
        'value',
        'is_location_applicable',
		'is_active',
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
        return False

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

class VoucherSetConfigurationAdmin(admin.ModelAdmin):
    """
    VoucherSetConfigurationAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['name','count']
    list_filter = [
		'name',
        'count',
        'start_datetime',
        'end_datetime',
	]

    list_display = [
		'name',
        'count',
        'start_datetime',
        'end_datetime',
        'date_created'

		
    ]

    exclude = [
     'date_created', 
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return False

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

class VoucherAdmin(admin.ModelAdmin):
    """
    VoucherAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['name','voucher_type']
    list_filter = [
		'name',
        'voucher_type',
        'start_datetime',
        'end_datetime',
        'date_created'
	]

    list_display = [
		'name',
        'voucher_type',
        'start_datetime',
        'end_datetime',
        'date_created'

		
    ]

    exclude = [
     'date_created', 
    ]

    list_per_page = 8

    actions = [make_active_data, make_deactive_data]

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission
        used to remove delete functionalty in admin panel.
        """
        return False

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

admin.site.register(Offer, OfferAdmin)
admin.site.register(VoucherSetConfiguration, VoucherSetConfigurationAdmin)
admin.site.register(Voucher, VoucherAdmin)


