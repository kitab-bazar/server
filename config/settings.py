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
from django.utils.translation import gettext_lazy as _
from utils import sentry


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
    CORS_ORIGIN_REGEX_WHITELIST=(str, 'r\"^https://\w+\.togglecorp\.com$\"'), # noqa W605
    TIME_ZONE=(str, 'Asia/Kathmandu'),
    CLIENT_URL=(str, 'http://localhost:3080'),
    # Static, Media configs
    DJANGO_STATIC_URL=(str, '/static/'),
    DJANGO_MEDIA_URL=(str, '/media/'),
    DJANGO_STATIC_ROOT=(str, os.path.join(BASE_DIR, "staticfiles")),
    DJANGO_MEDIA_ROOT=(str, os.path.join(BASE_DIR, "media")),
    # AWS static, media configs
    AWS_STORAGE_BUCKET_NAME=(str, None),
    # NOTE: aws access key id, and aws secret access keys are required if aws policy
    # is not set otherwise these variables are not required
    AWS_S3_ACCESS_KEY_ID=(str, None),
    AWS_S3_SECRET_ACCESS_KEY=(str, None),
    TEMP_DIR=(str, '/tmp'),
    HCAPTCHA_SECRET=(str, '0x0000000000000000000000000000000000000000'),
    MAX_LOGIN_ATTEMPTS=(int, 3),
    MAX_CAPTCHA_LOGIN_ATTEMPTS=(int, 10),
    LOGIN_TIMEOUT=(int, 10 * 60),
    # Sentry settings
    SENTRY_DSN=(str, None),
    ENVIRONMENT=(str, 'local'),
    DJANGO_API_HOST=(str, 'localhost'),
    SENTRY_SAMPLE_RATE=(float, 0.2),
    AWS_ACCESS_KEY_ID=(str, 'AWS_ACCESS_KEY_ID'),
    AWS_SECRET_ACCESS_KEY=(str, 'AWS_SECRET_ACCESS_KEY'),
    DEFAULT_FROM_EMAIL=(str, 'Kitab Bazar <kitabbazar@togglecorp.com>'),
    USE_LOCAL_STORATE=(bool, True),
    ENABLE_INTROSEPTION_SCHEMA=(bool, False),
    HTTP_PROTOCOL=(str, 'http')
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['server', env('DJANGO_ALLOWED_HOST')]
DJANGO_API_HOST = env('DJANGO_API_HOST')

HTTP_PROTOCOL = env('HTTP_PROTOCOL')

if HTTP_PROTOCOL == 'https':
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    # SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 30  # TODO: Increase this slowly
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
APPS_DIR = os.path.join(BASE_DIR, 'apps')

LOCAL_APPS = [
    'apps.user',
    'apps.common',
    'apps.institution',
    'apps.publisher',
    'apps.school',
    'apps.book',
    'apps.order',
    'apps.notification',
    'apps.helpdesk',
    'apps.blog',
    'apps.payment',
    'apps.package',
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
    'phonenumber_field',
    'tinymce',
    'storages',
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

if DEBUG or env('USE_LOCAL_STORATE'):
    STATIC_URL = env('DJANGO_STATIC_URL')
    MEDIA_URL = env('DJANGO_MEDIA_URL')
    STATIC_ROOT = env('DJANGO_STATIC_ROOT')
    MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')
else:
    AWS_S3_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{env('DJANGO_STATIC_URL')}/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{env('DJANGO_MEDIA_URL')}/"
    TINYMCE_JS_URL = f'{STATIC_URL}tinymce/tinymce.min.js'

    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

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

CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r'(^/api/.*$)|(^/media/.*$)|(^/graphql/$)'
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'accept-language',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'sentry-trace',
)

AUTH_USER_MODEL = "user.User"

GRAPHENE = {
    'ATOMIC_MUTATIONS': True,
    'SCHEMA': 'config.schema.schema',
    'SCHEMA_OUTPUT': 'schema.json',
    'SCHEMA_INDENT': 2,
    'MIDDLEWARE': [
        'config.auth.WhiteListMiddleware',
        'utils.sentry.SentryGrapheneMiddleware',
    ],
}

GRAPHENE_DJANGO_EXTRAS = {
    'DEFAULT_PAGINATION_CLASS': 'graphene_django_extras.paginations.PageGraphqlPagination',
    'DEFAULT_PAGE_SIZE': 25,
    'MAX_PAGE_SIZE': 50
}

ENABLE_INTROSEPTION_SCHEMA = env('ENABLE_INTROSEPTION_SCHEMA')

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
    'books',
    'book',
    'tags',
    'categories',
    'authors',
    'createContactMessage',
    'publisher',
    'publishers',
)

CLIENT_URL = env('CLIENT_URL')

# Smtp settings
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = 'django_ses.SESBackend'
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

USE_I18N = True
USE_L10N = True
LOCALEURL_USE_ACCEPT_LANGUAGE = True
LANGUAGES = [
    ('en', _('English')),
    ('ne', _('Nepali')),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ne')

# Locale dir for language transaction
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Set default reason to nepal
PHONENUMBER_DEFAULT_REGION = 'NP'

# Tinymce settings
DJANGO_SETTINGS_MODULE = "testtinymce.settings"
TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": (
        "advlist autolink lists link image charmap print preview anchor "
        "searchreplace visualblocks code fullscreen insertdatetime media table "
        "paste code help wordcount spellchecker"
    ),
    "toolbar": (
        "undo redo | bold italic underline strikethrough | fontselect "
        "fontsizeselect formatselect | alignleft aligncenter alignright "
        "alignjustify | outdent indent |  numlist bullist checklist | forecolor "
        "backcolor casechange permanentpen formatpainter removeformat | "
        "pagebreak | charmap emoticons | fullscreen  preview save print | "
        "insertfile image media pageembed template link anchor codesample | "
        "a11ycheck ltr rtl | showcomments addcomment code"
    ),
    "custom_undo_redo_levels": 10,
    "language": "en",
}
# Used to save og images temporarily
TEMP_DIR = env('TEMP_DIR')

# Hcaptcha
HCAPTCHA_SECRET = env('HCAPTCHA_SECRET')
MAX_LOGIN_ATTEMPTS = env('MAX_LOGIN_ATTEMPTS')
MAX_CAPTCHA_LOGIN_ATTEMPTS = env('MAX_CAPTCHA_LOGIN_ATTEMPTS')
LOGIN_TIMEOUT = env('LOGIN_TIMEOUT')

# Sentry Config
SENTRY_DSN = env('SENTRY_DSN')
SENTRY_SAMPLE_RATE = env('SENTRY_SAMPLE_RATE')
if SENTRY_DSN:
    SENTRY_CONFIG = {
        'dsn': env('SENTRY_DSN'),
        'send_default_pii': True,
        'release': sentry.fetch_git_sha(BASE_DIR),
        'environment': env('ENVIRONMENT'),
        'debug': DEBUG,
        'tags': {
            'site': DJANGO_API_HOST,
        },
    }
    sentry.init_sentry(
        app_type='API',
        **SENTRY_CONFIG,
    )
