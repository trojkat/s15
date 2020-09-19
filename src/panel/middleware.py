from django.utils.translation import activate

class ActiveMenu:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        activate(request.site.language)
        menu_active = None
        if request.path.startswith('/panel/'):
            menu_active = request.path.split('/')[2]
        request.menu_active = menu_active
        return self.get_response(request)
