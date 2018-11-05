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
"""Root URL routings.
"""
# pylint: disable=C0103

# Third Party
from django.conf import settings
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from .base import views as base_views

admin.site.site_title = admin.site.site_header = 'Aperte Administration'

# TOP-LEVEL URLs
# ------------------------------------------------------------------------------
urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='pages/home.html'), name='home'),
    # Django administration.
    url(r'^{}/'.format(settings.ADMIN_URL), admin.site.urls),
    # TODO: Re-enable this.
    # url(r'^accounts/', include('allauth.urls')),
]

urlpatterns += [
    # Top-level URLs for search engines.
    url(r'^(?P<template_name>(robots.txt))$',
        base_views.render_text_files, name='root-txt-files'),

    # Django Admin URL.
    url(r'^{}/'.format(settings.ADMIN_URL), admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.views import defaults as dj_default_views
    from django.urls import get_callable

    # ERROR URLs
    # --------------------------------------------------------------------------
    urlpatterns += [
        url(r'^400/$',
            dj_default_views.bad_request,
            kwargs={'exception': Exception('Bad Request.')}),
        url(r'^403/$',
            dj_default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied.')}),
        url(r'^403_csrf/$',
            get_callable(settings.CSRF_FAILURE_VIEW)),
        url(r'^404/$',
            dj_default_views.page_not_found,
            kwargs={'exception': Exception('Page Not Found.')}),
        url(r'^500/$',
            dj_default_views.server_error),
    ]

    # django-debug-toolbar URLs
    # --------------------------------------------------------------------------
    try:
        import debug_toolbar
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass

    # devrecargar URLs
    # --------------------------------------------------------------------------
    try:
        from devrecargar.urls import urlpatterns as devrecargar_urls
        urlpatterns += [
            url(r'^devrecargar/',
                include((devrecargar_urls, 'devrecargar', ), namespace='devrecargar'))
        ]
    except ImportError:
        pass
