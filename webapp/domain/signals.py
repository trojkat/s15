from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Site


@receiver(post_save, sender=Site)
def add_main_page(sender, instance, created, **kwargs):
    if not created:
        return
    instance.pages.create(title='start', slug='start', body='start', start_page=True)
