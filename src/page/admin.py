from django.contrib import admin

from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'insert_date','site')
    list_filter = ('site', 'insert_date', 'update_date')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
