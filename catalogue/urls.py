from django.urls import path

from catalogue.views import HomeDashboard
from catalogue.views import ProductList
from catalogue.views import ProductDescription
from catalogue.views import AllCategoryView
from catalogue.views import Checkout
from catalogue.views import paymenthandler
# from catalogue.views import ProductSearchViewSet


urlpatterns = [

    path('', HomeDashboard.as_view(), name='home_dashboard'),
    path('product_list/<int:id>', ProductList.as_view(), name='product_list'),
    path('product_description/<int:id>',
         ProductDescription.as_view(), name='product_description'),
    path('category-list/', AllCategoryView.as_view(), name='category-list'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),

    # path("product-search/", ProductSearchViewSet, basename='product-search'),


]
