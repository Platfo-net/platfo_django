import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_lifecycle import hook, BEFORE_CREATE
from django_lifecycle.mixins import LifecycleModelMixin

from account.querysets.user_queryset import CustomUserManager
from utilities.models.base_model import BaseModel
from utilities.models.phone_field import PhoneField


class User(LifecycleModelMixin, AbstractUser, BaseModel):
    """
    Custom User Model with additional fields
    """
    uuid = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    username = models.CharField(
        max_length=255, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneField(
        max_length=13, unique=True, null=True, blank=True, db_index=True)
    phone_country_code = models.CharField(max_length=5, null=True)
    profile_image = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    telegram_admin_bot_chat_id = models.BigIntegerField(
        null=True, db_index=True)
    can_approve_payment = models.BooleanField(default=False)

    objects = CustomUserManager()

    class Meta:
        unique_together = ('phone_country_code', 'phone_number')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @hook(BEFORE_CREATE)
    def generate_username(self):
        if not self.username:
            self.username = f"{self.first_name}_{self.last_name}"

    @hook(BEFORE_CREATE)
    def set_is_active(self):
        if self.is_superuser:
            self.is_active = True
