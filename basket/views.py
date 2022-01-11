from django.shortcuts import render
from django.shortcuts import redirect


from django.views.generic import TemplateView

# Create your views here.

# import basket models
from basket.models import Basket
from basket.models import BasketProductLine

# import basket modules
from grenades_services.modules.basket import DisplayProductsBasket
from grenades_services.modules.basket import UpdateProductsBasket

from catalogue.models import Product

from grenades_services.wow.customer import get_customer_instance
from grenades_services.wow.products import get_related_products
from grenades_services.wow.products import get_product_instance

from grenades_services.wow.basket import add_to_basket
from grenades_services.wow.basket import display_basket_products


class BaketView(TemplateView):
    """
    BaketView
    Basket this is display the basket baset is empty or not
    https://www.youtube.com/watch?v=HGXHkhzIH64
    path: /basket/
    {'products_description': {'id': 14, 'products_list': [], 'line_reference': '2', 
    'quantity': 1, 'price_currency': 'INR', 'price_excl_tax': None, 'price_incl_tax': None,
    'payable_amount': '1000.00', 'date_created': '2021-11-01T10:29:50.091484Z',
    'date_updated': '2021-11-01T10:29:50.091502Z',
    'basket': 5, 'product': 2, 'category': 5, 'collection': None},
    'product_price_details': {'total_item': 0}, 'random_products_list': <QuerySet [<Product: Winter clothes>]>}
    {'id': 14, 'products_list': [], 'line_reference': '2', 'quantity': 1, 'price_currency': 'INR', 'price_excl_tax': None,
    'price_incl_tax': None, 'payable_amount': '1000.00', 'date_created': '2021-11-01T10:29:50.091484Z',
    'date_updated': '2021-11-01T10:29:50.091502Z', 'basket': 5, 'product': 2, 'category': 5, 'collection': None}
    """
    template_name = 'basket.html'

    def get(self, request):
        """
        This method used to get the all basket elements from basket with user 
        if user is login in this system
        """
        print('___START')
        display_basket_instance = DisplayProductsBasket(request=request)
        try:
            basket_product_details = display_basket_instance.display_products()
            print("*****************************",
                  display_basket_instance.collect_basket_details())
        except Exception as e:
            print('DisplayProductException')
            print(e)
            basket_product_details = None
        related_product = Product.objects.all()
        # Basket count

        print(related_product)
        print('--basket_product_details--')
        print(basket_product_details)
        if not basket_product_details:
            return render(request, self.template_name, {})
        basket_product_description = DisplayProductsBasket.basket_product_description()
        print(basket)
        print('## ### ### ### ### ### ### ### ### ### ##')
        print(basket_product_details)
        print("this is product description",
              basket_product_details['products_description'])
        print("{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{",
              basket_product_details['product_price_details'])
        print("this is random product list",
              basket_product_details['random_products_list'])
        return render(
            request,
            self.template_name,
            {
                'products_description': basket_product_details['products_description'],
                'product_price_details': basket_product_details['product_price_details'],
                'random_products_list': basket_product_details['random_products_list'],
                'related_product': related_product,
            }
        )


class ProductAddBasket(TemplateView):
    """
    ADDToBasket
    """

    def get(self, request, product_alias_name):
        """get
        This get method used to help to add to basket product with 
        the product specification
        """
        basket_input_data = {
            'request': request,
            'product_alias_name': product_alias_name
        }
        basket_instance = UpdateProductsBasket(**basket_input_data)
        basket = Basket.objects.get(
            id=request.user.customer_profile_auth_user.id)

        print("this is basket instance", basket_instance)
        if basket_instance.add_to_basket():
            basket_count = BasketProductLine.objects.filter(
                id=basket.id).count()
            print("1234567890-98765434567890", basket_count)
            # return redirect('/basket/')
            return redirect('/')


# class BuyProducts(TemplateView):
#     """
#     BuyProducts
#     path: basket/buy-now/{{product_desc.product_alias_name}}/
#     """
#     def get(self, request, product_alias_name):
#         """get
#         This get method used to help to add to basket product with
#         the product specification
#         """
#         basket_instance = UpdateProductsBasket(
#             request=request,
#             product_alias_name=product_alias_name)
#         return (redirect('/basket/')
#                 if basket_instance.add_to_basket() else
#                 redirect('/basket/'))


class BuyProductsBac(TemplateView):
    """
    BuyProducts
    path: basket/buy-now/{{product_desc.product_alias_name}}/
    """

    template_name = 'basket.html'

    def get(self, request, product_alias_name):
        """get
        This get method used to help to add to basket product with 
        the product specification
        """
        relate_product = Product.objects.filter(is_active=True)
        buy_product = Product.objects.filter(
            product_alias_name=product_alias_name).last()
        print("098765678", buy_product)
        basket_product_description = DisplayProductsBasket(
            request=request).basket_product_description()
        print("basket description",
              basket_product_description)

        basket_instance = UpdateProductsBasket(
            request=request,
            product_alias_name=product_alias_name)
        return render(
            request,
            self.template_name, {'relate_product': relate_product, 'buy_product': buy_product})


class BuyProducts(TemplateView):
    """
    BuyProducts
    path: basket/buy-now/{{product_desc.product_alias_name}}/
    """

    template_name = 'basket.html'

    def get(self, request, product_alias_name):
        """get
        This get method used to help to add to basket product with 
        the product specification
        """
        try:
            customer_instance = request.user.customer_profile_auth_user.id
            print("^^^^", customer_instance)
        except Exception as e:
            print(e)
            customer_instance = get_customer_instance(request.user)
            print(")))))", customer_instance)
        if not customer_instance:
            return redirect('/')

        product_instance = get_product_instance(
            {
                'product_alias_name': product_alias_name
            }
        )
        print("product_instance", product_instance)
        if not product_instance:
            return redirect('/')
        add_basket_status = add_to_basket(
            customer_instance=customer_instance,
            product_instance=product_instance)
        print("************", add_basket_status)
        if add_basket_status:
            basket_data = display_basket_products(customer_instance=customer_instance,
                                                  product_instance=product_instance)
            print("basket dataaaaaaaaa", basket_data.count())
            if basket_data:
                subtotal_price = 0
                for product in basket_data:
                    subtotal_price = subtotal_price + product.product.price

            basket_count = basket_data.count()
            print(subtotal_price)

        else:
            basket_data = []
        return render(
            request,
            self.template_name,
            {'relate_product': get_related_products(),
             'basket_data': basket_data,
             'basket_count': basket_count,
             'subtotal': subtotal_price}
        )


def remove_basket_product(request, id):
    print("request user", request.user.id)
    basket_instance = Basket.objects.filter(
        owner=request.user.customer_profile_auth_user.id)
    print("rarararrarara", basket_instance)
    if basket_instance:
        basket_products = BasketProductLine.objects.filter(
            basket=basket_instance.last())
        a = basket_products.filter(product_id=id).delete()
        print("++++++++++++++++++++++++++++++++++++++++++++++++", a)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect("/")
