import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# প্রোডাকশনের জন্য সিক্রেট কী এনভায়রনমেন্ট ভেরিয়েবল থেকে নেয়া ভালো, অন্যথায় ডিফল্ট কি ব্যবহার হবে
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", 
    "django-insecure-marriage-media-development-key-12345"
)


# SECURITY WARNING: don't run with debug turned on in production!
# প্রোডাকশনে এটি False রাখুন। প্রয়োজন হলে পরিবেশ অনুযায়ী বদলাতে পারেন:
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"


# আপনার ডোমেইন নাম বা সার্ভার IP এড্রেসগুলো এখানে যুক্ত করুন
ALLOWED_HOSTS = [
    "yourdomain.com",
    "www.yourdomain.com",
    "127.0.0.1",
    "localhost",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "home",
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


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# প্রোডাকশন সার্ভারে python manage.py collectstatic চালানোর সময় ফাইল জমার লোকেশন
STATIC_ROOT = BASE_DIR / "staticfiles"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"