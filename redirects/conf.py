from typing import Tuple, Union

from django.conf import settings

__all__ = (
    'REDIRECTS_IGNORE_PATH_PREFIXES',
    'REDIRECTS_USE_PERMANENT_REDIRECT'
)

REDIRECTS_IGNORE_PATH_PREFIXES: Union[Tuple, str] = getattr(
    settings,
    'REDIRECTS_IGNORE_PATH_PREFIXES',
    ()
)

REDIRECTS_USE_PERMANENT_REDIRECT: bool = getattr(
    settings,
    'REDIRECTS_USE_PERMANENT_REDIRECT',
    False
)
