from django.conf import settings

__all__ = (
    'REDIRECTS_IGNORE_PATH_PREFIXES',
)

REDIRECTS_IGNORE_PATH_PREFIXES = getattr(
    settings,
    'REDIRECTS_IGNORE_PATH_PREFIXES',
    (
        '/api/v1/',
        '/uploads/',
        '/static/',
        '/vuejs-translate/',
        '/catalog/ajax/'
    )
)
