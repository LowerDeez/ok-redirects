from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Redirect


class RedirectValidationForm(forms.ModelForm):
    class Meta:
        model = Redirect
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        sites = cleaned_data["sites"]
        old_path = cleaned_data["old_path"]

        for site in sites:
            existing_redirects = Redirect.objects.filter(sites=site, old_path=old_path)

            if self.instance:
                existing_redirects = existing_redirects.exclude(pk=self.instance.pk)

            if existing_redirects.exists():
                raise forms.ValidationError(
                    {
                        "sites": _(
                            "Redirect for path `{path}` for site `{site}` already exists."
                        ).format(site=site, path=old_path),
                    }
                )

        return cleaned_data


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'is_active',
                'sites',
                'status_code',
                ('old_path', 'is_ignore_get_params'),
                'new_path',
                'to_language',
                'languages',
                'counter',
            ),
        }),
    )
    form = RedirectValidationForm
    list_display = (
        '__str__',
        'display_sites',
        'old_path',
        'is_ignore_get_params',
        'new_path',
        'is_active'
    )
    list_editable = (
        'old_path',
        'new_path',
        'is_ignore_get_params',
        'is_active'
    )
    list_filter = (
        'sites',
    )
    search_fields = (
        'old_path',
        'new_path'
    )
    readonly_fields = (
        'counter',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("sites")

    def display_sites(self, obj: "Redirect"):
        return mark_safe("<br>".join([str(site) for site in obj.sites.all()]))
    display_sites.short_description = _("Sites")
