from django.db import models
from django.utils.safestring import mark_safe

import markdown


class Page(models.Model):
    site = models.ForeignKey('domain.Site', on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    insert_date = models.DateField(auto_now=False, auto_now_add=True)
    update_date = models.DateField(auto_now=True, auto_now_add=False)
    body = models.TextField()
    public = models.BooleanField(default=True)
    start_page = models.BooleanField(default=False)
    order = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = [['site', 'slug']]
        ordering = ('order', )

    def __str__(self):
        return self.title

    @property
    def markup(self):
        return mark_safe(markdown.markdown(self.body, extensions=['tables']))

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('page', kwargs={'slug': self.slug})
