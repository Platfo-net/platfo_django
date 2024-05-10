from django.db import models

from utilities.models.base_model import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class TelegramBot(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bot_token = models.CharField(max_length=255)
    bot_id = models.BigIntegerField(db_index=True)

    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    welcome_message = models.TextField(null=True, blank=True)
    button_name = models.CharField(max_length=255, null=True, blank=True)
    app_link = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.username} : {self.bot_id}"
