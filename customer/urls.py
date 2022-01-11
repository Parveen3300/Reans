from django.urls import path

from customer.views import SignUpView
from customer.views import LoginView
from customer.views import OtpVerificationView
from customer.views import ResendOtpView
from customer.views import CustomerLogoutView


urlpatterns = [

    path('registration/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='sign_up'),
    path('otp-verification/<int:auth_user_id>', 
         OtpVerificationView.as_view(), 
         name='otp_verify'),
    path('resend-otp/<int:auth_user_id>', ResendOtpView.as_view(),  name='resend_otp'),
    path('logout/', CustomerLogoutView.as_view(),  name='logout'),
    
    

]