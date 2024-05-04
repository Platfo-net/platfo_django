import os

__author__ = 'Arian'

# Secret Keys
os.environ["SECRET_KEY"] = os.environ.get("SECRET_KEY",
                                          "sample_secret_key")

os.environ["DATABASE_NAME"] = os.environ.get("DATABASE_NAME", "platfo")
os.environ["DATABASE_USER"] = os.environ.get("DATABASE_USER", "postgres")
os.environ["DATABASE_PASSWORD"] = os.environ.get("DATABASE_PASSWORD", "postgres")
os.environ["DATABASE_HOST"] = os.environ.get("DATABASE_HOST", "localhost")
os.environ["DATABASE_PORT"] = os.environ.get("DATABASE_PORT", "5432")

os.environ["REDIS_HOST"] = os.environ.get("REDIS_HOST", "localhost")
os.environ["REDIS_PORT"] = os.environ.get("REDIS_PORT", "6379")
os.environ["REDIS_USER"] = os.environ.get("REDIS_USER", "")
os.environ["REDIS_PASSWORD"] = os.environ.get("REDIS_PASSWORD", "")

# Primary django setting
from core.settings.base import *  # noqa
