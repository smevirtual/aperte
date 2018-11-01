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
"""Helpful URL utilities.
"""

# Third Party
import django_sites as sites
from django.urls import reverse as django_reverse

URL_TEMPLATE: str = '{scheme}://{domain}/{path}'


def build_absolute_url(scheme: str = 'http', domain: str = 'localhost', path: str = '/'):
    """
    Build absolute a URL from the scheme, domain and path.

    Parameters
    ----------
    scheme
        Scheme of the URL. By default, this is 'http'.
    domain
        Domain name of the URL. By default, this is 'localhost'.
    path
        Path of the URL. By default, this is '/'.

    Returns
    -------
    str
        The absolute URL.
    """
    return URL_TEMPLATE.format(scheme=scheme, domain=domain, path=path.lstrip('/'))


def is_absolute_url(path_or_url: str):
    """
    Checks if the provided string is a path or an absolute URL (prefixed by
    'http' or 'https').

    Parameters
    ----------
    path_or_url
        The path or URL to check.

    Returns
    -------
    bool
        True if the provided string is an absolute URL, False otherwise.
    """
    return path_or_url.startswith('http')


def get_absolute_url(path: str = '/', site_id: str = None):
    """
    Retrieve the absolute URL by incorporating the provided path with the site
    scheme and domain from the Django Sites settings.

    Parameters
    ----------
    path
        Path of the URL. By default, this is '/'.
    site_id
        Site ID string.

    Returns
    -------
    str
        The absolute URL.
    """
    if is_absolute_url(path):
        return path
    if site_id:
        site = sites.get_by_id(site_id)
    else:
        site = sites.get_current()
    return build_absolute_url(scheme=site.scheme, domain=site.domain, path=path)


def reverse(viewname: str, *args, **kwargs):
    """
    Retrieve the absolute URL from a provided viewname.

    Parameters
    ----------
    viewname
        The URL pattern name or a callable view object to reverse.

    Returns
    -------
    str
        The absolute URL.
    """
    return get_absolute_url(django_reverse(viewname, *args, **kwargs))
