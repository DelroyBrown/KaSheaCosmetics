# KaSheaCosmetics_base\settings.py
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("SECRET_KEY", '')

DEBUG = 'DEVLOPMENT' in os.environ

ALLOWED_HOSTS = ['kashea-cosmetics-8f8861f9a989.herokuapp.com/', 'localhost']

# Import admin settings
try:
    from .admin_settings import *
except ImportError as e:
    raise ImportError(f"Could not import admin settings: {e}")


INSTALLED_APPS = [
    # New Admin
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # My Apps
    "KaSheaCosmetics_base",
    "KaSheaCosmetics_home",
    "KaSheaCosmetics_products",
    "KaSheaCosmetics_cart",
    "KaSheaCosmetics_checkout",
    "KaSheaCosmetics_orders",
    "KaSheaCosmetics_subscriptions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "KaSheaCosmetics_base.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "KaSheaCosmetics_products.views.side_nav_categories",
            ],
        },
    },
]

WSGI_APPLICATION = "KaSheaCosmetics_base.wsgi.application"

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default' : dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# DATABASES = {
#     "default": dj_database_url.parse(
#         "postgres://ud5dd4fujmal6d:pc64ecb2a0e8793971cec5dbb4050b821cc5c5a0e9ee78e5fa40aaedb2f9f3059@clhtb6lu92mj2.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d6hd6qnpuvootm"
#     )
# }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#  STRIPE STUFF

STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
