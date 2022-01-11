from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (Collection, Category, Product, Feature, Specification,
                    CollectionProductMapping, CategoryProductMapping,
                    ProductImages, ProductVariant, Review)

from datetime import datetime
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


class CollectionAdmin(admin.ModelAdmin):
    """
    CollectionAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['collection_name', 'collection_code','collection_year', 'from_date']
    list_filter = [
        'collection_name',
        'collection_code',
        'collection_year',
        'from_date',
        'to_date',
    ]

    list_display = [
        'collection_name',
        'collection_code',
        'collection_year',
        'from_date',
        'to_date',
        'created_at',
        'created_by',
     
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


class ReviewAdmin(admin.ModelAdmin):
    """
    ReviewAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['name', 'email']
    list_filter = [
        'name',
        'email',
        'rating',
    ]

    list_display = [
        'name',
        'email',
    
        'rating',
        'created_at',
        'created_by',
     
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


class CategoryAdmin(admin.ModelAdmin):
    """
    CategoryAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['category_name', 'category_code', 'is_color_variant_applicable']
    list_filter = [
        'category_name',
        'category_code',
    ]

    list_display = [
        'category_name',
        'category_code',
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
     
    ]

    exclude = [
        'created_at',
        'created_by',
        'updated_by',
        'updated_at',
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

class ProductAdmin(admin.ModelAdmin):
    """
    ProductAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['product_name', 'product_code', 'sku', 'is_available']
    list_filter = [
        'product_name',
        'product_code',
        'sku'
    ]

    list_display = [
        'product_name',
        'product_code',
        'sku',
        'is_available',
        'product_alias_name',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
     
    ]

    exclude = [
        'created_at',
        'created_by',
        'updated_by',
        'updated_at',
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

class FeatureAdmin(admin.ModelAdmin):
    """
    FeatureAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['feature', ]
    list_filter = [
        'feature',
    ]

    list_display = [
        'feature',
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
     
    ]

    exclude = [
        'created_at',
        'created_by',
        'updated_by',
        'updated_at',
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

class SpecificationAdmin(admin.ModelAdmin):
    """
    SpecificationAdmin
    all required listing data for
    admin panel
    """
    search_fields = ['name','value' ]
    list_filter = [
        'name',
        'value'
    ]

    list_display = [
        'name',
        'value',
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by'
     
    ]

    exclude = [
        'created_at',
        'created_by',
        'updated_by',
        'updated_at',
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

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(CollectionProductMapping)
admin.site.register(CategoryProductMapping)
admin.site.register(ProductImages)
admin.site.register(ProductVariant)
admin.site.register(Review, ReviewAdmin)

