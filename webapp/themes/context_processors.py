from django.conf import settings

def theme(request):
    return {
        'THEME_UPLOAD': f'{settings.MEDIA_URL}{request.site.subdomain}/themes/{request.site.theme}',
    }
