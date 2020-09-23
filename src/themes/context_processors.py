from django.conf import settings

def theme(request):
    if not request.site:
        return {}
    return {
        'THEME_UPLOAD': f'{settings.MEDIA_URL}{request.site.subdomain}/themes/{request.site.theme}',
    }
