# noinspection PyUnresolvedReferences

from core.settings.base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
HOSTNAME = 'localhost:8000'
USE_SSL = False

ALLOWED_HOSTS = ['*']

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# INSTALLED_APPS.append('debug_toolbar')
INTERNAL_IPS = ['127.0.0.1', ]
