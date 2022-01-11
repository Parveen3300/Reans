from django.db import models

# Create your models here.

# import Customer Models
from customer.models import CustomerProfile



class OTP(models.Model):
    """OTP
    mobile and email otp authentication module
    """
    otp = models.PositiveIntegerField()
    is_verified = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=20, choices=[
        ('phone', 'Phone Number'), ('email', 'Email ID')
        ])
    otp_status = models.CharField(max_length=20,
                                  verbose_name='OTP Status',
                                  choices=[('delivered', 'Delivered'),
                                           ('not_delivered', 'Not Delivered'),
                                           ('successful', 'Successful'),
                                           ('expired', 'Expired')])
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    expired_datetime = models.DateTimeField(verbose_name="Expired At")
    customer = models.ForeignKey(
        CustomerProfile, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = '  OTP Management'
        verbose_name_plural = '  OTP Management'
        db_table = 'otp_management'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.otp)