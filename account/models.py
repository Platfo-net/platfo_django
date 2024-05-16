import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_lifecycle import hook, BEFORE_CREATE
from django_lifecycle.mixins import LifecycleModelMixin

from account.querysets.user_queryset import CustomUserManager
from account.utils import normalize_phone_number
from utilities.models.base_model import BaseModel
from utilities.models.phone_field import PhoneField
from utilities.sms import sms_sender
from utilities.sms.sms_sender import SmsReceiver


class User(LifecycleModelMixin, AbstractUser, BaseModel, SmsReceiver):
    """
    Custom User Model with additional fields
    """
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneField(max_length=13, unique=True, null=True, blank=True, db_index=True)
    phone_country_code = models.CharField(max_length=5, null=True, blank=True)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    telegram_admin_bot_chat_id = models.BigIntegerField(null=True, db_index=True)
    can_approve_payment = models.BooleanField(default=False)

    objects = CustomUserManager()

    class Meta:
        unique_together = ('phone_country_code', 'phone_number')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def receive_sms(self, template_id=None, template_name=None, plain_text=None):
        sms_sender.send(f'+{self.phone_country_code}{normalize_phone_number(self.phone_number)}',
                        template_id=template_id, template_name=template_name, plain_text=plain_text)

    @hook(BEFORE_CREATE)
    def generate_username(self):
        if not self.username:
            self.username = f"{self.first_name}_{self.last_name}"
