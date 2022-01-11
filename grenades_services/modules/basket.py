"""
BasketManagementRelated modules
"""
# import basket models
from basket.models import Basket
from basket.models import BasketProductLine

# import configuration models
from grenades_services.all_configuration_data import get_currency_instance
from grenades_services.all_configuration_data import get_customer_instance_from_request_user
from grenades_services.all_configuration_data import product_price_calculator

# import home modules
from grenades_services.modules.home import Home

# import serializers modules
from grenades_services.separate_serializers.basket_serializers import \
    BasketProductSerializer


class UpdateProductsBasket:
    """
    UpdateProductsBasket
    """

    def __init__(self, **kwargs):
        self.basket_data = kwargs
        self._request = kwargs.get('request')
        self.basket_id = None
        self.customer_instance = None
        self.filter_query_data = kwargs.get(
            'filter_query_data', {'status': 'Open'})

    @staticmethod
    def _use_common_module(filter_input_data):
        """
        in this '_use_common_module' used to get the common request instance 
        as per request filter data
        In this Home class module will cover all filter logic to help of product basket class modules
        """
        return Home(**filter_input_data)

    @staticmethod
    def calculate_offer_value(product_offer_instance, product_price):
        """
        in this calculate_offer_value method we have calculate the product pricing according to the offer
        product_offer_instance: for get the offer related key fields
        manage two types of offer price
        RUPPPEES & PERCENTAGE
        """
        if product_offer_instance.offer_price_type == 'RUPPPEES':
            if product_price > product_offer_instance.value:
                return product_price - product_offer_instance.value
            return product_price

        if product_offer_instance.offer_price_type == 'PERCENTAGE':
            if product_price > product_offer_instance.value:
                return (product_offer_instance.value * product_price) / 100
            return product_price

    def get_basket_instance(self, _filter_query_data=None):
        """
        This 'get_basket_instance' method used to get the basket instance according 
        to auth user and session basket id or with inherit
        """
        try:
            print(self.filter_query_data)
            return Basket.objects.get(**_filter_query_data) \
                if _filter_query_data else Basket.objects.get(**self.filter_query_data)
        except Exception as e:
            print('Basket.DoesNotExist.Error')
            print(e)
            return None

    def collect_basket_product_values(self):
        """collect_basket_product_values
        This 'collect_basket_product_values' method used to collect the all basket related value data
        to entered in basket table with customer and session maintain instance
        """
        home_instance = self._use_common_module(dict(
            product_get_data={
                'product_alias_name': self.basket_data['product_alias_name']
            }
        )
        )
        product_instance = home_instance.get_product_instance()
        if product_instance:
            home_instance = self._use_common_module(
                dict(filter_input_data={'mapped_products__id__in': [product_instance.id]}))
            category_product_mapping_instance = \
                home_instance.category_product_mapping_instance()
            home_instance = self._use_common_module(
                dict(filter_input_data={
                    'included_products__id__in': [product_instance.id],
                    'offer_type': 'offer'
                })
            )
            product_offer_instance = home_instance.offer_products()
            payable_amount = self.calculate_offer_value(
                product_offer_instance,
                product_instance.price) if product_offer_instance else product_instance.price

        return (product_instance,
                category_product_mapping_instance,
                payable_amount)

    @staticmethod
    def create_basket_product_line(basket_create_data):
        """
        This 'create_basket_product_line' method used to create the basket
        """
        create_basket_line = BasketProductLine.objects.create(
            **basket_create_data)
        return True if create_basket_line else False

    def collect_basket_details(self, basket_instance):
        """
        This 'collect_basket_details' method collect the basket common code details
        """
        product_instance, category_product_mapping_instance, payable_amount = \
            self.collect_basket_product_values()
        return {
            'basket': basket_instance,
            'line_reference': str(product_instance.id),
            'product': product_instance,
            'category': category_product_mapping_instance.last(
            ).category if category_product_mapping_instance else None,
            'quantity': self.basket_data.get('quantity', 1),
            'price_currency': get_currency_instance(),
            'price_excl_tax': None,
            'price_incl_tax': None,
            'payable_amount': payable_amount
        }

    def add_new_basket(self):
        """
        This 'add_new_basket' method used to create a fresh basket for a customer or user
        """
        if self.customer_instance:
            self.filter_query_data['owner'] = self.customer_instance
        create_basket = Basket.objects.create(**self.filter_query_data)
        print("63546735435463543564", create_basket)
        if create_basket:
            if self.create_basket_product_line(self.collect_basket_details(create_basket)):
                self._request.session['basket_id'] = create_basket.id
                return True
            return False

    def update_product_basket(self):
        """
        This 'update_product_basket' method used to update the product in the basket
        """
        if self.basket_id:
            self.filter_query_data['id'] = self.basket_id
        if self.customer_instance:
            self.filter_query_data['owner'] = self.customer_instance
        basket_instance = self.get_basket_instance()
        if basket_instance:
            if self.create_basket_product_line(self.collect_basket_details(
                    basket_instance)):
                return True
            else:
                return False

    def add_to_basket(self):
        """
        This 'add_to_basket' method used to add the product in the basket
        """
        self.customer_instance = get_customer_instance_from_request_user(
            self._request.user)
        if 'basket_id' in self._request.session.keys():
            self.basket_id = self._request.session['basket_id']
            return self.update_product_basket()
        else:
            return self.add_new_basket()


