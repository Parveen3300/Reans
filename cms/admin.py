from django.contrib import admin
from .models import TermsConditions
from .models import ReplacementCancellationPolicy
from .models import WebsitePolicy
from .models import WebsiteCookiesPolicy
from .models import ContactUs
from .models import AboutUs
from datetime import datetime

# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
    """
    ContactUsAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['name', ]
    list_filter = [
        'name',
        'email',
        'mobile',
    ]

    list_display = [
        'name',
        'email',
        'mobile',
        'message',
    
      
    ]

    list_per_page = 8


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






admin.site.register(TermsConditions)
admin.site.register(ReplacementCancellationPolicy)
admin.site.register(WebsitePolicy)
admin.site.register(WebsiteCookiesPolicy)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(AboutUs)



