from django.apps import AppConfig


class DomainConfig(AppConfig):
    name = 'domain'

    def ready(self):
        from . import signals
