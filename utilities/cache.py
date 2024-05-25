from django.core.cache import cache


def get_user_code(phone_number, phone_country_code):
    key = f'{phone_country_code}{phone_number}'
    data = cache.get(key)
    return data


def set_user_code(phone_number, phone_country_code, code, token):
    data = {'code': code, 'token': token}
    key = f'{phone_country_code}{phone_number}'
    result = cache.set(key, data, 125)
    return result


def remove_user_code(phone_number, phone_country_code):
    key = f'{phone_country_code}{phone_number}'
    cache.delete(key)
