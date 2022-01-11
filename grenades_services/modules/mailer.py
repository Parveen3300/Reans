
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.utils.html import strip_tags


from django.template.loader import render_to_string
from grenades.grenades_settings.development_settings import EMAIL_HOST_USER

from helper.messages import MSG
from helper.messages import get_template_message


class Mailer:
    """
    Mailer
    """

    def __init__(self, **kwargs):
        self.to_email_id = kwargs.get('email_id', None)
        self.cc = "ravikalakoti@loopmethods.com"
        self.email_status = False
        self.notification_category = "EMAIL"
        self.email_subject = kwargs.get('subject', None)
        self.reason_for_failed = 'Error'
        self.customer_name = kwargs.get('customer_name', None)
        # self.mailer_template_name = "mailer/otp.html"
        self.mailer_template_name = kwargs.get(
            'mailer_template_name', 'mailer/otp.html')
        self.template_data = {}
        self.otp = kwargs.get('otp', None)
        self.service_name = kwargs.get('service_name', '__OTP__')
        self.order_id = kwargs.get('order_id', 'PP0000')
        self.total_price = kwargs.get('subtotal_price', '0')
        self.order_placed_at = kwargs.get(
            'order_placed_at', str(datetime.now().date()))
        self.basket_product = kwargs.get('basket_product', None)
        self.data = kwargs.get('data', {})

    def __call__(self):
        return self.email_sender()

    def order_template_data(self):
        """order_template_data
        This 'order_template_data' method used to create order templates data
        add 3 models fields
            order_id
            order_placed_at
            cart_product_queryset
        """
        self.template_data['order_id'] = self.order_id
        self.template_data['order_placed_at'] = self.order_placed_at
        self.template_data['basket_product'] = self.basket_product

    def email_sender(self):
        """
        This "email_sender" used to send the mail for each user as per logic 
        to send the mail all type users
        kwargs: {
            'email_id': 'pycodertest@gmail.com',
            'subject': 'python-test',
            'customer_name': 'Gourav Sharma',
            'otp': '9039',
            'service': 'API',
        }
        return: status=True/False
        """
        try:
            self.template_data['otp'] = self.otp
            self.template_data['message'] = get_template_message(
                self.service_name,
                self.customer_name,
                self.otp,
                self.order_id)
            self.order_template_data()
            self.template_data['data'] = self.data if self.data else {}
            html_content = render_to_string(
                self.mailer_template_name, self.template_data)
            text_content = strip_tags(html_content)
            print(text_content)
            msg = EmailMultiAlternatives(self.email_subject,
                                         text_content,
                                         EMAIL_HOST_USER,
                                         [self.to_email_id, self.cc],
                                         cc=[])
            msg.attach_alternative(html_content, "text/html")
            return True if msg.send() else False
        except Exception as e:
            print("G76")
            print(e)
            self.reason_for_failed = str(e)
            return False
