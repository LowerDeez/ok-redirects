from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = (
    'Redirect',
)


class Redirect(models.Model):
    site = models.ForeignKey(
        Site,
        models.CASCADE,
        verbose_name=_('site')
    )
    old_path = models.CharField(
        _('redirect from'),
        max_length=250,
        db_index=True,
        help_text=_(
            "This should be an absolute path, "
            "excluding the domain name. Example: '/events/search/'."
        ),
    )
    is_ignore_get_params = models.BooleanField(
        _('Ignore GET parameters'),
        default=True
    )
    new_path = models.CharField(
        _('redirect to'),
        max_length=250,
        blank=True,
        help_text=_(
            "This can be either an absolute path (as above) "
            "or a full URL starting with 'http://'."
        ),
    )
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _('redirect')
        verbose_name_plural = _('redirects')
        db_table = 'ok_redirects'
        unique_together = (('site', 'old_path'),)
        ordering = ('old_path',)

    def __str__(self):
        return f"`{self.old_path}` ---> `{self.new_path}`"
