# yapf: disable

import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False

HOSTNAME = 'localhost:8000'

ALLOWED_HOSTS = []

# Application definition apps
FIRST_PARTY_APPS = [
    'account',
    'credit',
    'etl',
    'store',
    'notification',
    'llm',
    'telegram',

    'utilities',
]

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # 'django_migration_scripts',

    # 'corsheaders',

    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    # 'rest_framework.authtoken',
    'django_jalali',
    'django_celery_beat',
    'django_celery_results',
    # 'django_linear_migrations',

    *FIRST_PARTY_APPS,

    # 'import_export',
    # 'django_json_widget',
    # 'psql_optimizer',
]

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'utilities.middlewares.business_logic_middleware.ApplicationExceptionMiddleware',

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

AUTH_USER_MODEL = 'account.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["DATABASE_NAME"],
        'USER': os.environ["DATABASE_USER"],
        'PASSWORD': os.environ["DATABASE_PASSWORD"],
        'HOST': os.environ["DATABASE_HOST"],
        'PORT': os.environ["DATABASE_PORT"],
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utilities.http.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=20),
}

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
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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


# Redis settings
def get_redis_connection_string(host: str, port: str, username: str = "",
                                password: str = "") -> str:
    if not username and not password:
        return f'redis://{host}:{port}/0'

    return f'redis://{username}:{password}@{host}:{port}/0'


REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]
REDIS_USER = os.environ.get("REDIS_USER", "")
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]

# Celery settings
CELERY_BROKER_URL = get_redis_connection_string(REDIS_HOST,
                                                REDIS_PORT,
                                                REDIS_USER,
                                                REDIS_PASSWORD)
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'Iran'
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'priority_steps': list(range(10)),
    'queue_order_strategy': 'priority',
}


# Cache
def redis_key_maker(key, key_prefix, version):
    return key


def redis_reverse_key_maker(key):
    return key


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': get_redis_connection_string(REDIS_HOST,
                                                REDIS_PORT,
                                                REDIS_USER,
                                                REDIS_PASSWORD),
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        },
        'KEY_FUNCTION': redis_key_maker,
        'REVERSE_KEY_FUNCTION': redis_reverse_key_maker
    },
    'cache_page': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': get_redis_connection_string(REDIS_HOST,
                                                REDIS_PORT,
                                                REDIS_USER,
                                                REDIS_PASSWORD),
        'OPTIONS': {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_TTL = 60 * 1

# object storage related configs
# If set true , django media will be uploaded to spaces , otherwise they will be stored locally
# this setting tells django-storage not to add sign and expire params to uploaded files

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# S3 configs
S3_HOST = os.environ.get('S3_HOST')
S3_ROOT_USER = os.environ.get('S3_ROOT_USER')
S3_ROOT_PASSWORD = os.environ.get('S3_ROOT_PASSWORD')

S3_USER_PROFILE_BUCKET = os.environ.get('S3_USER_PROFILE_BUCKET')
S3_SHOP_PRODUCT_IMAGE_BUCKET = os.environ.get('S3_SHOP_PRODUCT_IMAGE_BUCKET')
S3_SHOP_CATEGORY_IMAGE_BUCKET = os.environ.get('S3_SHOP_CATEGORY_IMAGE_BUCKET')
S3_TELEGRAM_BOT_IMAGES_BUCKET = os.environ.get('S3_TELEGRAM_BOT_IMAGES_BUCKET')
S3_TELEGRAM_BOT_MENU_IMAGES_BUCKET = os.environ.get('S3_TELEGRAM_BOT_MENU_IMAGES_BUCKET')
S3_PAYMENT_RECEIPT_IMAGE = os.environ.get('S3_PAYMENT_RECEIPT_IMAGE')
S3_SHOP_TELEGRAM_CREDIT_EXTENDING = os.environ.get('S3_SHOP_TELEGRAM_CREDIT_EXTENDING')
S3_KNOWLEDGE_BASE_BUCKET = os.environ.get('S3_KNOWLEDGE_BASE_BUCKET')
S3_MESSAGE_BUILDER_IMAGE_BUCKET = os.environ.get('S3_MESSAGE_BUILDER_IMAGE_BUCKET')

# HTTP Requests
DEFAULT_REQUESTS_TIMEOUT = 10

DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024  # 20 MBs
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB

IS_PRODUCTION = False

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

USE_DEPRECATED_PYTZ = True
