"""
Django settings for kitab bazar project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import environ
from pathlib import Path
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str),
    DJANGO_ALLOWED_HOST=(str, '*'),
    DB_NAME=(str, 'postgres'),
    DB_USER=(str, 'postgres'),
    DB_PWD=(str, 'postgres'),
    DB_HOST=(str, 'db'),
    DB_PORT=(int, 5432),
    REDIS_URL=(str, 'redis://redis:6379/0'),
    CORS_ORIGIN_REGEX_WHITELIST=(str, r"^https://\w+\.togglecorp\.com$"),
    TIME_ZONE=(str, 'Asia/Kathmandu'),
    CLIENT_URL=(str, 'http://localhost:3080')
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [env('DJANGO_ALLOWED_HOST')]


# Application definition
APPS_DIR = os.path.join(BASE_DIR, 'apps')

LOCAL_APPS = [
    'apps.user',
    'apps.common',
    'apps.institution',
    'apps.publisher',
    'apps.school',
]

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'graphene_graphiql_explorer',
    'corsheaders',
] + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PWD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery settings
BROKER_URL = env("REDIS_URL")
BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_TIMEZONE = env('TIME_ZONE')
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60


# CORS CONFIGS
if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_REGEX_WHITELIST = [env('CORS_ORIGIN_REGEX_WHITELIST')]

CORS_URLS_REGEX = r'(^/api/.*$)|(^/media/.*$)|(^/graphql/$)'

AUTH_USER_MODEL = "user.User"

GRAPHENE = {
    'ATOMIC_MUTATIONS': True,
    'SCHEMA': 'config.schema.schema',
    'SCHEMA_OUTPUT': 'schema.json',
    'SCHEMA_INDENT': 2,
    'MIDDLEWARE': [
        'config.auth.WhiteListMiddleware',
    ],
}

GRAPHENE_DJANGO_EXTRAS = {
    'DEFAULT_PAGINATION_CLASS': 'graphene_django_extras.paginations.PageGraphqlPagination',
    'DEFAULT_PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 50
}

if not DEBUG:
    GRAPHENE['MIDDLEWARE'].append('utils.graphene.middleware.DisableIntrospectionSchemaMiddleware')

GRAPHENE_NODES_WHITELIST = (
    'login',
    'logout',
    'me',
    'register',
    'resetPassword',
    'generateResetPasswordToken',
    'activate',
    'province',
    'district',
    'municipality',
    'provinces',
    'districts',
    'municipalities',
    # __ double underscore nodes
    '__schema',
    '__type',
    '__typename',
)

CLIENT_URL = env('CLIENT_URL')

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "Kitab Bazar <kitabbazar@togglecorp.com>"

USE_I18N = True
USE_L10N = True
LOCALEURL_USE_ACCEPT_LANGUAGE = True
LANGUAGES = [
    ('en', _('English')),
    ('ne', _('Nepali')),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ne'
MODELTRANSLATION_LANGUAGES = ('en', 'ne')
