﻿# Django settings for lowcostsite project.

import os
import sys

DIRNAME = os.path.dirname(__file__)

at_project_root = lambda name: os.path.join(DIRNAME, name)
sys.path.insert(0, DIRNAME)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'panov.db',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Yekaterinburg'
DATE_FORMAT = 'j.n.Y'
TIME_FORMAT = 'G:i'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'panov', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
STATIC_URL = MEDIA_URL = '/assets/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'zzxpn(ktv8jg6+son708$h$79q0kye&)f^fn7bep92u5)qp61_'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'request.middleware.RequestMiddleware'

)

ROOT_URLCONF = 'urls'


INSTALLED_APPS = [

    # admin tools
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    # contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.redirects',

    'django_coverage',
    'request',
    'simple_history',
    'sorl.thumbnail',
    #'south',

    # main
    'panov',

]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.auth.context_processors.auth',
    'panov.context_processors.settings',
)

LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'advanced': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'advanced_error': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - error: %(message)s'
    
            },
        },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'advanced',
            'stream': sys.stdout,
        },
        'error': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'advanced_error',
            'stream': sys.stderr,

        },

    },
    'loggers': {
        '': {
            'handlers': ['default', 'error'],
            'level': 'INFO',
            'propagate': False
        },

    },
}


if 'django-nosetests.py' in sys.argv[0]:
    
    LOGGING['handlers']['file_out'] = {
                                   'level': 'INFO',
                                   'class': 'logging.FileHandler',
                                   'formatter': 'advanced',
                                   'mode': 'w',
                                   'filename': 'tests_out.txt'
                                   }
    
    LOGGING['handlers']['file_error'] = {
                                   'level': 'INFO',
                                   'class': 'logging.FileHandler',
                                   'formatter': 'advanced_error',
                                   'mode': 'w',
                                   'filename' : 'tests_error.txt'
                                   }
    
    LOGGING['loggers']['']['handlers'].append('file_out')  
    LOGGING['loggers']['']['handlers'].append('file_error')

        
SOUTH_TESTS_MIGRATE = False

REQUEST_LIST_PAGE_LIMIT = 10
REQUEST_LIST_PAGE_ORDER_BY = '-requestextension__priority'

LOGIN_REDIRECT_URL = '/'
THUMBNAIL_DEBUG = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'django_cache',
    }
}

try:
    from settings_local import *
except ImportError:
    pass
