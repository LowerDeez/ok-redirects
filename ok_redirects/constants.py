from django.utils.translation import pgettext_lazy

from .responses import (
    HttpResponsePermanentRedirect,
    HttpResponseTemporaryRedirect,
    HttpResponseSeeOtherRedirect,
    HttpResponseStrictTemporaryRedirect,
    HttpResponseStrictPermanentRedirect
)

__all__ = (
    'REDIRECT_301',
    'REDIRECT_302',
    'REDIRECT_303',
    'REDIRECT_307',
    'REDIRECT_308',
    'REDIRECT_TYPE_CHOICES',
    'REDIRECT_RESPONSE_CLASSES'
)

REDIRECT_301 = 301
REDIRECT_302 = 302
REDIRECT_303 = 303
REDIRECT_307 = 307
REDIRECT_308 = 308

REDIRECT_TYPE_CHOICES = (
    (REDIRECT_301, pgettext_lazy("ok:redirects", '301 Moved Permanently')),
    (REDIRECT_302, pgettext_lazy("ok:redirects", '302 Found')),
    (REDIRECT_303, pgettext_lazy("ok:redirects", '303 See Other')),
    (REDIRECT_307, pgettext_lazy("ok:redirects", '307 Temporary Redirect')),
    (REDIRECT_308, pgettext_lazy("ok:redirects", '308 Permanent Redirect')),
)

REDIRECT_RESPONSE_CLASSES = {
    REDIRECT_301: HttpResponsePermanentRedirect,
    REDIRECT_302: HttpResponseTemporaryRedirect,
    REDIRECT_303: HttpResponseSeeOtherRedirect,
    REDIRECT_307: HttpResponseStrictTemporaryRedirect,
    REDIRECT_308: HttpResponseStrictPermanentRedirect,
}
