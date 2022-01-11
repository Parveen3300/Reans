"""
HomeDashBoard MAIN Screens 
"""

# import catalogue models
from catalogue.models import Category
from catalogue.models import CategoryProductMapping
from catalogue.models import Product
# import CMS model
from cms.models import DealOfTheDayProduct
from basket.models import Basket
# import offer models
from offer_coupon_voucher.models import Offer


class Home:
    """
    Home View Module
    This Home class module used to set all home level task in multiple methods
    """

    def __init__(self, **kwargs):
        self.response_dict = {
            'status': False,
            'message': 'data not found',
        }
        self.category_id = kwargs.get('category_id')
        self.product_id = kwargs.get('product_id')
        self.product_get_data = kwargs.get('product_get_data')
        self.filter_input_data = kwargs.get('filter_input_data')

    @staticmethod
    def simple_category_list():
        """
        This 'simple_category_list' used to get all active category list
        """
        category_queryset = Category.objects.filter(
            is_active=True
        ).order_by('-created_at')
        if category_queryset:
            return category_queryset

    @staticmethod
    def product_category_list():
        """
        This 'product_category_list' used to get all product as per category list
        """
        category_product_mapping_instance = CategoryProductMapping.objects.filter()
        if category_product_mapping_instance:
            return category_product_mapping_instance.order_by('-created_at')

    def product_list_from_category(self):
        """
        This 'product_category_list' used to get all product as per category request id
        """
        try:
            category_product_mapping_instance = CategoryProductMapping.objects \
                .get(category_id=self.category_id)
        except CategoryProductMapping.DoesNotExist:
            print('G61')
            print('CategoryProductMapping.DoesNotExist.Exception')
            category_product_mapping_instance = None
        return category_product_mapping_instance.mapped_products.all() \
            if category_product_mapping_instance else []

    def get_product_instance(self):
        """
        This 'get_product_instance' used to get a single product instance as per product filter id
        """
        try:
            return Product.objects.get(**self.product_get_data)
        except Product.DoesNotExist:
            print('G73')
            print('Product.DoesNotExist.Exception')
            return None

    @staticmethod
    def deal_day_product():
        """
        This 'deal_day_product' method used display of deal of the day product 
        to manage from cms panel
        """
        deal_instance = DealOfTheDayProduct.objects.filter(
            is_active=True).last()
        if deal_instance:
            return deal_instance

    def category_product_mapping_instance(self):
        """
        This 'deal_day_product' method used display of deal of the day product 
        to manage from cms panel
        """
        product_category_mapping_instance = CategoryProductMapping.objects \
            .filter(**self.filter_input_data)
        if product_category_mapping_instance:
            return product_category_mapping_instance

    def offer_products(self):
        """
        This 'offer_products' get the offer of product and calculate the price
        """
        offer_instance = Offer.objects.filter(**self.filter_input_data)
        if offer_instance:
            return offer_instance

    @staticmethod
    def random_products_list():
        """
        @ravi singh
        This 'random_products_list' methods used to get random category products list 
        for display on anywhere will required
        """
        try:
            return CategoryProductMapping.objects \
                .get(category=Category.objects.order_by('?')[0]) \
                .mapped_products.all()
        except Exception as e:
            print('G113')
            print(e)
            return []

    @staticmethod
    def basket_products_detail(**kwargs):
        """
        @ravi singh
        basket_products_detail
        """
        basket_instance = Basket.objects.filter(
            owner=kwargs.get('customer_instance.id'))
        print("rarararrarara", basket_instance.last())
        if basket_instance:
            basket_products = BasketProductLine.objects.filter(
                basket=basket_instance.last())
            return basket_products
        return []
