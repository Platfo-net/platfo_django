from django import forms
from django.contrib import admin

from .models import Shop,  Category, Product, Attribute
# Register your models here.


class AttributeForm(forms.ModelForm):

    class Meta:
        widgets = {
            'description': forms.Textarea(attrs={
                'cols': 20,
                'rows': 5
            }),
        }


class AttributeInline(admin.TabularInline):
    model = Attribute
    form = AttributeForm
    # can_delete = False
    extra = 0
    fields = ['key', "value"]
    # readonly_fields = ['uid', 'amount', 'price_unit',
    #    'description', 'started', 'ended']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [AttributeInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class ThemeAdmin(admin.ModelAdmin):
    pass
