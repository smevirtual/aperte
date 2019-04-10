# Copyright 2018 SME Virtual Network Contributors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Common Django settings for all project environments.
"""
# pylint: disable=C0111,W0232

# Third Party
import environ
from configurations import Configuration, values
from django.utils.translation import ugettext_lazy as _


def get_release():
    import aperte
    import os
    import raven
    release = aperte.__version__
    try:
        git_hash = raven.fetch_git_sha(os.path.dirname(os.pardir))[:7]
        release = '{}-{}'.format(release, git_hash)
    except raven.exceptions.InvalidGitRepository:
        pass
    return release


class Common(Configuration):
    REPO_ROOT_DIR: str = environ.Path(__file__) - 2
    APPS_ROOT_DIR: str = REPO_ROOT_DIR.path('aperte')

    env = environ.Env()

    # See https://docs.djangoproject.com/en/2.0/ref/settings/ for a description
    # of each Django setting.

    # CORE SETTINGS
    # --------------------------------------------------------------------------
    DEBUG = values.BooleanValue(False)
    TIME_ZONE = values.Value('UTC')
    USE_TZ = True
    if USE_TZ:
        from django.conf.locale.en import formats
        formats.DATETIME_FORMAT = values.Value('m/d/Y h:i:s T', environ_name='DJANGO_DATETIME_FORMAT')
    LANGUAGE_CODE = values.Value('en-us')
    LANGUAGES = (
        ('en', _('English')),
    )
    LOCALE_PATHS = (
        str(APPS_ROOT_DIR.path('locale')),
    )
    USE_I18N = values.BooleanValue(True)
    USE_L10N = values.BooleanValue(True)
    FIXTURE_DIRS = (
        str(APPS_ROOT_DIR.path('fixtures')),
    )
    WSGI_APPLICATION = 'wsgi.application'
    # Note: This variable is an empty list by default for security reasons. The
    #       allowed hosts for Django to serve must be specified explicitly in
    #       all environments.
    ALLOWED_HOSTS = values.ListValue([], environ_required=True)

    # INSTALLED APPS SETTINGS
    # --------------------------------------------------------------------------
    DJANGO_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django_sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
    ]
    LOCAL_APPS = [
        'aperte.base',
        'aperte.users',
    ]
    THIRD_PARTY_APPS = [
        # TODO: Re-enable this.
        # 'allauth',
        # 'allauth.account',
        # 'allauth.socialaccount',
        # 'allauth.socialaccount.providers.github',
        # 'allauth.socialaccount.providers.google',
        # 'allauth.socialaccount.providers.linkedin',
        # 'allauth.socialaccount.providers.linkedin_oauth2',
        'versatileimagefield',
        # TODO: Re-enable this.
        # 'corsheaders',
        'raven.contrib.django.raven_compat',
        'mail_templated',
    ]
    INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

    # URL SETTINGS
    # --------------------------------------------------------------------------
    ROOT_URLCONF = 'aperte.urls'

    # ADMIN SETTINGS
    # --------------------------------------------------------------------------
    ADMIN_URL = values.Value('admin')
    ADMINS = [
        ("""Adam Cook""", 'adam.j.cook@alliedstrand.com'),
    ]
    ADMINS = values.SingleNestedTupleValue((
        ('SME Virtual Network Admin', 'aperte@smevirtual.com')
    ))
    MANAGERS = ADMINS

    # AUTHENTICATION AND LOGIN SETTINGS
    # --------------------------------------------------------------------------
    AUTH_USER_MODEL = 'users.User'
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        # TODO: Re-enable this.
        #'allauth.account.auth_backends.AuthenticationBackend',
    ]
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.Argon2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
        'django.contrib.auth.hashers.BCryptPasswordHasher',
    ]
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6, }},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
    ]
    LOGIN_REDIRECT_URL = 'users:redirect'
    LOGIN_URL = 'login'

    # EMAIL SETTINGS
    # --------------------------------------------------------------------------
    DEFAULT_FROM_EMAIL = values.Value('SME Virtual Network <hello@smevirtual.com>')
    EMAIL_SUBJECT_PREFIX = values.Value('[SME Virtual Network]')
    EMAIL_USE_TLS = values.BooleanValue(True)
    SERVER_EMAIL = values.Value(DEFAULT_FROM_EMAIL)

    # DATABASE SETTINGS
    # --------------------------------------------------------------------------
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': values.Value('',
                                 environ_name='DATABASE_NAME_DEFAULT',
                                 environ_required=True),
            'USER': values.Value('',
                                 environ_name='DATABASE_USER_DEFAULT',
                                 environ_required=True),
            'PASSWORD': values.SecretValue(environ_name='DATABASE_PASSWORD_DEFAULT'),
            'HOST': values.Value('',
                                 environ_name='DATABASE_HOST_DEFAULT',
                                 environ_required=True),
            'PORT': values.Value('5432',
                                 environ_name='DATABASE_PORT_DEFAULT'),
            'ATOMIC_REQUESTS': True,
            'CONN_MAX_AGE': 10
        }
    }

    # TEMPLATE SETTINGS
    # --------------------------------------------------------------------------
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                str(APPS_ROOT_DIR.path('templates')),
            ],
            'OPTIONS': {
                'debug': DEBUG,
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
                'context_processors': [
                    'aperte.base.context_processors.site_settings',
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.request',
                ],
            },
        },
    ]
    CSRF_FAILURE_VIEW = 'aperte.base.views.render_csrf_failure'

    # STATIC FILE SETTINGS
    # --------------------------------------------------------------------------
    # STATIC_ROOT - The absolute path to the directory where `collectstatic`
    # will collect static files for deployment. This is only used during
    # production (not development).
    STATIC_ROOT = str(REPO_ROOT_DIR.path('static'))
    # STATICFILES_DIRS - This setting defines the additional locations the
    # 'staticfiles' app will traverse if the 'FileSystemFinder' finder is
    # enabled.
    STATICFILES_DIRS = (
        str(APPS_ROOT_DIR.path('dist')),
    )
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    if env.bool('DJANGO_DISABLE_WHITENOISE', default=False):
        # Whitenoise is disabled.
        # This branch is for a local development where `collectstatic` will not
        # be called any time the styles or scripts are changed. This makes
        # development faster as the browser can refresh with the latest builds
        # of the styles and/or scripts without having to call `collectstatic`
        # first.
        STATIC_URL = '/static/'
    else:
        # Whitenoise is enabled.
        # This branch is for a local development environment which enables
        # Whitenoise to test a staging or production environment before pushing
        # the code to the cloud.
        INSTALLED_APPS = INSTALLED_APPS + ['whitenoise.runserver_nostatic',]
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        STATIC_HOST = values.URLValue('', environ_name='STATIC_HOST', environ_required=True)
        STATIC_URL = str(STATIC_HOST) + '/static/'

    # django-sites SETTINGS
    # --------------------------------------------------------------------------
    # Note: Default setting is 'https' for security reasons. For development,
    #       the setting will likely have to be 'http'.
    SITE_SCHEME = values.Value('https')
    SITE_DOMAIN = values.Value('',
                               environ_name='SITE_DOMAIN',
                               environ_required=True)
    SITE_NAME = values.Value('SME Virtual Network')
    SITES = {
        'current': {
            'domain': SITE_DOMAIN,
            'scheme': SITE_SCHEME,
            'name': SITE_NAME
        },
    }
    SITE_ID = 'current'

    # MEDIA SETTINGS
    # --------------------------------------------------------------------------
    MEDIA_ROOT = str(REPO_ROOT_DIR.path('.media'))
    MEDIA_URL = values.Value('{}://{}/media/'.format(SITE_SCHEME, SITE_DOMAIN))

    # SECURITY SETTINGS
    # --------------------------------------------------------------------------
    SECRET_KEY = values.SecretValue()
    CSRF_COOKIE_HTTPONLY = False
    SESSION_COOKIE_HTTPONLY = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

    # django-log-request-id SETTINGS
    # --------------------------------------------------------------------------
    REQUEST_ID_RESPONSE_HEADER = 'REQUEST_ID'

    # LOGGING SETTINGS
    # --------------------------------------------------------------------------
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'request_id': {
                '()': 'log_request_id.filters.RequestIDFilter'
            }
        },
        'formatters': {
            'complete': {
                'format': '%(asctime)s:[%(levelname)s]:logger=%(name)s:request_id=%(request_id)s message="%(message)s"'
            },
            'simple': {
                'format': '%(levelname)s:%(asctime)s: %(message)s'
            },
            'null': {
                'format': '%(message)s',
            },
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'complete',
                'filters': ['request_id'],
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'formatter': 'complete',
                'filters': ['request_id'],
            },
        },
        'loggers': {
            'django': {
                'handlers': ['null'],
                'propagate': False,
                'level': 'INFO',
            },
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.server': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'hello_world': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            '': {
                'handlers': [
                    'console',
                    'sentry'
                ],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

    # MIDDLEWARE SETTINGS
    # --------------------------------------------------------------------------
    MIDDLEWARE = [
        # TODO: Re-enable this.
        # 'corsheaders.middleware.CorsMiddleware',
        'log_request_id.middleware.RequestIDMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    # CACHE SETTINGS
    # --------------------------------------------------------------------------
    # See https://cloud.google.com/appengine/docs/flexible/java/upgrading#memcache_service
    # See https://cloud.google.com/appengine/docs/flexible/python/using-redislabs-memcache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': values.Value('',
                                     environ_name='CACHE_URL_DEFAULT',
                                     environ_required=True),
            'OPTIONS': {
                'BINARY': True,
                'USERNAME': values.Value('',
                                         environ_name='CACHE_USERNAME_DEFAULT',
                                         environ_required=True),
                'PASSWORD': values.SecretValue(environ_name='CACHE_PASSWORD_DEFAULT'),
            }
        }
    }

    # django-allauth SETTINGS
    # --------------------------------------------------------------------------
    ACCOUNT_ALLOW_REGISTRATION = True
    ACCOUNT_AUTHENTICATION_METHOD = 'username'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_ADAPTER = 'aperte.users.adapters.AccountAdapter'
    SOCIALACCOUNT_ADAPTER = 'aperte.users.adapters.SocialAccountAdapter'

    # raven SETTINGS
    # --------------------------------------------------------------------------
    RELEASE_VERSION = get_release()
    SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'
    RAVEN_CONFIG = {
        'dsn': values.Value('', environ_name='SENTRY_DSN'),
        'environment': values.Value('production', environ_name='SENTRY_ENVIRONMENT'),
        'release': RELEASE_VERSION,
    }

    SITE_INFO = {
        'RELEASE_VERSION': RELEASE_VERSION,
        'IS_RAVEN_INSTALLED': RAVEN_CONFIG['dsn'] is not ''
    }
