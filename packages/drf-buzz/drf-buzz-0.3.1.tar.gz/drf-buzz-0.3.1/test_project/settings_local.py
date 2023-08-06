import os

from .settings import *  # noqa

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}}

LOCAL_APPS = ["test_app"]

INSTALLED_APPS = EXTERNAL_APPS + LOCAL_APPS

ROOT_URLCONF = "urls"
