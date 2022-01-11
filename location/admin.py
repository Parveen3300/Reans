from django.contrib import admin
from .models import CountryMaster, StateMaster, CityMaster
from datetime import datetime

# function of active the data for all project records
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



class CountryMasterAdmin(admin.ModelAdmin):
    """
    CountryMasterAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['country',]
    list_filter = [
		'country',
        'updated_by',
        'updated_at',
        'created_by',
        'created_at'
	]

    list_display = [
		'country',
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



class StateMasterAdmin(admin.ModelAdmin):
    """
    CurrencyMasterAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['state',]
    list_filter = [
		'state',
        'updated_by',
        'updated_at',
        'created_by',
        'created_at'
	]

    list_display = [
		'state',
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

class CityMasterAdmin(admin.ModelAdmin):
    """
    CityMasterAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['city',]
    list_filter = [
		'city',
        'updated_by',
        'updated_at',
        'created_by',
        'created_at'
	]

    list_display = [
		'city',
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


admin.site.register(CountryMaster, CountryMasterAdmin)
admin.site.register(StateMaster, StateMasterAdmin)
admin.site.register(CityMaster, CityMasterAdmin)

