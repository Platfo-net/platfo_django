from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, \
    TabularInlineJalaliMixin

from utilities.admin.custom_actions import CustomActionsMixin
from utilities.admin.mixins import LargeQuerysetMixin, LongIntegerMixin, LinkMixin


class CommonModelAdmin(LargeQuerysetMixin, LongIntegerMixin, CustomActionsMixin, LinkMixin,
                       ModelAdminJalaliMixin, admin.ModelAdmin):
    pass


class CommonTabularInline(LongIntegerMixin, CustomActionsMixin, LinkMixin,
                          TabularInlineJalaliMixin, admin.TabularInline):
    pass


class CommonStackedInline(LongIntegerMixin, CustomActionsMixin, LinkMixin,
                          StackedInlineJalaliMixin, admin.StackedInline):
    pass
