"""
RegistrationLoginModule
created 22 Oct 2021 by GouravSharma (^_^)
This RegistrationLoginModule class module used to manage the user registration and login process
"""
# import regex
import re


# import User models
from django.contrib.auth.models import User

# import Customer models
from customer.models import CustomerProfile

# import helper modules
from helper.serializer_error_parser import SerializerErrorParser

# import OTP models
from grenades_services.modules.otp_management import OTPAuthentication
from grenades_services.serializers.customer_serializers import CustomerProfileSerializer
from grenades_services.all_configuration_data import get_auth_user
from grenades_services.modules.auth_authentication_user import Authentication

# import MSG Models
from helper.messages import MSG
from grenades_services.modules.mailer import Mailer

from _thread import start_new_thread


def is_mobile_number_valid(mobile_number_as_username):
    """
    This 'is_mobile_number_valid' method used to return the regex validation re compile modules
    # 1) Begins with 0 or 91
    # 2) Then contains 7 or 8 or 9.
    # 3) Then contains 9 digits
    pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    """
    return re.compile("(0|91)?[7-9][0-9]{9}") \
        .match(mobile_number_as_username)


def otp_mailer_trigger(email_id, customer, otp):
    """
    created by @ravi singh
    11 december 2021
    This "otp_mailer_trigger" function used to trigger the mial for a customer
    otp: 
    return: None
    """
    mailer_obj = Mailer(email_id=str(email_id),
                        customer_name= str(customer),
                        otp = str(otp),
                        subject="otp generation",
                        mailer_template_name='otp.html',
                        service_name="__OTP__")
    mailer_status = mailer_obj()
    print(mailer_status)


class RegistrationLogin:
    """
    'RegistrationLogin'
    """

    def __init__(self, registration_login_data={}, source=None, request=None):
        self.request = request
        self.registration_login_data = registration_login_data
        self.default_isd = '+91'
        self.source = source
        self._username = None
        self.email = None
        self.auth_username_type = None
        self.customer_profile_data = {}
        self.response_dict = {
            'status': False,
            'message': '-',
            'data': {}
        }

    def check_auth_username_params(self):
        """check_auth_username_params
        This 'check_auth_username_params' method used to check the username parameter 
        is a phone number field or a email fields
        """
        return True if is_mobile_number_valid(self._username) else False

    def mail_validation(self):
        """
        mail_validation
        this 'mail_validation' method used to check mail validation, mail string is valid or not
        """
        return False if re.fullmatch(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            self._username) else True

    def already_exist_user(self):
        """
        This 'already_exist_user' method used to check user is already exit or not
        """
        if User.objects.filter(username=self._username).exists():
            return True
        return False

    def create_auth_user(self):
        """
        This 'create_auth_user' method used to create the auth user 
        with a create new user instance
        """
        auth_user_dict = {
            'first_name': self.registration_login_data.get('firstname', None),
            'last_name': self.registration_login_data.get('lastname', None),
            'username': self._username,
            'password': self.registration_login_data.get('password'),
            'email': None if self.auth_username_type == 'mobile_no' else self._username,
            'is_staff': False,
            'is_active': False,
            'is_superuser': False
        }
        return User.objects.create_user(**auth_user_dict)




    def create_customer_profile_with_otp(self, auth_user_instance):
        """
        This 'create_customer_profile_with_otp' methods used to create a new customer profile 
        with otp management system
        """
        customer_profile_data = {
            'auth_user': auth_user_instance.id,
            'registration_type': self.source,
            'customer_full_name': ''.join(
                [
                    self.registration_login_data['firstname'], ' ',
                    self.registration_login_data['lastname']
                ]
            ),
        }
        if self.auth_username_type == 'mobile_no':
            customer_profile_data['mobile'] = self.registration_login_data['username']
            customer_profile_data['mobile_with_isd'] = ''.join(
                [self.default_isd,
                 self.registration_login_data['username']]
            )
            customer_profile_data['isd'] = self.default_isd
        else:
            customer_profile_data['email'] = self.registration_login_data['username']
       
        customer_profile_serializer = CustomerProfileSerializer(
            data=customer_profile_data)

        if customer_profile_serializer.is_valid():
            customer_profile_serializer.save()
            self.customer_profile_data = customer_profile_serializer.data
            otp_instance = OTPAuthentication(
                customer_id=self.customer_profile_data['id'],
                api_service_name='__registration__',
                auth_type=self.auth_username_type)
            otp_status = otp_instance.otp_generation()
            otp = otp_instance.random_otp_number
       
            if otp_status:
                try:
                    start_new_thread(otp_mailer_trigger, (customer_profile_data['email'],customer_profile_data['customer_full_name'],otp))
                except Exception as e:
                    print('G256')
                    print(e)
                # mailer_obj = Mailer(email_id=customer_profile_data['email'],
                #                     customer_name= customer_profile_data['customer_full_name'],
                #                     otp = otp,
                #                     subject="otp generation",
                #                     mailer_template_name='otp.html',
                #                     service_name="__OTP__")
                # mailer_status = mailer_obj()

                # print("############", mailer_status)

                return False
            return True

        # customer profile not create so we have delete the auth user data from
        # auth user table according to valid customer login details
        User.objects.filter(
            username=self.registration_login_data['username']).delete()
        serializer_error_instance = SerializerErrorParser(
            customer_profile_serializer.errors)
        key, value_error = serializer_error_instance()
        print(''.join([key, ': ', value_error]))
        return True

    def registration_new_customer(self):
        """
        registration_new_customer
        This 'registration_new_customer' method used to register the new user in our system 
        with new records
        """
        # :get auth user name type like: username field parameter find
        self._username = self.registration_login_data['username'].strip()
        self.auth_username_type = (
            'mobile_no'
            if self.check_auth_username_params() else
            'email'
        )

        # :email validation and create customer profile
        # with auth user and otp management
        if self.auth_username_type == 'email':
            if self.mail_validation():
                self.response_dict['message'] = MSG['VALID_MAIL_ID']
                return self.response_dict
        if self.already_exist_user():
            self.response_dict['message'] = MSG['ALREADY_EXIST_USER']
            return self.response_dict
        auth_user_instance = self.create_auth_user()
        if auth_user_instance:
            if self.create_customer_profile_with_otp(auth_user_instance):
                self.response_dict['message'] = MSG['DATA_ERROR']
                return self.response_dict

            # last success response
            self.response_dict['status'] = True
            self.response_dict['data'] = self.customer_profile_data
            self.response_dict['message'] = MSG['DONE']
            return self.response_dict

    def login_customer_web(self):
        """
        login_customer_web
        This 'login_customer_web' method used to login the system user 
        with create a login session
        """
        self._username = self.registration_login_data['username'].strip()
        if self.already_exist_user():
            auth_user_instance = get_auth_user(
                {'username': self._username})

            if auth_user_instance:
                # authentication with diffrent user and application type
                _authentication = Authentication(
                    auth_user_instance,
                    self.registration_login_data['password'],
                    self.request)

                if _authentication.web_authentication():
                    self.response_dict['status'] = True
                    self.response_dict['message'] = MSG['DONE']
                    return self.response_dict  # last success response
                else:
                    self.response_dict['message'] = MSG['AUTHENTICATION_FAILED']
                    return self.response_dict  # failed authentication status

        # already exit so warning user
        # please enter valid user name
        self.response_dict['message'] = MSG['WARN_USERNAME']
        return self.response_dict
