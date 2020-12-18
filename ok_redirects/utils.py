from django.conf import settings
from django.utils.translation.trans_real import language_code_prefix_re

__all__ = (
    'strip_language_from_path',
)


def strip_language_from_path(
        path: str
) -> str:
    """
    Return current path from request, excluding language code
    """
    regex_match = language_code_prefix_re.match(path)

    if regex_match:
        lang_code = regex_match.group(1)
        languages = [
            language_tuple[0] for
            language_tuple in settings.LANGUAGES
        ]

        if lang_code in languages:
            path = path[1 + len(lang_code):]

            if not path.startswith('/'):
                path = '/' + path

    return path
