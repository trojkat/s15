import json
import os

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

from themes.models import ThemeSettings
from themes.utils import get_theme, get_themes_names


class Site(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subdomain = models.CharField(max_length=50)
    domain = models.CharField(null=True, blank=True, max_length=50)
    theme = models.CharField(max_length=50, choices=get_themes_names())
    active = models.BooleanField(default=True)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES)

    def __str__(self):
        return self.subdomain

    def get_absolute_url(self) -> str:
        return f'http://{self.subdomain}.localhost:8000'

    @property
    def settings(self) -> dict:
        try:
            return json.loads(self.theme_settings.get(theme=self.theme).values)
        except ThemeSettings.DoesNotExist:
            # getting default values from the theme config
            theme = get_theme(self.theme, self.language)
            return {setting.id: setting.default for setting in theme.settings}

    @property
    def upload_folder(self) -> str:
        return os.path.join(settings.MEDIA_ROOT, self.subdomain)

    def remove_theme_image(self, field_name: str) -> None:
        image_name = self.settings[field_name]
        os.remove(os.path.join(self.upload_folder, 'themes', self.theme, image_name))
