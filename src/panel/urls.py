from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('', views.PageList.as_view(), name='index'),
    path('pages', views.PageList.as_view(), name='pages'),
    path('pages/create', views.PageCreate.as_view(), name='page-create'),
    path('pages/change-order', views.PageOrderChange.as_view(), name='pages-change-order'),
    path('pages/<int:pk>', views.PageUpdate.as_view(), name='page-update'),
    path('pages/<int:pk>/delete', views.PageDeleteView.as_view(), name='page-delete'),
    path('themes', views.ThemeList.as_view(), name='themes'),
    path('themes/<slug:slug>', views.ThemeDetails.as_view(), name='theme'),
    path('theme-settings', views.ThemeSettingsEditor.as_view(), name='theme-settings'),
    path('image-upload', views.ImageUpload.as_view(), name='image-upload'),
    path('logowanie', auth_views.LoginView.as_view(template_name='panel/login.html'), name='login'),
    path('wyloguj', auth_views.LogoutView.as_view(), name='logout'),
]
