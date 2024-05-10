from django.contrib import admin
from .models import TelegramBot
# Register your models here.


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    pass
