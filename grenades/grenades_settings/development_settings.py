"""
DevelopmentEnvSettings
created at 10 August 2021 by loop developer's
This settings file manage the all development env setting in this project 
with all secure parameters
"""


from .core_settings import *


# Database Settings using decouple configurations.
DATABASES = {'default': {'ENGINE': config('ENGINE'),
                         'NAME': config('DB_NAME'),
                         'PASSWORD': config('DB_PASSWORD'),
                         'USER': config('DB_USER'),
                         'HOST': config('DB_HOST'),
                         'PORT': config('DB_PORT')}, }



#mailer credential
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "reanscreation@gmail.com" #"loopmethods3@gmail.com"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = "loop@123"      #"loopadmin123"


#razor Pay key
RAZOR_PAY_ID = config('RAZOR_PAY_ID')
RAZOR_PAY_SECRET_KEY = config('RAZOR_PAY_SECRET_KEY')



