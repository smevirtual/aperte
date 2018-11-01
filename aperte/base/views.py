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
"""Base views.
"""

# Third Party
from django.conf import settings
from django.shortcuts import render


def render_csrf_failure(request, reason: str = '', template_name: str = '403_csrf.html'):
    """
    View for rendering CSRF verification failures.

    Parameters
    ----------
    request
        The request object used to generate this response.
    reason
        The reason constant from `django.middleware.csrf` as to why the CSRF
        verification failed.
    template_name
        The full name of the template to render.

    Returns
    -------
    django.http.HttpResponse
        A `HttpResponse` object with the rendered text.
    """
    from django.middleware.csrf import REASON_NO_REFERER, REASON_NO_CSRF_COOKIE
    context = {
        'reason': reason,
        'no_referer': reason == REASON_NO_REFERER,
        'no_cookie': reason == REASON_NO_CSRF_COOKIE,
        'DEBUG': settings.DEBUG,
    }
    return render(request, template_name=template_name, context=context, status=403)


def render_text_files(request, template_name: str):
    """
    View for rendering text files.

    Parameters
    ----------
    request
        The request object used to generate this response.
    template_name
        The full name of the text file template to render.

    Returns
    -------
    django.http.HttpResponse
        A `HttpResponse` object with the rendered text.
    """
    return render(request, template_name, {}, content_type='text/plain')
