from typing import TYPE_CHECKING

from django.db.models import F

from .constants import REDIRECT_RESPONSE_CLASSES
from .responses import HttpResponseGone

if TYPE_CHECKING:
    from django.http.response import HttpResponse
    from .models import Redirect

__all__ = (
    'get_redirect_response',
    'increase_redirect_counter'
)


def get_redirect_response(*, redirect: 'Redirect') -> 'HttpResponse':
    if redirect.new_path == '':
        return HttpResponseGone()

    return (
        REDIRECT_RESPONSE_CLASSES[redirect.status_code](
            redirect.new_path
        )
    )


def increase_redirect_counter(*, redirect: 'Redirect'):
    redirect.counter = F('counter') + 1
    redirect.save(update_fields=['counter'])
