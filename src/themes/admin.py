from django.contrib import admin

from .models import ThemeSettings


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ('site', 'theme')
