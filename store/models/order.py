
from typing import Iterable
from django.db import models

from social.models import Lead

from .product import Product, Variant

from .shop import Shop, ShopShipmentMethod, ShopPaymentMethod, ShopTable
from utilities.models.base_model import BaseModel
from django_lifecycle import hook, BEFORE_CREATE, BEFORE_UPDATE
from django_lifecycle.mixins import LifecycleModelMixin

from .choices import CurrencyChoices, OrderStatusChoices


class Order(LifecycleModelMixin, BaseModel):

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=255, choices=OrderStatusChoices.choices, default=OrderStatusChoices.UNPAID)

    order_number = models.IntegerField()
    total_amount = models.FloatField(default=0.0)
    currency = models.CharField(
        choices=CurrencyChoices.choices, default=CurrencyChoices.IRT)
    is_paid = models.BooleanField(default=False)

    paid_at = models.DateTimeField(null=True, blank=True)

    payment_information = models.JSONField(null=True, blank=True)

    shipment_cost_currency = models.CharField(
        choices=CurrencyChoices.choices, default=CurrencyChoices.IRT)
    shipment_cost_amount = models.FloatField(default=False)

    payment_image = models.CharField(null=True, blank=True)

    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="orders")

    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")

    shipment_method_id = models.ForeignKey(
        ShopShipmentMethod, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")

    table_id = models.ForeignKey(
        ShopTable, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")

    shop_payment_method_id = models.ForeignKey(
        ShopPaymentMethod, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")

    @hook(BEFORE_CREATE)
    def generate_order_number(self):
        self.order_number = 1
        if last_order := Order.objects.filter(shop=self.shop).first():
            self.order_number = last_order.order_number + 1


class OrderItem(LifecycleModelMixin, models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL, related_name="order_items")
    variant = models.ForeignKey(
        Variant, null=True, blank=True, on_delete=models.SET_NULL, related_name="order_items")

    variant_title = models.CharField(max_length=255, null=True, blank=True)
    product_title = models.CharField(max_length=255, null=True, blank=True)

    count = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)
    currency = models.CharField(
        choices=CurrencyChoices.choices, default=CurrencyChoices.IRT)

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:

        return super().save(force_insert, force_update, using, update_fields)

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE)
    def generate_product_title(self):
        if not self.product_title and self.product:
            self.product_title = self.product.title

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE)
    def generate_variant_title(self):
        if not self.variant_title and self.variant:
            self.variant_title = self.variant.title

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE)
    def generate_product_price(self):
        if not self.price:
            if self.variant:
                self.price = self.variant.price
                self.currency = self.variant.currency
            elif self.product:
                self.price = self.variant.price
                self.currency = self.variant.currency
