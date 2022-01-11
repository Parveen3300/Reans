
from customer.models import CustomerProfile


def get_customer_instance(auth_user_instance):
	"""get_customer_instance
	"""
	try:
		return CustomerProfile.objects.get(auth_user=auth_user_instance)
	except Exception as e:
		return None