"""
OTPFactorAuthentication
This OTP Authentication module used to generate and verified the otp 
validation using OTP validation class
created at 2021-OCt-22 by Gourav Sharma(^_^)
"""
import random
from datetime import datetime
from datetime import timedelta

# import User models
from django.contrib.auth.models import User

from two_factor_authentication.models import OTP
from helper.messages import MSG

from grenades_services.modules.auth_authentication_user import Authentication
from grenades_services.modules.mailer import Mailer


class OTPAuthentication:
    """
    OTPAuthentication
    This OTPAuthentication class module used to generate and authenticate (verification)
    the otp for checking the user is valid or not in our system
    """

    def __init__(self, **kwargs):

        self.request = kwargs.get('request')
        self.customer_id = kwargs.get('customer_id', None)
        self.auth_user = kwargs.get('auth_user', None)
        self.api_service_name = kwargs.get('api_service_name', '__OTP__')
        self.source = kwargs.get('source', 'WEB')
        self.session_password = kwargs.get('session_password')
        self.auth_type = kwargs.get('auth_type', 'email')

        self.sms_otp_expiry = timedelta(minutes=120)
        self.random_otp_number = '8392'
        self.current_date_time = datetime.now()
        self.otp = kwargs.get('otp', None)

    def get_the_otp(self):
        """get_the_otp
        this get_the_otp() methods used to generate the 6 digits random number
        for customer otp
        """
        self.random_otp_number = random.randint(100000, 999999)

    def otp_sent(self):
        """
        This otp_sent() method used to sent otp to mail or sms for customer
        """
        self.get_the_otp()
        try:
            mailer_obj = Mailer(
                email_id=self.auth_user.email if self.auth_user.email else None,
                otp=str(self.random_otp_number),
                customer_name=(
                    self.auth_user.first_name
                    if self.auth_user.email else
                    self.auth_user.phone_number),
                subject='otp generation',
                mailer_template_name='otp.html',
                service_name='__OTP__'
            )
            mailer_status = mailer_obj()
            print("maikler stautssssssssssssssssss", mailer_status)
            return 'delivered' if mailer_status else 'not_delivered'
        except Exception as e:
            print('G93')
            print(e)
            return 'not_delivered'

    def otp_generation(self):
        """
        otp_generation
        """
        otp_sent_status = self.otp_sent()
        print(" otp sentttttttttttttttttttt status", otp_sent_status)
        create_customer_otp = OTP.objects.create(otp=self.random_otp_number,
                                                 otp_status=otp_sent_status,
                                                 is_verified=False,
                                                 auth_type=self.auth_type,
                                                 expired_datetime=datetime.now() + self.sms_otp_expiry,
                                                 customer_id=self.customer_id)
        if not create_customer_otp:
            return False
        return True

    def otp_verification(self):
        """
        otp_verification
        """
        two_factor_instance = OTP.objects.filter(
            created_at__lte=self.current_date_time,
            expired_datetime__gte=self.current_date_time,
            customer_id=self.customer_id).first()
        if not two_factor_instance:
            return False, MSG['OTP_EXPIRED'], {}

        if int(two_factor_instance.otp) == int(self.otp):
            two_factor_instance.is_verified = True
            two_factor_instance.save()
            User.objects.filter(id=self.auth_user.id).update(is_active=True)

            # authentication with diffrent user and application type
            _authentication = Authentication(
                self.auth_user,
                self.session_password,
                self.request)
            if self.source == 'WEB':
                if _authentication.web_authentication():
                    print('AuthenticationPassed')
                    return True, MSG['DONE'], {}
                return False, MSG['AUTHENTICATION_FAILED'], {}
            else:
                if _authentication.api_authentication():
                    print('APIAuthenticationPassed')
                    return True, MSG['DONE'], {}
                return False, MSG['AUTHENTICATION_FAILED'], {}

        # otp mismatach
        return False, MSG['MIS_MATCH_OTP'], {}
