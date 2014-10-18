# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import dotenv
dotenv.read_dotenv()

from getenv import env

PLATFORM_VERSION = "0.03"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6ug(5zb3$&kt5fwkh@yd%=1htq5ww#754q4tn^nmhglybj$)!_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'postman',
    #'django_facebook',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.openid',
    'south',

    'shared',
    'gc_steam',
    'frontend',
    'profiles',
    'conversation',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gamecoach.urls'

WSGI_APPLICATION = 'gamecoach.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en_US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

POSTMAN_AUTO_MODERATE_AS = True

AUTHENTICATION_BACKENDS = (
    #'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
    "allauth.account.auth_backends.AuthenticationBackend",
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django_facebook.context_processors.facebook",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",  # Added

    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",

    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': env('LOGGING_MAIN_FILE'),
            'formatter': 'verbose',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'] if DEBUG else ['logfile'],
            'propagate': True,
            'level': 'DEBUG' if DEBUG else 'ERROR',
        },
        'django.request': {
            'handlers': ['console', 'logfile'] if DEBUG else ['logfile'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': False,
        },
        'frontend': {
            'handlers': ['console', 'logfile'] if DEBUG else ['logfile'],
            'propagate': False,
            'level': 'DEBUG' if DEBUG else 'ERROR',
        }
    }
}

FACEBOOK_APP_ID = env('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = env('FACEBOOK_APP_SECRET')
FACEBOOK_TEST_USER = env('FACEBOOK_TEST_USER')
FACEBOOK_TEST_PASSWORD = env('FACEBOOK_TEST_PASSWORD')
#AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'
#AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MEDIA_ROOT = env('MEDIA_ROOT')

DISTRIBUTION = env('DISTRIBUTION')

CALQ_WRITE_KEY = env('CALQ_WRITE_KEY')

os.environ['REUSE_DB'] = "1"

SITE_DOMAIN = env('SITE_DOMAIN')
SITE_NAME = env('SITE_NAME')
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email'],
        'METHOD': 'js_sdk'
    }
}

STEAM_API_ROOT = env('STEAM_API_ROOT')
STEAM_API_KEY = env('STEAM_API_KEY')
STEAM_OPENID_ENDPOINT = env('STEAM_OPENID_ENDPOINT')
STEAM_TEST_UID = env('STEAM_TEST_UID')
STEAM_TEST_PERSONANAME = env('STEAM_TEST_PERSONANAME')
