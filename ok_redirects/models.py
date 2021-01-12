from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import pgettext_lazy

from .constants import REDIRECT_TYPE_CHOICES, REDIRECT_301
from .fields import MultipleChoiceArrayField

__all__ = (
    'Redirect',
)

LANGUAGES = getattr(settings, 'LANGUAGES', [])


class Redirect(models.Model):
    site = models.ForeignKey(
        Site,
        models.CASCADE,
        verbose_name=pgettext_lazy("ok:redirects", 'site')
    )
    old_path = models.CharField(
        pgettext_lazy("ok:redirects", 'redirect from'),
        max_length=250,
        db_index=True,
        help_text=pgettext_lazy(
            "ok:redirects",
            "This should be an absolute path, "
            "excluding the domain name. Example: '/events/search/'."
        ),
    )
    languages = MultipleChoiceArrayField(
        models.CharField(
            max_length=2,
            choices=LANGUAGES,
            blank=True
        ),
        blank=True,
        default=[lang[0] for lang in LANGUAGES] if LANGUAGES else list,
        verbose_name=pgettext_lazy("ok:redirects", "Languages to check redirect")
    )
    is_ignore_get_params = models.BooleanField(
        pgettext_lazy("ok:redirects", 'Ignore GET parameters'),
        default=True
    )
    new_path = models.CharField(
        pgettext_lazy("ok:redirects", 'redirect to'),
        blank=True,
        max_length=250,
        help_text=pgettext_lazy(
            "ok:redirects",
            "This can be either an absolute path (as above) "
            "or a full URL starting with 'http://'."
        ),
    )
    to_language = models.CharField(
        pgettext_lazy("ok:redirects", 'to language'),
        blank=True,
        choices=LANGUAGES,
        max_length=5,
        help_text=pgettext_lazy(
            "ok:redirects",
            "Leave blank to redirect to the current language on the site"
        ),
    )
    status_code = models.PositiveSmallIntegerField(
        db_index=True,
        choices=REDIRECT_TYPE_CHOICES,
        default=REDIRECT_301,
        verbose_name=pgettext_lazy("ok:redirects", 'Status code'),
        help_text=pgettext_lazy(
            "ok:redirects",
            'The redirect http status code.'
        )
    )
    counter = models.PositiveIntegerField(
        blank=True,
        default=0,
        verbose_name=pgettext_lazy("ok:redirects", 'Counter'),
    )
    is_active = models.BooleanField(
        pgettext_lazy("ok:redirects", 'Is active'),
        default=True,
        db_index=True,
    )

    class Meta:
        db_table = 'ok_redirects'
        ordering = ('old_path',)
        unique_together = (('site', 'old_path'),)
        verbose_name = pgettext_lazy("ok:redirects", 'redirect')
        verbose_name_plural = pgettext_lazy("ok:redirects", 'redirects')

    def __str__(self):
        return (
            f"{pgettext_lazy('ok:redirects', 'Redirect')} "
            f"{self.status_code}: "
            f"`{self.old_path}` ---> `{self.new_path}`"
        )
