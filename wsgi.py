"""WSGI configuration for the project.
"""
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
# pylint: disable=C0103

# Standard Library
import os
import sys

# Third Party
from configurations.wsgi import get_wsgi_application

app_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.append(os.path.join(app_path, 'aperte'))

if os.environ.get('DJANGO_CONFIGURATION') == 'Production':
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Production')

application = get_wsgi_application()

if os.environ.get('DJANGO_CONFIGURATION') == 'Production':
    application = Sentry(application)
