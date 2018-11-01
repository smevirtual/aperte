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
"""Django settings for project development environments. These settings are
intended to be used with deploying this project into a Docker container.
"""
# pylint: disable=C0111,W0232

# Standard Library
import environ
import socket

# Third Party
from configurations import values

from .common import Common


class Development(Common):
    # See https://docs.djangoproject.com/en/2.0/ref/settings/ for a description
    # of each Django setting.

    env = environ.Env()

    # CORE SETTINGS
    # --------------------------------------------------------------------------
    DEBUG = values.BooleanValue(True)
    INTERNAL_IPS = [
        '127.0.0.1',
        '10.0.2.2',
    ]

    # INSTALLED APPS SETTINGS
    # --------------------------------------------------------------------------
    Common.INSTALLED_APPS += [
        'django_extensions',
        'devrecargar',
        'debug_toolbar',
    ]

    # MIDDLEWARE SETTINGS
    # --------------------------------------------------------------------------
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + Common.MIDDLEWARE

    # EMAIL SETTINGS
    # --------------------------------------------------------------------------
    MAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # django-cors-headers SETTINGS
    # --------------------------------------------------------------------------
    # TODO: Re-enable this.
    # CORS_ORIGIN_WHITELIST = []

    # django-debug-toolbar SETTINGS
    # --------------------------------------------------------------------------
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }

    if env.bool('DJANGO_USE_DOCKER', default=True):
        # This is required for the 'django-debug-toolbar' to work with Docker.
        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
        INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]

    # devrecargar SETTINGS
    # --------------------------------------------------------------------------
    DEVRECARGAR_PATHS_TO_WATCH = [{
        'path': str(Common.APPS_ROOT_DIR),
        'patterns': ['*.html', '*.js', '*.css'],
    }]