class DisplayProductsBasket(UpdateProductsBasket):
    """
    DisplayProductsBasket
    return: {
        'products_description': {
            'id': 14,
            'products_list': [], 
            'line_reference': '2',
            'quantity': 1,
            'price_currency': 'INR',
            'price_excl_tax': None,
            'price_incl_tax': None,
            'payable_amount': '1000.00',
            'date_created': '2021-11-01T10:29:50.091484Z',
            'date_updated': '2021-11-01T10:29:50.091502Z',
            'basket': 5,
            'product': 2,
            'category': 5,
            'collection': None
        }, 
        'product_price_details': {'total_item': 0},
        'random_products_list': <QuerySet [<Product: Instruments>]>
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._request = kwargs.get('request')
        self.customer_instance = None
        self.basket_id = None
        self.products_description_data = []
        self.product_price_details = {}
        self.filter_data = {'status': 'Open'}
        self.estimate_tax = 0
        self.offer_name = '-'
        self.coupon_name = '-'

    @staticmethod
    def get_basket_product_lines(filter_query_data=None):
        """get_basket_product_lines
        This 'get_basket_product_lines' method is used to get the all instance of 
        products of basket
        """
        _product_line_instance = BasketProductLine.objects.filter(
            **filter_query_data)
        if _product_line_instance:
            return _product_line_instance

    def basket_product_description(self):
        """basket_product_description
        This 'basket_product_description' method used to get the all product description with
        all products details from baskets
        """
        if self.basket_id:
            self.filter_data['id'] = self.basket_id
        if self.customer_instance:
            self.filter_data['owner'] = self.customer_instance
        basket_instance = self.get_basket_instance(self.filter_data)
        if basket_instance:
            product_line_last_obj = self.get_basket_product_lines(
                {'basket': basket_instance}).last()
            self.products_description_data = BasketProductSerializer(
                product_line_last_obj).data

    def create_product_order_summary_dict(self, order_summary_dict):
        """
        This 'create_product_order_summary_dict' method used to create dict for product order summary
        total_price, coupon_price, offer_price
        """
        self.product_price_details['total'] = order_summary_dict['total_price']
        self.product_price_details['sub_total'] = order_summary_dict['total_price']
        self.product_price_details['estimate_tax'] = self.estimate_tax
        self.product_price_details['coupon_name'] = self.coupon_name
        self.product_price_details['coupon_price'] = order_summary_dict['coupon_price']
        self.product_price_details['offer_name'] = self.offer_name
        self.product_price_details['offer_price'] = order_summary_dict['offer_price']

    def order_product_price_details(self):
        """order_product_price_details
        This 'order_product_price_details' method used to get the all product order summary with price calculation
        and manage the all coupon and offers
        """
        self.product_price_details['total_item'] = len(
            self.products_description_data['products_list'])
        for _products_details in self.products_description_data['products_list']:
            order_summary_dict = product_price_calculator(_products_details,
                                                          self.coupon_details,
                                                          self.offer_details)

            # create product order summary
            # return total_price, coupon_price, offer_price
            self.create_product_order_summary_dict(order_summary_dict)

    def display_products(self):
        """
        This 'display_products' method used to get the all session and customer related
        basket products for help on display
        """
        if 'basket_id' in self._request.session.keys():
            self.basket_id = self._request.session.get('basket_id')
        else:
            self.basket_id = None
        self.customer_instance = get_customer_instance_from_request_user(
            self._request.user)
        self.basket_product_description()
        self.order_product_price_details()
        home_instance = Home()
        random_products_list = home_instance.random_products_list()
        return {
            'products_description': self.products_description_data,
            'product_price_details': self.product_price_details,
            'random_products_list': random_products_list if random_products_list else []
        }
