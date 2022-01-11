from django.urls import path
from order.views import *


urlpatterns = [


    path('create_order/', CreateOrder, name ="create_order"),
 
    

]