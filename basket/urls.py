from django.urls import path

from basket.views import BaketView
from basket.views import ProductAddBasket
from basket.views import BuyProducts
from basket.views import remove_basket_product

urlpatterns = [

    path('', BaketView.as_view(), name='baskets'),
    path('add-basket/<str:product_alias_name>', 
    	 ProductAddBasket.as_view(), name='product_add_basket'),
    path('buy-now/<str:product_alias_name>', BuyProducts.as_view(), 
    	 name='buy_now_products'), 
    path('remove-product/<int:id>', remove_basket_product, name="remove_basket_product"),   

]