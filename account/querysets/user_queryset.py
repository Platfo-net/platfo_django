from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def existing(self, phone_number, phone_country_code):
        return self.filter(
            phone_number=phone_number,
            phone_country_code=phone_country_code,
        )

    def is_active(self):
        return self.filter(is_active=True)
