from django.urls import path

from cms.views import TermsAndConditions
from cms.views import WebCookiePolicy
from cms.views import About_Us
from cms.views import Contact_Us
from cms.views import Support
from cms.views import ReplacementPolicy



urlpatterns = [

    path('terms-conditions/', TermsAndConditions.as_view(), name='terms-conditions'),
    path('cookie-policy/', WebCookiePolicy.as_view(), name = "cookie-policy"),
    path('about-us/', About_Us.as_view(), name = "about-us"),
    path('contact-us/', Contact_Us.as_view(), name = "contact-us"),
    path('support/', Support.as_view(), name = "support"),
    path('replacement-policy/', ReplacementPolicy.as_view(), name="replacement-policy"),

]