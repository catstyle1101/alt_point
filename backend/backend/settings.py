import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", 'django-insecure-c079+ftmw%5togxhjo6mk*j7#*5qty=5^xe(vf3c=&+=zbd6xr')
DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'phonenumber_field',
    'clients.apps.ClientsConfig',
    'utils',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.getenv("POSTGRES_USER", "user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("DB_HOST", "0.0.0.0"),
        "PORT": os.getenv("DB_PORT", "8000"),
    }
}

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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Yekaterinburg'
USE_I18N = True
USE_TZ = False
USE_L10N = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler',
    'COERCE_DECIMAL_TO_STRING': False,
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MAX_SERIES_LENGTH = 4
MAX_PASSPORT_NUMBER_LENGTH = 6
MAX_NAME_LENGTH = 100
MAX_GIVER_LENGTH = 200
ZIP_CODE_LENGTH = 6
MAX_COUNTRY_NAME_LENGTH = 200
MAX_REGION_NAME_LENGTH = 200
MAX_CITY_NAME_LENGTH = 200
MAX_STREET_NAME_LENGTH = 200
MAX_HOUSE_NAME_LENGTH = 20
MAX_APARTMENT_NAME_LENGTH = 20
TIN_NUMBER_LENGTH = 12
MAX_MONEY_DIGITS = 10
MAX_MONEY_DECIMAL_PLACES = 2
