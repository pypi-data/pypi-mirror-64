import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

EXTERNAL_APPS = ["django.contrib.auth", "django.contrib.contenttypes"]

LOCAL_APPS = ["test_project.test_app"]

INSTALLED_APPS = EXTERNAL_APPS + LOCAL_APPS

ROOT_URLCONF = "test_project.urls"

SITE_ID = 1

SECRET_KEY = "foobar"

USE_L10N = True

# MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_URL = "/media/"

# STATIC CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_URL = "/static/"

# DRF CONFIGURATION
REST_FRAMEWORK = {"EXCEPTION_HANDLER": "drf_buzz.exception_handler"}
