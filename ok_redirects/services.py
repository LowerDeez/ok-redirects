from typing import TYPE_CHECKING

from django.conf import settings
from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.db.models import F
from django.utils.translation import get_language_from_path

from .constants import REDIRECT_RESPONSE_CLASSES
from .responses import HttpResponseGone

if TYPE_CHECKING:
    from django.http.response import HttpResponse
    from .models import Redirect

__all__ = (
    'get_redirect_response',
    'increase_redirect_counter'
)

LANGUAGE_CODE = getattr(settings, 'LANGUAGE_CODE', None)


def get_prefixed_default_language(*, request):
    urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
    i18n_patterns_used, prefixed_default_language = (
        is_language_prefix_patterns_used(urlconf)
    )
    return prefixed_default_language


def get_redirect_response(
        *, redirect: 'Redirect', request, response
) -> 'HttpResponse':
    language_code: str = getattr(request, 'LANGUAGE_CODE', None)
    path_to_redirect = redirect.new_path

    if path_to_redirect == '':
        return HttpResponseGone()

    if redirect.to_language:
        language_code = redirect.to_language

    if language_code:
        is_default_language = language_code == LANGUAGE_CODE
        prefixed_default_language = get_prefixed_default_language(request=request)

        if not (is_default_language and not prefixed_default_language):
            path_to_redirect = f'/{language_code}{path_to_redirect}'

    # same paths
    if (
            request.path_info == path_to_redirect
            and get_language_from_path(request.path_info) == redirect.to_language
    ):
        return response

    return REDIRECT_RESPONSE_CLASSES[redirect.status_code](path_to_redirect)


def increase_redirect_counter(*, redirect: 'Redirect'):
    redirect.counter = F('counter') + 1
    redirect.save(update_fields=['counter'])
