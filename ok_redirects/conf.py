from typing import Tuple, Union

from django.conf import settings

__all__ = (
    'REDIRECTS_IGNORE_PATH_PREFIXES',
)


REDIRECTS_IGNORE_PATH_PREFIXES: Union[Tuple, str] = getattr(
    settings,
    'REDIRECTS_IGNORE_PATH_PREFIXES',
    ()
)
