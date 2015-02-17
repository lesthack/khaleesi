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

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['localhost', 'khaleesi.unisem.mx']

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
    ('0 8 * * *', 'track.cron.mail_daily'),
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
        {'label': 'Gantt', 'url': '/admin/gantt/', 'icon': 'icon-leaf'}
    ]
}
