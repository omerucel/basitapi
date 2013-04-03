import os
import sys

from django.conf import settings

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'basitapi',
    'django_nose',
]


if not settings.configured:
    settings.configure(
        DATABASES={
            'default':{
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=INSTALLED_APPS,
        ROOT_URLCONF='basitapi.tests.urls',
    )

from django_nose import NoseTestSuiteRunner

def runtests(*test_args):
    failures = NoseTestSuiteRunner(verbosity=2, interactive=True).run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
