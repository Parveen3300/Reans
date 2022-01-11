
from catalogue.models import Category
from catalogue.models import Product


def get_related_products():
    """
    get_related_products
    """
    relate_product = Product.objects.filter(is_active=True)
    if relate_product:
        return relate_product
    return []


def get_product_instance(product_filter_data):
    """
    get_product_instance
    """
    product_instance = Product.objects.filter(**product_filter_data).last()
    if product_instance:
        return product_instance
    return None


def get_category_instance(product_filter_data):
    category_instance = Category.objects.filter(**product_filter_data).last()
    if category_instance:
        return category_instance
    return None
