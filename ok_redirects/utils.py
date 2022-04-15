from logging import getLogger

from django.conf import settings
from django.contrib.sites.models import Site
from django.http.request import HttpRequest
from django.utils.translation.trans_real import language_code_prefix_re

logger = getLogger(__name__)

__all__ = (
    'strip_language_from_path',
    'get_current_site',
)


def strip_language_from_path(path: str) -> str:
    """
    Return current path from request, excluding language code
    """
    regex_match = language_code_prefix_re.match(path)

    if regex_match:
        lang_code = regex_match.group(1)
        languages = [language_tuple[0] for language_tuple in settings.LANGUAGES]

        if lang_code in languages:
            path = path[1 + len(lang_code):]

            if not path.startswith('/'):
                path = '/' + path

    return path


def get_current_site(request: HttpRequest) -> 'Site':
    try:
        # try to find a site instance by current domain
        site: 'Site' = Site.objects._get_site_by_request(request=request)
    except Site.DoesNotExist:
        logger.warning(f"Site for host `{request.get_host()}` does not exist.")
        # fallback to return site by domain
        site: 'Site' = Site.objects.get_current(request)

    return site
