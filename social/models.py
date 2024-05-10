from django.db import models

from utilities.models.base_model import BaseModel
from telegram_app.models import TelegramBot
# Create your models here.


class Lead(BaseModel):
    telegram_bot = models.ForeignKey(
        TelegramBot, null=True, blank=True, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    chat_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    lead_number = models.BigIntegerField(null=True, blank=True, db_index=True)
