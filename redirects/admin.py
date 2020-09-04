from django.contrib import admin

from .models import Redirect


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'site',
                ('old_path', 'is_ignore_get_params'),
                'new_path',
                'is_active'
            ),
        }),
    )
    list_display = (
        '__str__',
        'old_path',
        'new_path',
        'is_ignore_get_params',
        'is_active'
    )
    list_editable = (
        'old_path',
        'new_path',
        'is_ignore_get_params',
        'is_active'
    )
    list_filter = (
        'site',
    )
    search_fields = (
        'old_path',
        'new_path'
    )
    radio_fields = {'site': admin.VERTICAL}
