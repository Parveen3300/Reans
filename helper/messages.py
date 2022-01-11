""" All Messages Alerts """

MODEL_MSG = dict(
    ZIPCODEMSG="Zipcode must be entered in the format: '11111'. Up to 5 digits allowed.",
    PHONENOMSG="Phone number must be entered in the format: '9999999999'. Up to 15 digits allowed.",
    EMAIL_EXIST="This Email Id Already Exist in W&R System Please enter other Email Id",
    UNIQUE_PHONE="This Phone Number Already Exist in W&R System Please enter other Phone Number"
)


MSG = dict(
    DONE='DONE',
    VALID_MAIL_ID='Please Enter valid email or mobile number to create new account',
    ALREADY_EXIST_USER='This Email/ Mobile Number is already exist please choose another one',
    DATA_ERROR='DATA_ERROR',
    AUTH_USER_NOT_FOUND='Auth user not found',
    auth_user_not_found='Auth user not found',
    customer_not_defined='Customer Profile not defined',
    OTP_EXPIRED='Otp is expired please resend the otp',
    AUTHENTICATION_FAILED='Authentication Failed',
    MIS_MATCH_OTP='Otp is not match please enter valid otp',
    WARN_USERNAME='Please enter valid email/ mobile number for login user',
    PASSWORD_NOT_MATCH="Please enter valid confirm password"
)


TEMPLATE_MESSAGE = dict(
    OTP='Your verification OTP/Code is : ',
    ORDER='Hi [NAME], your order with [ORDER-ID] created successfully please check and track your order',
    SHIP_ROCKET_WALLET="Hi, order place with [ORDER-ID] but ship-rocket wallet has not afficiant balance please update your wallet"
)


def get_template_message(service_name, customer_name, otp, order_id):
    """
    get_template_message
    """
    if service_name == '__OTP__':
        return TEMPLATE_MESSAGE['OTP']
    if service_name == '__ORDER__':
        return TEMPLATE_MESSAGE['ORDER'] \
            .replace('[NAME]', customer_name) \
            .replace('[ORDER-ID]', order_id)
    if service_name == '__SHIP_ROCKET_WALLET__':
        return TEMPLATE_MESSAGE['SHIP_ROCKET_WALLET'].replace('[ORDER-ID]', order_id)
