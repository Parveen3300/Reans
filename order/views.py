from django.shortcuts import render, redirect

from order.models import Order
from customer.models import CustomerProfile
from customer.models import CustomerAddress
from basket.models import Basket, BasketProductLine
from grenades_services.modules.mailer import Mailer
from helper.messages import TEMPLATE_MESSAGE

from _thread import start_new_thread

from datetime import datetime

# Create your views here.


def Thanks(request):
    return render(request, 'thankyou.html')


def order_mailer_trigger(_order_instance):
    """
    created by @ravi singh
    11 december 2021
    This "order_mailer_trigger" function used to trigger the mial for a customer
    _order_instance: order model's instance
    return: None
    """
    mailer_obj = Mailer(
        email_id=str(
            _order_instance.customer.email) if _order_instance.customer.email else None,
        customer_name=str(
            _order_instance.customer) if _order_instance.customer else '-',
        order_id=str(_order_instance.order_number),
        order_placed_at=str(datetime.now().date()),
        subject='Order generation',
        mailer_template_name='order.html',
        service_name='__ORDER__'
    )
    mailer_status = mailer_obj()
    print(mailer_status)


def CreateOrder(request):
    """
    6 DEC 2021
    @ravi Singh
    for send mail use threading 
    this  create order method is used for to create a order of customer
    """
    if request.user.id:
        try:
            customer_id = CustomerProfile.objects.get(
                auth_user=request.user.id)
        except CustomerProfile.DoesNotExist:
            print('customer_id')
            customer_id = None
        print("***********", customer_id)
        if customer_id:
            address_instance = CustomerAddress.objects.filter(
                customer_id=customer_id).last()
            if address_instance.is_same:
                shipping_instance = address_instance
            else:
                shipping_instance = None
            basket_instance = Basket.objects.filter(
                owner=request.user.customer_profile_auth_user.id).last()
            print("basket -------instance", basket_instance.owner)
            basket_product_line = BasketProductLine.objects.filter(
                basket=basket_instance)
            print("basket product line", basket_product_line)
            if basket_product_line:
                subtotal_price = 0
                for product in basket_product_line:
                    print("*****", product.product.product_name)
                    subtotal_price = subtotal_price + product.product.price
                    print("fdsghjk", subtotal_price)
            else:
                return redirect('/')

            print("________________", basket_product_line)
            print("subvtotal---------------------", subtotal_price)
            print("*************************************************")
            last_order_number = Order.objects.filter().values().last()
            print(last_order_number)

            order_instance = Order.objects.create(customer=customer_id,
                                                  billing_address=address_instance,
                                                  shipping_address=shipping_instance,
                                                  total_incl_tax=subtotal_price,
                                                  total_excl_tax=subtotal_price,
                                                  basket=basket_instance,
                                                  )

            order_number = str("REA00000") + str(order_instance.id)
            order_instance.order_number = order_number
            order_instance.save()
            if order_instance:
                try:
                    basket_product_line.delete()
                except Exception as exception_error:
                    print(exception_error)

                try:
                    start_new_thread(order_mailer_trigger, (order_instance,))
                except Exception as e:
                    print('G256')
                    print(e)

                return render(request, 'thankyou.html')
            return redirect("/")
        return redirect("/")
