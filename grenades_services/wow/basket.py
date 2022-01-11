

from basket.models import Basket
from basket.models import BasketProductLine

from catalogue.models import Category
from catalogue.models import Product
from grenades_services.wow.products import get_category_instance


def create_basket_query(basket_instance, kwargs):
	"""
	create_basket_query
	"""
	return True if BasketProductLine.objects.create(
		basket=basket_instance.last(),
		line_reference='RAVI',
		product=kwargs.get('product_instance'),
		category=kwargs.get('product_instance').product_category.last(),
		price_incl_tax=kwargs.get('product_instance').price,
		price_excl_tax=kwargs.get('product_instance').price,
		payable_amount=kwargs.get('product_instance').price,
	) else False


def add_to_basket(**kwargs):
	"""add_to_basket
	"""
	print("*&*&*&*&*&&*&&",kwargs.get('product_instance').product_category.last().category_name)
	basket_instance = Basket.objects.filter(owner=kwargs.get('customer_instance'))
	print("basket instanceeeeeeeeeeeeeee",basket_instance)
	if basket_instance.exists():
		basket_product_instance = BasketProductLine.objects.filter(
			basket_id=basket_instance.last().id)
		print("basket product instance", basket_product_instance)
		print('**********************************')
		print(kwargs.get('product_instance').id)
		if basket_product_instance.filter(product_id=kwargs.get('product_instance').id).exists():
			basket_product_quantity = basket_product_instance.last().quantity + 1
			print("basket_product_quantity", basket_product_quantity)
			if basket_product_instance.update(
				quantity=basket_product_quantity):
				return True
			return False
		else:
			product_line_instance = create_basket_query(basket_instance, kwargs)
			print("product_line_instance", product_line_instance)
			if product_line_instance:
				return True
			return False
	else:
		print("%%%%%%%%%%%%%%%%%%%%")
		print(kwargs.get('customer_instance'))
		create_basket = Basket.objects.create(owner_id=kwargs.get('customer_instance'))
		print("create_basket", create_basket)
		if create_basket:
			product_line_instance = create_basket_query(basket_instance, kwargs)
			if product_line_instance:
				return True
			return False			


def display_basket_products(**kwargs):
	"""
	display_basket_products
	"""
	basket_instance = Basket.objects.filter(owner=kwargs.get('customer_instance'))
	print("rarararrarara",basket_instance)
	if basket_instance:
		basket_products = BasketProductLine.objects.filter(basket=basket_instance.last())
		return basket_products

	return []	


