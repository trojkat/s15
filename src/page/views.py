from django.shortcuts import render

from .models import Page


def view_page(request, slug=None):
    if not slug:
        page = request.site.pages.get(start_page=True)
    else:
        page = request.site.pages.get(slug=slug)
    return render(request, f'themes/{request.site.theme}/page.html', {
        'page': page,
        'pages': request.site.pages.filter(public=True).values('title', 'slug', 'start_page'),
        'settings': request.site.settings,
    })
