"""
Django settings for huesped_backend project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import pip
from .critical_settings import * #Configuraciones propias de cada entorno, que deben mantenerse fuera del source code
from subprocess import check_output

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

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
    'rest_framework.authtoken',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    'hc_practicas',
    'hc_common',
    'hc_pacientes',
    'hc_core',
    'hc_notificaciones',
    'reversion'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reversion.middleware.RevisionMiddleware'
]

ROOT_URLCONF = 'huesped_backend.urls'

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

WSGI_APPLICATION = 'huesped_backend.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

LOGOUT_ON_PASSWORD_CHANGE = False

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),

    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny'
    ],

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',

    'DEFAULT_PAGINATION_CLASS': 'hc_core.paginators.ParameterPageNumberPaginator'
}

#CORS headers applied to all hosts
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

CORS_EXPOSE_HEADERS = {
    'auth-token'
}

#
# Notifications configuration
#

# Days to look in advance to send notifications
NOTIFICATION_ANTICIPATION_DAYS = os.getenv('NOTIFICATION_ANTICIPATION_DAYS', 2)

# Set to true to activate these chanels
SEND_SMS_NOTIFICATIONS = True
SEND_EMAIL_NOTIFICATIONS = True

# Email configuration
EMAIL_HOST = os.getenv('EMAIL_HOST', 'EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT', 'PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'EMAIL_HOST_PASSWORD')
EMAIL_SENDER_ADDRESS = os.getenv('EMAIL_SENDER_ADDRESS', 'EMAIL_SENDER_ADDRESS')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', False)




# SMS Configurations
BASE_SMS_URL = os.getenv('BASE_SMS_URL', 'BASE_SMS_URL')
SMS_SERVICE_USER = os.getenv('SMS_SERVICE_USER', 'SMS_SERVICE_USER')
SMS_SERVICE_PASSWORD = os.getenv('SMS_SERVICE_PASSWORD', 'SMS_SERVICE_PASSWORD')



# TODO Replace this with jenkins build info file
try:
    GIT_INFO = {
        'branch': check_output(['git', 'rev-parse', '--abbrev-ref',
                                'HEAD']).strip(),
        'commit': {
            'hash': check_output(['git', 'rev-parse', 'HEAD']).strip(),
            'date': check_output(['git', 'show', '-s', '--format=%ci',
                                  'HEAD']).strip()
        }
    }
except:
    GIT_INFO = None

DEPENDENCIES_INFO = {
    dist.key: dist.version
    for dist in pip.get_installed_distributions()
}
