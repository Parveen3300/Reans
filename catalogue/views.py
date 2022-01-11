from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from grenades_services.modules.home import Home
# Create your views here.
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt

# Helper
from helper.serializers import ProductSerializer


from catalogue.models import Category
from catalogue.models import Product
from catalogue.models import CollectionProductMapping
from catalogue.models import CategoryProductMapping
from catalogue.models import Review
from customer.models import CustomerProfile, CustomerAddress
from location.models import CountryMaster, StateMaster, CityMaster
from basket.models import Basket
import json
from grenades_services.wow.basket import display_basket_products

# mailer
from grenades_services.modules.mailer import Mailer

#razor pay
import razorpay
from grenades.grenades_settings.development_settings import RAZOR_PAY_ID
from grenades.grenades_settings.development_settings import RAZOR_PAY_SECRET_KEY


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(RAZOR_PAY_ID,RAZOR_PAY_SECRET_KEY))


class HomeDashboard(TemplateView):
    """
    HomeDashboard
    """
    template_name = 'index.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_context_data = {
            'category_queryset': [],
            'category_product_queryset': []
        }

    def get(self, request):
        """get
        This GET method used to get the home screen page
        in hom-screen dashboard display all context with cms and catalogue products detail
        calling Home class to get each details of 
        category list and product list with all specification and product details
        return: template_context_data: {
            'category_queryset': [],
            'category_product_queryset': []
        }
        """
        # home class module get the all the home
        # related data using home methods
        home_instance = Home()
        category_queryset = home_instance.simple_category_list()
        category_product_queryset = home_instance.product_category_list()
        deal_day_product = home_instance.deal_day_product()

        # manage the all home related data
        self.template_context_data['category_queryset'] = category_queryset[0:6] \
            if category_queryset else []
        self.template_context_data['category_product_queryset'] = category_product_queryset \
            if category_product_queryset else []
        self.template_context_data['deal_day_product'] = deal_day_product \
            if deal_day_product else []

        # render the final templates
        return render(request, self.template_name, self.template_context_data)


class AllCategoryView(TemplateView):
    """
    HomeDashboard
    """
    template_name = 'category-page.html'

    def get(self, request):
        """get
        This GET method used to get the home screen page
        """
        home_instance = Home()
        category_queryset = home_instance.simple_category_list()
        return render(
            request,
            self.template_name,
            {'category_queryset': category_queryset if category_queryset else []}
        )


class ProductList(TemplateView):
    """
    ProductList
    """
    template_name = 'product_list.html'

    def get(self, request, id):
        """
        This GET method used to get the product list
        """
        home_instance = Home(category_id=id)
        product_list = home_instance.product_list_from_category()
        return render(request, self.template_name, {'product_list': product_list})

    def post(self, request, id):
        """
        create by ravi Singh kalakoti
        18-November-2021
        this post method is used for filter the product by taking input from frontend filter
        """
        home_instance = Home(category_id=id)
        product_list = home_instance.product_list_from_category()
        price = request.POST.get('price')
        print("#####################################", request.POST.get('size'))

        # Size wise filter
        if request.POST.get('size') == 'small':
            product_list = product_list.filter(product_size='Small').all()

        elif request.POST.get('size') == 'medium':
            product_list = product_list.filter(product_size='Medium').all()

        elif request.POST.get('size') == 'large':
            product_list = product_list.filter(product_size='Large').all()

        # color wise filter
        elif request.POST.get('color') == 'green':
            product_list = product_list.filter(product_color='green').all()
        elif request.POST.get('color') == 'red':
            product_list = product_list.filter(product_color='red').all()
        elif request.POST.get('color') == 'black':
            product_list = product_list.filter(product_color='black').all()

        # price wise filter
        elif price == 'low':
            product_list = product_list.all().order_by("price")
        elif price == 'high':
            product_list = product_list.all().order_by("-price")
        elif price == 'newest':
            product_list = product_list.all().order_by("-created_at")
        return render(request, self.template_name, {'product_list': product_list})


