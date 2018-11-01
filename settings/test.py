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
"""Django settings for project test environments.
"""
# pylint: disable=C0111,W0232

from .development import Development


class Test(Development):
    # See https://docs.djangoproject.com/en/2.0/ref/settings/ for a description
    # of each Django setting.

    # CORE SETTINGS
    # --------------------------------------------------------------------------
    DEBUG = False
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'

    # MEDIA SETTINGS
    # --------------------------------------------------------------------------
    MEDIA_ROOT = '/tmp'

    # AUTHENTICATION AND LOGIN SETTINGS
    # --------------------------------------------------------------------------
    PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

    # SECURITY SETTINGS
    # --------------------------------------------------------------------------
    SECRET_KEY = 'TOP_SECRET'

    # CACHE SETTINGS
    # --------------------------------------------------------------------------
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': ''
        }
    }

    # EMAIL SETTINGS
    # --------------------------------------------------------------------------
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    # INSTALLED APPS SETTINGS
    # --------------------------------------------------------------------------
    INSTALLED_APPS = [
        'tests',
    ] + Development.INSTALLED_APPS
