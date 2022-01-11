

from django.contrib.auth.models import User
from customer.models import CustomerProfile
from configuration.models import CurrencyMaster


def get_auth_user(filter_query_data):
    """
    get_auth_user
    This 'get_auth_user' method used to get auth user instance
    """
    try:
        return User.objects.get(**filter_query_data)
    except Exception as e:
        print('##G11-16')
        print(e)
        return None


def get_customer_profile_instance(filter_query_data):
    """
    get_customer_profile_instance
    This 'get_customer_profile_instance' method used get the customer profile instance
    """
    try:
        return CustomerProfile.objects.get(**filter_query_data)
    except Exception as e:
        print('##G11-29')
        print(e)
        return None


def get_currency_instance(filter_query_data=None):
    """
    This 'get_currency_instance' method used to get the currency data
    """
    try:
        return (CurrencyMaster.objects.get(**filter_query_data).symbol
                if filter_query_data else CurrencyMaster.objects.get(currency='Rupees').symbol)

    except Exception as e:
        print('##G11-42')
        print(e)
        return 'INR'


def get_customer_instance_from_request_user(auth_request_user):
    """
    This 'get_customer_instance_from_request_user' function used to get the customer 
    auth user instance from request user
    return: auth_user_instance
    """
    try:
        if auth_request_user:
            return get_customer_profile_instance({'auth_user': auth_request_user})
    except Exception as e:
        print('##G11-57')
        print(e)
        return None


def product_price_calculator(product_details,
                             coupon_details={},
                             offer_details={}):
    """
    This 'product_price_calculator' method used to manage and calculate the all types 
    of products calculation with sub-total, coupon and offer details
    product_details:dict(), coupon_details:dict(), offer_details:dict()
    return price calculation details
    """
    pass
