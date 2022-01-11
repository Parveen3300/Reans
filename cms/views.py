from django.shortcuts import render, redirect
from django.views.generic import TemplateView
# Create your views here.

from cms.models import TermsConditions
from cms.models import WebsiteCookiesPolicy
from cms.models import WebsitePolicy
from cms.models import ReplacementCancellationPolicy
from cms.models import AboutUs
from cms.models import ContactUs


class About_Us(TemplateView):

    """
    About_Us
    """
    template_name = 'about_us.html'

    def get(self, request):
        """
        this About_Us method used for get the terms dynamic data
        """
        about_us_data = AboutUs.objects.last()

        return render(
            request,
            self.template_name,
            {'about_us_data': about_us_data if about_us_data else []}
        )


class Contact_Us(TemplateView):

    """
    Contact_Us
    """
    template_name = 'contact.html'

    def get(self, request):
        """
        this Contact_Us method used for get the terms dynamic data
        """
        contact_us_data = ContactUs.objects.last()

        return render(
            request,
            self.template_name,
            {'contact_us_data': contact_us_data if contact_us_data else []}
        )

    def post(self, request):
        """
        this post method used for submit the contact detail:
        date 15 nov 2021
        @ravisingh
        """
        if request.method == "POST":
            data = {
                'name': request.POST['name'],
                'email': request.POST['email'],
                'mobile': request.POST['mobile'],
                'message': request.POST['message']
            }

            if data.values():
                ContactUs.objects.create(**data)
            # name = request.POST['name']
            # email = request.POST['email']
            # mobile = request.POST['mobile']
            # message = request.POST['message']
            # ContactUs.objects.create(
            #     name=name, email=email, mobile=mobile, message=message)

            return redirect("/")
        return redirect('/contact-us/')


class TermsAndConditions(TemplateView):

    """
    TermsConditions
    """
    template_name = 'terms_condition.html'

    def get(self, request):
        """
        this TermsConditions method used for get the terms dynamic data
        """
        terms_conditions = TermsConditions.objects.last()

        return render(
            request,
            self.template_name,
            {'terms_conditions': terms_conditions if terms_conditions else []}
        )


class WebCookiePolicy(TemplateView):
    """
    WebCookiePolicy
    """
    template_name = 'cookie_policy.html'

    def get(self, request):
        """
        this WebCookiePolicy method used for get the terms dynamic data
        """
        cookie_policy = WebsiteCookiesPolicy.objects.last()
        return render(
            request,
            self.template_name,
            {'cookie_policy': cookie_policy if cookie_policy else []}
        )


class Support(TemplateView):
    """
    Support
    """
    template_name = 'support.html'

    def get(self, request):
        """
        this Support method used for get the terms dynamic data
        """
        return render(
            request,
            self.template_name, {}
        )


class ReplacementPolicy(TemplateView):
    """
    WebCookiePolicy
    """
    template_name = 'replacement_policy.html'

    def get(self, request):
        """
        this ReplacementPolicy method used for get the terms dynamic data
        """
        return render(request, self.template_name, {})
