import random
import string

from django.core.cache import cache


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


def get_user_reset_password_code(phone_number, phone_country_code):
    key = f'{phone_country_code}{phone_number}'
    data = cache.get(key)
    return data


def set_user_reset_password_code(phone_number, phone_country_code, code, token):
    data = {'code': code, 'token': token}
    key = f'{phone_country_code}{phone_number}'
    result = cache.set(key, data, 125)
    return result
