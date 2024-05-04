import re

from django.core.exceptions import ValidationError
from django.db.models import CharField


def validate_format(value):
    if not re.match('^09\d{0,9}$', value):
        raise ValidationError('Phone number is not valid.')


class PhoneField(CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.validators.append(validate_format)
