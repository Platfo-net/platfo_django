from django.db import models
from django.contrib.auth import get_user_model

from store.models.choices import CurrencyChoices
from utilities.models.base_model import BaseModel

User = get_user_model()


class Shop(BaseModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(
        max_length=64, null=True, blank=True)  # TODO Choices to enum

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Theme(models.Model):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="themes")

    color_code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.shop} Theme"


class PaymentMethod(BaseModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)

    information_fields = models.JSONField(null=True, blank=True)
    payment_fields = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class ShopPaymentMethod(BaseModel):
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="shop_payment_methods")
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE, related_name="shop_payment_methods")

    information = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=False)


class ShopShipmentMethod(BaseModel):
    title = models.CharField(max_length=255)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="shipment_methods")

    is_active = models.BooleanField(default=False)

    price = models.FloatField(default=0.0)
    currency = models.CharField(
        choices=CurrencyChoices.choices, default=CurrencyChoices.IRT)


class ShopTable(BaseModel):
    title = models.CharField(max_length=255)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="tables")
