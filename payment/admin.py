from django.contrib import admin
from datetime import datetime
from .models import PaymentMethodOption, PaymentMethodConfiguration, PaymentTransaction

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



class PaymentMethodConfigurationAdmin(admin.ModelAdmin):
    """
    PaymentMethodConfigurationAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['pay_pal_id','pay_pal_name','credit_card_type']
    list_filter = [
		'pay_pal_id',
        'pay_pal_name',
        'credit_card_type',
        'expiry_date',
        'card_name',
        'created_datetime',
        'modified_datetime'
	]

    list_display = [
		'pay_pal_id',
        'pay_pal_name',
        'card_name',
        'credit_card_type',
        'expiry_date',
        'created_datetime',
        'modified_datetime'

		
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


class PaymentTransactionAdmin(admin.ModelAdmin):
    """
    PaymentTransactionAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['invoice_number','amount_type']
    list_filter = [
		'invoice_number',
        'amount_type',
        'payment_status',
        'amount',
        'transaction_id',
        'initiated_by'
	]

    list_display = [
		'invoice_number',
        'transaction_id',
        'amount_type',
        'payment_status',
        'amount',
        'initiated_by',
        'payment_datetime'
    

		
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


admin.site.register(PaymentMethodConfiguration, PaymentMethodConfigurationAdmin)
admin.site.register(PaymentMethodOption)
admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
