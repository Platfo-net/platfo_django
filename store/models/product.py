
from django.db import models

from .shop import Shop
from utilities.models.base_model import BaseModel

from .choices import CurrencyChoices


class Category(BaseModel):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True, blank=True)

    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="categories")
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Product(BaseModel):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(default=0.0)
    currency = models.CharField(
        choices=CurrencyChoices.choices, default=CurrencyChoices.IRT)

    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL,  related_name="products")

    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Attribute(models.Model):
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=255)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes")

    def __str__(self) -> str:
        return self.title


class Variant(BaseModel):
    title = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants")

    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)


    price = models.FloatField(default=0.0)
    currency = models.CharField(
        choices=CurrencyChoices.choices, default=CurrencyChoices.IRT)

    def __str__(self) -> str:
        return self.title
