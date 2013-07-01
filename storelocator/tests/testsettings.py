import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'testrunner',
        'KEY_PREFIX': 'testrunner',
    }
}

INSTALLED_APPS = [
    'storelocator',
]

LOGGING_CONFIG = None

SECRET_KEY = "blup"

TEST_RUNNER = 'discover_runner.DiscoverRunner'

ROOT_URLCONF = 'storelocator.urls'

USE_TZ = True
