from django.contrib import admin

from account.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number')


admin.site.register(User, CustomUserAdmin)
