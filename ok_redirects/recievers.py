from typing import TYPE_CHECKING, Union

from .models import Redirect

if TYPE_CHECKING:
    from django.contrib.sites.models import Site

__all__ = (
    'get_redirect',
)


def get_redirect(
        *,
        site: 'Site',
        old_path: str
) -> Union['Redirect', None]:
    try:
        r = (
            Redirect.objects.get(
                site=site,
                old_path=old_path,
                is_active=True
            )
        )
    except Redirect.DoesNotExist:
        r = None
    return r