class ProductDescription(TemplateView):
    """
    ProductList
    """
    template_name = 'product_description.html'

    def get(self, request, id):
        """
        This GET method used to get the product list
        """
        home_instance = Home(product_get_data={'id': id})
        product_instance = home_instance.get_product_instance()
        try:
            review_list = Review.objects.filter(
                product=product_instance.id, is_active=True).all()

        except Exception as e:
            print("G105", e)
        relate_product = Product.objects.filter(is_active=True)
        return render(
            request,
            self.template_name,
            {'product_desc': product_instance if product_instance else [],
             'review_list': review_list if review_list else [],
             'related_products': relate_product})


class Checkout(TemplateView):
    """
    Checkout
    """
    template_name = "checkout.html"

    def get(self, request):
        """
        this get method used for all details in checkout page
        """
        if request.user.id:
            customer_id = CustomerProfile.objects.get(
                auth_user=request.user.id)
            print("456456", customer_id)
            country_list = CountryMaster.objects.filter(is_active=True)
            city_list = CityMaster.objects.filter(is_active=True)
            state_list = StateMaster.objects.filter(is_active=True)
            customer_address = CustomerAddress.objects.filter(
                customer_id=customer_id).last()
            basket_products = display_basket_products(customer_instance=customer_id)
            if basket_products:
                subtotal_price = 0
                for product in basket_products:
                    subtotal_price = subtotal_price + product.product.price

            basket_count = basket_products.count()
            currency = 'INR'
            
            #razor pay________________________________________________________________>

            try:
                razorpay_order = razorpay_client.order.create(dict(amount=subtotal_price,
                                                       currency=currency,
                                                       payment_capture='0'))
            except Exception as e:
                print('MINIMUM-ONE-RUPEES')
                print('Exception')
                print(e)
                return redirect('/cart/')



            razorpay_order_id = razorpay_order['id']
            print("razor-----------------pay order id",razorpay_order_id)
            callback_url = 'http://127.0.0.1:8000/paymenthandler/'
            print("$%^&*^%^&*(", customer_address)
            return render(request, self.template_name, {'country': country_list,
                                                        'city': city_list,
                                                        'state': state_list,
                                                        'customer_address': customer_address,
                                                        'basket_products':basket_products,
                                                        'total_price':subtotal_price,
                                                        'basket_count':basket_count,
                                                        'razorpay_order_id':razorpay_order_id,
                                                        'razorpay_merchant_key':RAZOR_PAY_ID,
                                                        'razorpay_amount':subtotal_price,
                                                        'currency':currency,
                                                        'callback_url':callback_url})
        else:
            return redirect("/customer/login/")

    def post(self, request):
        """
        this post method used for submit the detail of checkout page
        """
        if request.user.id:
            customer_id = CustomerProfile.objects.get(
                auth_user=request.user.id)

            if customer_id:
                try:
                    billing_address = {
                        "customer": customer_id,
                        "customer_address_type": "billing",
                        "country_id": request.POST['country'],
                        "state_id": request.POST['state'],
                        "city": request.POST['city'],
                        "line1": request.POST['line1'],
                        "postcode": request.POST['postcode']
                    }
                    customer_address_queryset = CustomerAddress.objects.filter(
                        customer_id=customer_id)
                    if customer_address_queryset.exists():
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",
                              customer_address_queryset.exists())
                        customer_address_instance = customer_address_queryset.update(
                            **billing_address)
                        print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
                              customer_address_instance)

                    else:
                        customer_address_instance = CustomerAddress.objects.create(
                            **billing_address)

                    if customer_address_instance:
                        return render(request, self.template_name, {})

                    return redirect("/")

                except Exception as e:
                    print("customer address issue", e)
                    return redirect("/")





@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            print("fghjkohuyghjukiolp;kjuyhgjukiol;", result)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    print("RAVIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII",razorpay_client.payment.capture(payment_id, amount))
                    return render(request, 'thankyou.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

# class ProductSearchViewSet(ModelViewSet):
#     """
#     this method used for product search
#     """
#     serializer_class = ProductSerializer
#     http_method_names = ['get', 'head', 'option']

#     def get_queryset(self):
#         search_term = self.request.query_params.get("searchTerm", None)
#         if search_term:
#             return Product.objects.filter(product_name__icontains=search_term)
#         return Product.objects.none()
