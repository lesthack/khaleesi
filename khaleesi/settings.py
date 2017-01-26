# -*- coding: utf-8 -*-
"""
Django settings for khaleesi project.
"""

import os, sys, traceback

SECRET_KEY = 'z6zel7bs)1!1=adwrh(1%hqup_)rra@57ytukv*66_+es3qh_c'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True
HOST_NAME       = 'localhost'
URL_HOST        = 'http://' + HOST_NAME
ALLOWED_HOSTS   = ['localhost', HOST_NAME, '192.168.33.20', '192.168.1.83', '192.168.16.21']

try:
    from sensible import *
except ImportError:
    traceback.print_exc(file=sys.stdout)
    print 'Help: \n\tCreate a file khaleesi\sensible.py \n\tSample https://gist.github.com/lesthack/0485bc3c94f340d73570'
    sys.exit(0)

ADMINS = (
    ('Admin', 'iam@jorgeluis.com.mx')
)

INSTALLED_APPS = [
    #'material',
    #'material.admin',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    #'tastypie',
    'changelog',
    'track',
]

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'khaleesi.urls'
WSGI_APPLICATION = 'khaleesi.wsgi.application'


LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = BASE_DIR + '/static'
STATIC_URL = '/static/'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Jet
JET_SIDE_MENU_COMPACT = True
