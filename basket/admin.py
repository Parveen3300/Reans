from datetime import datetime
from django.contrib import admin
from .models import Basket, BasketProductLine

# Register your models here.


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


class BasketAdmin(admin.ModelAdmin):
    """
    BasketAdmin
    all required listing data for
    admin panel
    """
    search_fields = []
    list_filter = [
        "owner",
        "status",


    ]

    list_display = [
        'owner',
        'status',
        'date_created',
        'date_submitted'

    ]

    exclude = [
        'created_at',
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


class BasketProductLineAdmin(admin.ModelAdmin):
    """
    BasketProductLineAdmin
    all required listing data for
    admin panel
    """
    search_fields = ["basket", ]

    list_filter = [
        "basket",
        "line_reference",
    ]

    list_display = [
        'basket',
        'line_reference',
        "quantity",
        "price_currency",
        "price_excl_tax",
        "price_incl_tax",
        "payable_amount"
    ]

    exclude = [
        'created_at',
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


admin.site.register(Basket, BasketAdmin)
admin.site.register(BasketProductLine, BasketProductLineAdmin)
