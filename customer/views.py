
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from grenades_services.decorators import iamdecorator
from django.contrib.auth.decorators import login_required

# Create your views here.

# import helper models
from helper.messages import MSG

# import customer modules
from grenades_services.modules.otp_management import OTPAuthentication
from grenades_services.modules.customer_modules import RegistrationLogin

# import configuration data
from grenades_services.all_configuration_data import get_auth_user
from grenades_services.all_configuration_data import get_customer_profile_instance


@method_decorator(iamdecorator, name='dispatch')
class SignUpView(TemplateView):
    """
    SignUpView
    path: /customer/registration/
    return: home-screen-redirect
    """
    template_name = 'registration.html'

    def get(self, request):
        """get
        This GET method used to get the home screen page
        """
        return render(request, self.template_name, {})

    def post(self, request):
        """post
        This POST method used to post the sign up registration forms
        """
        if request.POST['password'] != request.POST['confirm_password']:
            messages.success(request, MSG['PASSWORD_NOT_MATCH'])
            return redirect('/customer/registration/')

        registration_instance = RegistrationLogin(request.POST, 'web')
        registration_status_data = registration_instance.registration_new_customer()

        if not registration_status_data['status']:
            return render(request, self.template_name, {
                'message': registration_status_data['message']})

        # redirect login home page
        # django session use for authentication on otp verification time
        # so we can use this session password
        request.session['session_password'] = request.POST['confirm_password']
        return redirect(''.join(['/customer/otp-verification/', str(
            registration_status_data[
                'data'
            ]['auth_user'])]))


@method_decorator(csrf_exempt, name='dispatch')
class OtpVerificationView(TemplateView):
    """
    OtpVerificationView
    path: /customer/otp-verification/<int:id>
    """
    template_name = 'otp_verification.html'

    def get(self, request, auth_user_id):
        """get
        This GET method used to get the home screen page
        """
        auth_user_instance = get_auth_user({'id': auth_user_id})
        if auth_user_instance:
            return render(request, self.template_name, {'auth_user_id': auth_user_id})
        return redirect('/')

    def post(self, request, auth_user_id):
        """post
        This POST method used to post the otp to verification 
        the customer is valid or not at our system
        """
        auth_user_instance = get_auth_user({'id': auth_user_id})
        if not auth_user_instance:
            return redirect('/')
        customer_profile_instance = get_customer_profile_instance(
            {'auth_user': auth_user_instance})
        otp_instance = OTPAuthentication(
            request=request,
            auth_user=auth_user_instance,
            customer_id=customer_profile_instance.id,
            session_password=request.session.get('session_password', None),
            otp=''.join([request.POST['digit-1'],
                         request.POST['digit-2'],
                         request.POST['digit-3'],
                         request.POST['digit-4'],
                         request.POST['digit-5'],
                         request.POST['digit-6']])
        )
        _status, _message, _data = otp_instance.otp_verification()
        if _status:
            return redirect('/')
        messages.success(request, _message)
        return redirect(
            ''.join(
                [
                    '/customer/otp-verification/',
                    str(auth_user_id)
                ]
            )
        )


class ResendOtpView(TemplateView):
    """
    ResendOtpView
    path: /customer/resend-otp/<int:id>
    """
    template_name = 'otp_verification.html'

    def get(self, request, auth_user_id):
        """get
        This GET method used to get the home screen page
        """
        auth_user_instance = get_auth_user({'id': auth_user_id})
        if not auth_user_instance:
            messages.success(request, MSG['auth_user_not_found'])
            return redirect('/')
        customer_profile_instance = get_customer_profile_instance(
            {'auth_user': auth_user_instance})
        if not customer_profile_instance:
            messages.success(request, MSG['customer_not_defined'])
            return redirect('/')
        otp_instance = OTPAuthentication(
            customer_id=customer_profile_instance.id)
        otp_instance.otp_generation()
        return redirect(
            ''.join(
                [
                    '/customer/otp-verification/',
                    str(auth_user_id)
                ]
            )
        )


@method_decorator(iamdecorator, name='dispatch')
class LoginView(TemplateView):
    """
    LoginView
    path: /customer/login/
    """
    template_name = 'login.html'

    def get(self, request):
        """get
        This GET method used to get the home screen page
        """
        return render(request, self.template_name, {})

    def post(self, request):
        """get
        This GET method used to get the home screen page
        """
        login_instance = RegistrationLogin(request.POST, 'web', request)
        login_status_data = login_instance.login_customer_web()
        if not login_status_data['status']:
            return render(
                request,
                self.template_name,
                {'login_status': login_status_data['status']})

        # redirect login home page
        return redirect('/')


@method_decorator(login_required, name='dispatch')
class CustomerLogoutView(TemplateView):
    """
    CustomerLogoutView
    path: /customer/logout/
    """

    def get(self, request):
        """
        This get methoda call the logout function to clear django auth session
        """
        logout(request)
        return redirect('/customer/login/')
