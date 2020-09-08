from django.http.response import (
    HttpResponseRedirectBase,
    HttpResponseRedirect as HttpResponseTemporaryRedirect,
    HttpResponsePermanentRedirect,
    HttpResponseGone
)

__all__ = (
    'HttpResponsePermanentRedirect',
    'HttpResponseTemporaryRedirect',
    'HttpResponseSeeOtherRedirect',
    'HttpResponseStrictTemporaryRedirect',
    'HttpResponseStrictPermanentRedirect',
    'HttpResponseGone'
)


class HttpResponseSeeOtherRedirect(HttpResponseRedirectBase):
    status_code = 303


class HttpResponseStrictTemporaryRedirect(HttpResponseRedirectBase):
    status_code = 307


class HttpResponseStrictPermanentRedirect(HttpResponseRedirectBase):
    status_code = 308
