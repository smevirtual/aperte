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
"""Django settings for project production environments. These settings are
intended to be used with deploying this project into a Docker container and
on a Google App Engine Flexible environment.
"""
# pylint: disable=C0111,W0232

# Third Party
from configurations import values

from .common import Common


class Production(Common):
    # See https://docs.djangoproject.com/en/2.0/ref/settings/ for a description
    # of each Django setting.

    # django-cors-headers SETTINGS
    # --------------------------------------------------------------------------
    # TODO: Re-enable this.
    # CORS_ORIGIN_WHITELIST = values.ListValue([], environ_required=True)

    # SECURITY SETTINGS
    # --------------------------------------------------------------------------
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
    SESSION_CACHE_ALIAS = 'default'
    if Common.SITE_SCHEME == 'https':
        # WARNING: Set this to 518400 (6 days) after the web application is
        # configured correctly to confidently serve HTTPS.
        SECURE_HSTS_SECONDS = values.IntegerValue(60)
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_SSL_REDIRECT = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True

    # MIDDLEWARE SETTINGS
    # --------------------------------------------------------------------------
    MIDDLEWARE = [
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
        'django_auth_wall.middleware.BasicAuthMiddleware',
    ] + Common.MIDDLEWARE

    # EMAIL SETTINGS
    # The settings below are suitable for using SendGrid's Web API for sending
    # email from Django.
    # --------------------------------------------------------------------------
    EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
    ANYMAIL = {
        'SENDGRID_API_KEY': values.Value('',
                                         environ_name='SENDGRID_API_KEY',
                                         environ_required=True),
    }

    # TEMPLATE SETTINGS
    # --------------------------------------------------------------------------
    Common.TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', Common.TEMPLATES[0]['OPTIONS']['loaders']),
    ]

    # INSTALLED APPS SETTINGS
    # --------------------------------------------------------------------------
    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'gunicorn',
        'anymail',
    ]
