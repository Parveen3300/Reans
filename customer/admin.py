from django.contrib import admin
from datetime import datetime
from .models import CustomerProfile, CustomerAsCompany, CustomerAddress

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


class CustomerProfileAdmin(admin.ModelAdmin):
    """
    CustomerProfileAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['customer_full_name', 'email', 'mobile','designation']
    list_filter = [
        'customer_full_name',
        'email',
        'mobile',
        'designation',
        'registration_type',
        'imei_no'
    ]

    list_display = [
        'customer_full_name',
        'email',
        'mobile',
        'designation',
        'registration_type',
        'imei_no',
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

class CustomerAsCompanyAdmin(admin.ModelAdmin):
    """
    CustomerAsCompanyAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['customer_company_name', 'brand', 'contact_no','gst_no', 'email_id']
    list_filter = [
        'customer_company_name',
        'brand',
        'contact_no',
        'gst_no',
        'email_id',
        'landmark',
        'pan_no'
    ]

    list_display = [
        'customer_company_name',
        'brand',
        'contact_no',
        'gst_no',
        'landmark',
        'pan_no',
        'email_id',
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

class CustomerAddressAdmin(admin.ModelAdmin):
    """
    CustomerAddressAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['customer_address_type', 'first_name', 'last_name','postcode', 'email']
    list_filter = [
        'customer_address_type',
        'first_name',
        'last_name',
        'postcode',
        'email',
        'phone_number'
      
    ]

    list_display = [
        'customer_address_type',
        'first_name',
        'last_name',
        'email',
        'postcode',
        'phone_number',
        'line1',
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

admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(CustomerAsCompany, CustomerAsCompanyAdmin)
admin.site.register(CustomerAddress, CustomerAddressAdmin)