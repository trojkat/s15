from django.db import models

from .utils import get_themes_names


class ThemeSettings(models.Model):

    site = models.ForeignKey('domain.Site', on_delete=models.CASCADE, related_name='theme_settings')
    theme = models.CharField(max_length=50, choices=get_themes_names())
    values = models.TextField()

    class Meta:
        unique_together = [['site', 'theme']]
