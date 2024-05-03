# yapf: disable

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False

HOSTNAME = 'localhost:8000'

ALLOWED_HOSTS = []

# Application definition apps
FIRST_PARTY_APPS = [
    # 'utilities',

    # 'account',
]

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.postgres',

    # 'jalali_date',
    # 'django_migration_scripts',

    # 'corsheaders',

    # 'rest_framework',
    # 'rest_framework.authtoken',
    # 'django_jalali',
    # 'django_celery_beat',
    # 'django_celery_results',
    # 'django_linear_migrations',

    *FIRST_PARTY_APPS,

    # 'import_export',
    # 'django_json_widget',
    # 'drf_multiple_model',
    # 'psql_optimizer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # 'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'utilities.middlewares.business_logic_middleware.ApplicationExceptionMiddleware',

]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')),
                              "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
    # 'default': {
    #     'ENGINE': 'psqlextra.backend',
    #     'NAME': os.environ["DATABASE_NAME"],
    #     'USER': os.environ["DATABASE_USER"],
    #     'PASSWORD': os.environ["DATABASE_PASSWORD"],
    #     'HOST': os.environ["DATABASE_HOST"],
    #     'PORT': os.environ["DATABASE_PORT"],
    # }
}

# REST_FRAMEWORK = {
#     'EXCEPTION_HANDLER': 'utilities.http.exceptions.exception_handler',
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.TokenAuthentication',
#     ),
#     'DEFAULT_PAGINATION_CLASS':
#         'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 15,
#     'DEFAULT_THROTTLE_RATES': {
#         'burst': '1/minute',
#         'voucher': '5/minute',
#         'create_order': '20/minute',
#         'cancel_order': '20/minute',
#         'remove_item_from_cart': '20/minute',
#         'create_driver_payment': '3/day',
#     },
# }

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = './front-end/'
MEDIA_URL = '/media/'
MEDIA_ROOT = './media/'

# CORS_ORIGIN_ALLOW_ALL = True
#
# CORS_ALLOW_HEADERS = (
#     'x-requested-with',
#     'content-type',
#     'accept',
#     'origin',
#     'authorization',
#     'x-csrftoken',
#     'user-agent',
#     'accept-encoding',
#     'sentry-trace',
#     'access-mode',
#     'entity-id',
# )

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'root': {
#         'level': 'DEBUG',
#         'handlers': ['console'],
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['console'],
#             'propagate': False,
#             'level': 'DEBUG',
#         }
#     },
#     'formatters': {
#         'json': {
#             '()': 'logging_utilities.formatters.json_formatter.JsonFormatter',
#             'add_always_extra': True,
#             'fmt': {
#                 'time': 'asctime',
#                 'level': 'levelname',
#                 'logger': 'name',
#                 'module': 'module',
#                 'message': 'message',
#             },
#         }
#     },
#     'filters': {
#         'ignore_gdal_errors': {
#             '()': 'django.utils.log.CallbackFilter',
#             'callback': ignore_gdal_errors,
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'class': 'infrastructure.stream_handler_with_extra.StreamHandlerWithExtra',
#             'formatter': 'json'
#         }
#     },
# }

USE_SSL = True

def get_redis_connection_string(host: str, port: str, username: str = "",
                                password: str = "") -> str:
    if not username and not password:
        return f'redis://{host}:{port}/0'

    return f'redis://{username}:{password}@{host}:{port}/0'


# REDIS_HOST = os.environ["REDIS_HOST"]
# REDIS_PORT = os.environ["REDIS_PORT"]
# REDIS_USER = os.environ["REDIS_USER"]
# REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]

# Celery settings
# CELERY_BROKER_URL = get_redis_connection_string(REDIS_HOST,
#                                                 REDIS_PORT,
#                                                 REDIS_USER,
#                                                 REDIS_PASSWORD)
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_ACCEPT_CONTENT = ['pickle', 'json']
# CELERY_TASK_SERIALIZER = 'pickle'
# CELERY_RESULT_SERIALIZER = 'pickle'
# CELERY_TIMEZONE = 'Iran'
# CELERY_WORKER_SEND_TASK_EVENTS = True
# CELERY_TASK_SEND_SENT_EVENT = True
# CELERY_BROKER_TRANSPORT_OPTIONS = {
#     'priority_steps': list(range(10)),
#     'queue_order_strategy': 'priority',
# }


# Cache
def redis_key_maker(key, key_prefix, version):
    return key


def redis_reverse_key_maker(key):
    return key


# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': get_redis_connection_string(REDIS_HOST,
#                                                 REDIS_PORT,
#                                                 REDIS_USER,
#                                                 REDIS_PASSWORD),
#         'OPTIONS': {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
#         },
#         'KEY_FUNCTION': redis_key_maker,
#         'REVERSE_KEY_FUNCTION': redis_reverse_key_maker
#     },
#     'cache_page': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': get_redis_connection_string(REDIS_HOST,
#                                                 REDIS_PORT,
#                                                 REDIS_USER,
#                                                 REDIS_PASSWORD),
#         'OPTIONS': {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     },
# }
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_TTL = 60 * 1

# object storage related configs
# If set true , django media will be uploaded to spaces , otherwise they will be stored locally
# this setting tells django-storage not to add sign and expire params to uploaded files
USE_S3 = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# directory that files are uploaded to
# AWS_LOCATION = os.environ.get('AWS_LOCATION')
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
# AWS_S3_ADDRESSING_STYLE = os.environ.get('AWS_S3_ADDRESSING_STYLE', 'virtual')

# HTTP Requests
DEFAULT_REQUESTS_TIMEOUT = 10

DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024  # 20 MBs
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB

IS_PRODUCTION = False

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

USE_DEPRECATED_PYTZ = True
