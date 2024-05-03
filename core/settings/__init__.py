import os

__author__ = 'Arian'

# Secret Keys
os.environ["SECRET_KEY"] = os.environ.get("SECRET_KEY",
                                          "django-insecure-z98&ulx0i4ndx=ckxeecu8r6fm**r++hw8*g8av8&0ay(b(9rx")

os.environ["DATABASE_NAME"] = os.environ.get("DATABASE_NAME", "miare")
os.environ["DATABASE_USER"] = os.environ.get("DATABASE_USER", "miare")
os.environ["DATABASE_PASSWORD"] = os.environ.get("DATABASE_PASSWORD", "miare")
os.environ["DATABASE_HOST"] = os.environ.get("DATABASE_HOST", "localhost")
os.environ["DATABASE_PORT"] = os.environ.get("DATABASE_PORT", "5432")

os.environ["REDIS_HOST"] = os.environ.get("REDIS_HOST", "localhost")
os.environ["REDIS_PORT"] = os.environ.get("REDIS_PORT", "6379")
os.environ["REDIS_USER"] = os.environ.get("REDIS_USER", "")
os.environ["REDIS_PASSWORD"] = os.environ.get("REDIS_PASSWORD", "")

# Primary django setting
from core.settings.base import *  # noqa
