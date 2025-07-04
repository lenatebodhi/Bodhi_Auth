"""
Django settings for Bodhi project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import environ
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))  # reading .env file
env = environ.Env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+y0d%cn__#!97t-*%pq5f-!s#ruj40p&-ejssdj94zvbh3&6ke'
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "django-insecure-+y0d%cn__#!97t-*%pq5f-!s#ruj40p&-ejssdj94zvbh3&6ke")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'accounts',
    'courses'
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


ROOT_URLCONF = 'Bodhi.urls'

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

WSGI_APPLICATION = 'Bodhi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "NAME": env.str("DATABASE_NAME", default="bodhi"),
#         "ENGINE": "django.db.backends.postgresql",
#         "USER": env.str("DATABASE_USERNAME", default=""),
#         "PASSWORD": env.str("DATABASE_PASSWORD", default=""),
#         "HOST": env.str("DATABASE_HOST", default="localhost"),
#         # 'HOST': 'db',
#         "PORT": "5432",
#     }
# }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="bodhi"),
        "USER": env("POSTGRES_USER", default="postgres"),
        "PASSWORD": env("POSTGRES_PASSWORD", default=""),
        "HOST": "db",  # ✅ not localhost
        "PORT": 5432,
    }
}




print(DATABASES)


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Celery Configuration
CELERY_BROKER_URL="redis://redis:6379/0"
RESULT_BACKEND="redis://redis:6379/0"
accept_content = ['application/json']
task_serializer = 'json'
result_serializer= 'json'
broker_connection_retry_on_startup = True


# JWT configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "JTI_CLAIM": "jti",
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SECRET_KEY,  # 🔐 explicitly set
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default=False)
DEFAULT_FROM_EMAIL = 'ROH<%s>' % EMAIL_HOST_USER
SERVER_EMAIL = 'ROH<%s>' % EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default=False)
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = True

DEFAULT_BASE_URL = env.str('DEFAULT_BASE_URL',default='')


# TWILO_ACCOUNT_SID = env.str('TWILO_ACCOUNT_SID',default='')
# TWILO_ACCESS_TOKEN = env.str('TWILO_ACCESS_TOKEN',default='')
# TWILO_SERVICE_ID= env.str('TWILO_SERVICE_ID',default='')
