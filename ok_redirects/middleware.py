from typing import TYPE_CHECKING

from django.apps import apps
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin

from .conf import (
    REDIRECTS_IGNORE_PATH_PREFIXES,
)
from .recievers import get_redirect
from .services import (
    increase_redirect_counter,
    get_redirect_response
)

if TYPE_CHECKING:
    from django.contrib.sites.models import Site
    from django.http.response import HttpResponse
    from .models import Redirect


__all__ = (
    'RedirectMiddleware',
)


class RedirectMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        if not apps.is_installed('django.contrib.sites'):
            raise ImproperlyConfigured(
                "You cannot use RedirectMiddleware when "
                "django.contrib.sites is not installed."
            )
        super().__init__(get_response)

    def process_response(self, request, response) -> 'HttpResponse':
        path: str = request.path

        if isinstance(REDIRECTS_IGNORE_PATH_PREFIXES, str):
            ignore_prefixes = (REDIRECTS_IGNORE_PATH_PREFIXES, )
        else:
            ignore_prefixes = tuple(REDIRECTS_IGNORE_PATH_PREFIXES)

        if path.startswith(ignore_prefixes):
            return response

        full_path: str = request.get_full_path()
        current_site: 'Site' = get_current_site(request)

        r: 'Redirect' = get_redirect(site=current_site, old_path=path)

        if r:
            if request.GET and not r.is_ignore_get_params:
                r = None

        if r is None:
            r: 'Redirect' = get_redirect(site=current_site, old_path=full_path)

        if r is None and settings.APPEND_SLASH and not request.path.endswith('/'):
            r: 'Redirect' = (
                get_redirect(
                    site=current_site,
                    old_path=request.get_full_path(force_append_slash=True)
                )
            )

        if r is not None:
            increase_redirect_counter(redirect=r)
            return get_redirect_response(redirect=r)

        # No redirect was found. Return the response.
        return response
