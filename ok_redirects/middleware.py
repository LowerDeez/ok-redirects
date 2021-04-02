import re
from typing import Optional, TYPE_CHECKING

from django.apps import apps
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import is_valid_path
from django.utils.deprecation import MiddlewareMixin

from .conf import (
    REDIRECTS_IGNORE_PATH_PREFIXES,
)
from .recievers import get_redirect
from .services import (
    increase_redirect_counter,
    get_redirect_response
)
from .utils import strip_language_from_path

if TYPE_CHECKING:
    from django.contrib.sites.models import Site
    from django.http.response import HttpResponse
    from .models import Redirect


__all__ = (
    'RedirectMiddleware',
    'extra_slashes_redirect_middleware'
)

REDIRECTS_EXTRA_SLASHES_REDIRECT_EXEMPT_URLS = []

if hasattr(settings, 'REDIRECTS_EXTRA_SLASHES_REDIRECT_EXEMPT_URLS'):
    REDIRECTS_EXTRA_SLASHES_REDIRECT_EXEMPT_URLS += [
        re.compile(url)
        for url in settings.REDIRECTS_EXTRA_SLASHES_REDIRECT_EXEMPT_URLS
    ]


class RedirectMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        if not apps.is_installed('django.contrib.sites'):
            raise ImproperlyConfigured(
                "You cannot use RedirectMiddleware when "
                "django.contrib.sites is not installed."
            )
        super().__init__(get_response)

    def process_response(self, request, response) -> 'HttpResponse':
        language_code: str = getattr(request, 'LANGUAGE_CODE', None)
        path: str = strip_language_from_path(path=request.path)

        if isinstance(REDIRECTS_IGNORE_PATH_PREFIXES, str):
            ignore_prefixes = (REDIRECTS_IGNORE_PATH_PREFIXES, )
        else:
            ignore_prefixes = tuple(REDIRECTS_IGNORE_PATH_PREFIXES)

        if path.startswith(ignore_prefixes):
            return response

        current_site: 'Site' = get_current_site(request)

        r: Optional['Redirect'] = (
            get_redirect(site=current_site, old_path=path)
        )

        if r:
            if request.GET and not r.is_ignore_get_params:
                r = None

        if r is None:
            full_path: str = (
                strip_language_from_path(
                    path=request.get_full_path()
                )
            )
            r: 'Redirect' = (
                get_redirect(site=current_site, old_path=full_path)
            )

        if (
                r is None
                and settings.APPEND_SLASH
                and not request.path.endswith('/')
        ):
            r: 'Redirect' = (
                get_redirect(
                    site=current_site,
                    old_path=request.get_full_path(force_append_slash=True)
                )
            )

        if r is not None:
            if (
                    language_code is not None
                    and r.languages
                    and language_code not in r.languages
            ):
                return response

            increase_redirect_counter(redirect=r)

            return (
                get_redirect_response(
                    redirect=r,
                    request=request,
                    response=response
                )
            )

        # No redirect was found. Return the response.
        return response


def extra_slashes_redirect_middleware(get_response):
    """
    Middleware to redirect from urls with extra slashes
    at the end to urls with one slash
    """
    def middleware(request):
        path = request.get_full_path()

        if '//' in path:
            path = re.sub(r'(/)\1+', r'\1', path)
            return redirect(path, permanent=True)

        if not settings.APPEND_SLASH:
            return get_response(request)

        is_url_exempt = any(
            url.match(path.lstrip('/'))
            for url in REDIRECTS_EXTRA_SLASHES_REDIRECT_EXEMPT_URLS
        )

        if is_url_exempt:
            return get_response(request)

        is_url_to_redirect = all([
            not request.GET,
            len(path) > 1,
            not str(path).endswith('/')
        ])

        if is_url_to_redirect:
            urlconf = getattr(request, 'urlconf', None)

            # if path without slash is not valid - append slash
            if not is_valid_path(path, urlconf):
                path += '/'

            if is_valid_path(path, urlconf):
                return redirect(path, permanent=True)

        if path.endswith('?'):
            path = path[:-1]
            return redirect(path, permanent=True)

        return get_response(request)

    return middleware
