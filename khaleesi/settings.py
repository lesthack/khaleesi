# -*- coding: utf-8 -*-
"""
Django settings for khaleesi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
import os, sys, traceback

try:
    from sensible import *
except ImportError:
    traceback.print_exc(file=sys.stdout)
    print 'Help: \n\tCreate a file khaleesi\sensible.py \n\tSample https://gist.github.com/lesthack/0485bc3c94f340d73570'
    sys.exit(0)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

HOST_NAME = 'khaleesi.unisem.mx'
URL_HOST = 'http://' + HOST_NAME

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['localhost', HOST_NAME]

ADMINS = (
    ('Jorge Hernandez', 'j.hernandez@maices.com')
)

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_crontab',
    'suit_redactor',
    'changelog',
    'track',
)

TEMPLATE_DIRS = (BASE_DIR+'/khaleesi/templates/',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'khaleesi.context_processors.context_url_host',
)

ROOT_URLCONF = 'khaleesi.urls'
WSGI_APPLICATION = 'khaleesi.wsgi.application'

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = BASE_DIR + '/static'
STATIC_URL = '/static/'

CRONJOBS = [
    ('* * * * *', 'track.cron.mail_sending'),
    ('30 18 * * *', 'track.cron.mail_daily'),
]

SUIT_CONFIG = {
    'ADMIN_NAME': 'Khaleesi',
    'MENU': [
        {'app': 'changelog', 'icon':'icon-asterisk', 'models': (
            'objeto', 'cambio',
        )},
        {'app': 'track', 'icon':'icon-tasks', 'label': 'Dashboard', 'models': (
            'proyecto', 'modulo', 'tarea', 'issue', 'pizarron', 'cita'
        )},
        {'label': 'Gantt', 'url': '/admin/gantt/', 'icon': 'icon-leaf'},
        {'label': 'Chrome Extension', 'url': 'https://chrome.google.com/webstore/detail/khaleesi-chrome-extension/lbgkpaeeldcdiapihpbflkjgaakmebjb?utm_source=chrome-app-launcher-info-dialog', 'icon': 'icon-fire'},
        {'label': 'Firefox Extension', 'url': 'https://drive.google.com/open?id=0B3lVvLj-naJYWW1nUTRlQWZnS0VITC1LWE8yMFo0NFMtR3Jv&authuser=0', 'icon': 'icon-fire'}
    ]
}
