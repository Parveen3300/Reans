
from django.db import models

# import the helpful module for using notification

from configuration.models import Language

# import abstract modules
from helper.models import AbstractCreatedByUpdatedBy
from helper.models import AbstractDate
from helper.models import AbstractStatus

# import customer modules
from customer.models import CustomerProfile


NOTIFICATION_CATEGORY_CHOICES = [('PUSH', 'PUSH'), ('SMS', 'SMS'), ('EMAIL', 'EMAIL')]
NOTIFICATION_FOR_CHOICES = [('customer', 'Customer'), ('both', 'Both'), ('admin', 'Admin')]
DEVICE_TYPE = [('ios', 'IOS'), ('android', 'ANDROID'), ('web', 'WEB')]


# Create your models here.

class NotificationConfiguration(AbstractCreatedByUpdatedBy, AbstractDate, AbstractStatus):
    """
    NotificationConfiguration
    this model manage all
    notification configuration types
    """
    # Notification main types.
    notification_main_type = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=100, 
                                         verbose_name='Notification Type')

    language = models.ForeignKey(Language, 
                                 on_delete=models.CASCADE, 
                                 null=True, blank=True)

    # Notification sample content use for trigger notification.
    sample_content = models.TextField(verbose_name='Sample Content')
    notification_category = models.CharField(
        choices=NOTIFICATION_CATEGORY_CHOICES, 
        max_length=20,
        verbose_name='Notification Category',
        null=True, blank=True
    )
    notification_for = models.CharField(max_length=50,
                                        choices=NOTIFICATION_FOR_CHOICES, 
                                        verbose_name='Notification For')
    description = models.CharField(
        max_length=200, 
        null=True, blank=True, 
        verbose_name='Description'
    )

    class Meta:
        verbose_name = ' Notification Configuration'
        verbose_name_plural = ' Notification Configuration'
        db_table = 'notification_configuration'

    def __str__(self):
        return str(self.notification_type)


class NotificationRecord(AbstractCreatedByUpdatedBy, AbstractDate, AbstractStatus):
    """
    NotificationRecord
    all types of users
    notification history
    """
    notification_category = models.CharField(
        choices=NOTIFICATION_CATEGORY_CHOICES,
        max_length=20,
        verbose_name='Notification Category'
    )
    notification_type = models.ForeignKey(
        NotificationConfiguration, 
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='Notification Type'
    )
    customer = models.ForeignKey(
        CustomerProfile, on_delete=models.CASCADE, 
        null=True, blank=True, verbose_name='Customer')
    notification_to = models.CharField(choices=NOTIFICATION_FOR_CHOICES, 
                                       max_length=50)
    is_event_done = models.CharField(max_length=50, default="0")
    reason_for_failed = models.TextField(
        verbose_name='Reason For Non Delivery',
        null=True, blank=True)
    message_body = models.TextField(verbose_name='Notification Content')
    device_type = models.CharField(
        max_length=20,
        choices=DEVICE_TYPE, null=True, blank=True,
        verbose_name='Device Type')
    is_read = models.BooleanField(default=False)
    notify_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Notification Date & Time')

    class Meta:
        verbose_name = 'Notification History'
        verbose_name_plural = 'Notification History'
        db_table = 'notification_record'

    def __str__(self):
        return str(self.notification_type)


class NotificationFirebaseToken(AbstractStatus):
    """
    NotificationFirebaseToken
    store all types of user
    notification firebase token
    """
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    device_token = models.TextField(verbose_name='Fire base Token')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    device_type = models.CharField(choices=DEVICE_TYPE,
                                   max_length=30,
                                   verbose_name="Device Type")

    class Meta:
        verbose_name = 'Notification Firebase'
        verbose_name_plural = 'Notification Firebase'

    def __str__(self):
        return self.device_token