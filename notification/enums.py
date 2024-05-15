from django.db import models


class SMSNotificationSender(models.TextChoices):
    USER_ACTIVATION = 'user-activation-api'
    RESET_PASSWORD = 'reset-password-api'
    OTHERS = 'others'
