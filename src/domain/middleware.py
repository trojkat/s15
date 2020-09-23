from django.conf import settings
from django.http import Http404

from .models import Site


class DomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if settings.DEBUG:
            host = host.split(':')[0]
        supported_domains = settings.SUPPORTED_DOMAINS
        site = None
        for domain in supported_domains:
            if host.endswith(domain):
                subdomain = host.split('.')[0]
                try:
                    site = Site.objects.get(subdomain=subdomain)
                except:
                    pass
                break
        if site is None and not request.path.startswith(f'/{settings.ADMIN_PANEL_PATH_NAME}/'):
            raise Http404()
        request.site = site
        return self.get_response(request)
