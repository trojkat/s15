import json

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, FormView, ProcessFormView, UpdateView
from django.urls import reverse

from page.models import Page
from themes.utils import get_themes, get_theme
from themes.forms import ThemeSettingsForm
from themes.models import ThemeSettings


def login(request):
    if request.method == "POST":
        return redirect('dashboard')
    return render(request, 'panel/login.html')


class PageList(LoginRequiredMixin, ListView, ProcessFormView):
    context_object_name = 'pages'
    template_name = 'panel/pages.html'

    def get_queryset(self):
        return Page.objects.filter(site=self.request.site).values(
            'id',
            'title',
            'slug',
            'public',
            'start_page',
            'insert_date',
            'update_date',
        )

    def post(self, request):
        request.site.pages.update(start_page=False)
        request.site.pages.filter(id=request.POST['start_page']).update(start_page=True)
        messages.success(self.request, 'Nowa strona główna została ustawiona.')
        return HttpResponseRedirect(reverse('pages'))


class PageOrderChange(LoginRequiredMixin, ProcessFormView):

    def post(self, request):
        new_order = map(int, request.POST['new_order'].split(','))
        my_pages = request.site.pages.values_list('id', flat=True)
        for index, page_id in enumerate(new_order):
            if page_id not in my_pages:
                continue
            request.site.pages.filter(id=page_id).update(order=index)
        return HttpResponse(status=204)


class PageCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Page
    fields = ['title', 'slug', 'body', 'public']
    template_name = 'panel/page-update.html'
    success_message = "Strona %(title)s została dodana"

    def get_success_url(self):
        return reverse('pages')

    def form_valid(self, form):
        form.instance.site = self.request.site
        return super().form_valid(form)


class PageUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Page
    fields = ['title', 'slug', 'body', 'public']
    template_name = 'panel/page-update.html'
    success_message = "Strona %(title)s została zaktualizowana"

    def get_success_url(self):
        return reverse('pages')


class ImageUpload(LoginRequiredMixin, ProcessFormView):

    def post(self, request):
        myfile = request.FILES['image']
        fs = FileSystemStorage(
            location=request.site.upload_folder,
            base_url=f'{settings.MEDIA_URL}{request.site.subdomain}',
        )
        filename = fs.save(myfile.name, myfile)
        return JsonResponse({
            'data': {
                'filePath': fs.url(filename)
            }
        })


class PageDeleteView(DeleteView):
    model = Page
    template_name = "panel/page-delete.html"

    def get_success_url(self):
        return reverse('pages')


class ThemeList(LoginRequiredMixin, TemplateView):
    template_name = 'panel/themes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['themes'] = get_themes()
        return context


class ThemeDetails(LoginRequiredMixin, ProcessFormView, TemplateView):
    template_name = 'panel/theme.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = get_theme(self.kwargs['slug'], self.request.site.language)
        return context

    def post(self, request, slug):
        self.request.site.theme = slug
        self.request.site.save()
        messages.success(self.request, "Skróka została zmieniona.")
        return HttpResponseRedirect(reverse('theme-settings'))


class ThemeSettingsEditor(LoginRequiredMixin, FormView):
    template_name = 'panel/theme-settings.html'
    form_class = ThemeSettingsForm
    REMOVE_CHECKBOX_POSTFIX = '_remove_image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = get_theme(self.request.site.theme, self.request.site.language)
        context['remove_checkbox_postfix'] = self.REMOVE_CHECKBOX_POSTFIX
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['settings'] = get_theme(self.request.site.theme, self.request.site.language).settings
        kwargs['current_settings'] = self.request.site.settings
        return kwargs

    def post(self, request):
        theme = get_theme(self.request.site.theme, self.request.site.language)
        updated_settings = {}
        for field in request.POST:
            if field == 'csrfmiddlewaretoken':
                continue
            if field.endswith(self.REMOVE_CHECKBOX_POSTFIX):
                continue
            if field in theme.image_fields and not request.POST[field]:
                remove_checkbox_name = f'{field}{self.REMOVE_CHECKBOX_POSTFIX}'
                if remove_checkbox_name in request.POST:
                    # Image removal request
                    updated_settings[field] = ''
                    request.site.remove_theme_image(field)
                    continue
                # Image field is empty - keeping the current value
                updated_settings[field] = request.site.settings.get(field)
            else:
                updated_settings[field] = request.POST[field]
        for file_field in request.FILES:
            file = request.FILES[file_field]
            fs = FileSystemStorage(
                location=f'{request.site.upload_folder}/themes/{request.site.theme}',
                base_url=f'{settings.MEDIA_URL}{request.site.subdomain}',
            )
            filename = fs.save(file.name, file)
            updated_settings[file_field] = filename
        site_settings, _ = self.request.site.theme_settings.get_or_create(theme=self.request.site.theme)
        site_settings.values = json.dumps(updated_settings)
        site_settings.save()
        messages.success(self.request, 'Ustawienia zostały zapisane.')
        return HttpResponseRedirect(reverse('theme-settings'))
