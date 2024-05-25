import random
import string

from rest_framework.exceptions import ValidationError


def generate_random_token(length: int) -> str:
    return ''.join(
        random.choice(f'{string.ascii_letters}0123456789') for _ in range(length)
    )


def generate_random_code(length: int) -> int:
    return random.randint(10 ** length, (10 ** (length + 1)) - 1)


def normalize_phone_number(phone_number):
    if phone_number[0] == '0':
        phone_number = phone_number[1:]
    return phone_number


def validate_code_and_token(cached_data, validated_data):
    code = cached_data.get('code', None)
    token = cached_data.get('token', None)
    if not code and token:
        raise ValidationError('Invalid code or token')
    if not token == validated_data['token'] or not code == validated_data['code']:
        raise ValidationError('Invalid code or token')
