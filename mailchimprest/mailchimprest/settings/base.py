"""
This file contains all default Django settings.

It is extended by local, development and production setting files.

------------------------------------------------------------------------

"""


import os
from mailchimp3 import MailChimp


ALLOWED_HOSTS = ['*']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECRET_KEY = os.environ['SECRET_KEY']


MAILCHIMP_DC = os.environ['MAILCHIMP_DC']
MAILCHIMP_BASE_URL = f'https://{MAILCHIMP_DC}.api.mailchimp.com/3.0'
MAILCHIMP_KEY = os.environ['MAILCHIMP_KEY']
MAILCHIMP_API_KEY = f'{MAILCHIMP_KEY}-{MAILCHIMP_DC}'
MAILCHIMP_USERNAME = os.environ['MAILCHIMP_USERNAME']
# TO DO useragent
MAILCHIMP_CLIENT = MailChimp(
    mc_api=MAILCHIMP_API_KEY,
    mc_user=MAILCHIMP_USERNAME,
    timeout=30.0
)
MAILCHIMP_LIST_ID = os.environ['MAILCHIMP_LIST_ID']
MAILCHIMP_MEMBER_FIELDS = [
    'id',
    'email_address',
    'merge_fields',
    'status',
    'timestamp_signup',
    'last_changed',
    'tags'
]

MANAGERS = [
    ('Manager', 'annie.thiessen@icloud.com'),
]
ADMINS = [
    ('Administrator', 'annie.thiessen@icloud.com'),
]


# --- application definition ---
ROOT_URLCONF = 'mailchimprest.urls'
WSGI_APPLICATION = 'mailchimprest.wsgi.application'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'markdown',
    'mailchimp.apps.MailChimpAppConfig',
    'django_extensions',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

# --- database settings ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# --- internationalization settings ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# static files settings ---
STATIC_URL = '/static/'


# rest_framework settings ---
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}


# --- logging settings ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'incremental': True,
    'root': {
        'level': 'DEBUG',
    },
}


LOCAL = 0
DEVELOPMENT = 1
PRODUCTION = 2
