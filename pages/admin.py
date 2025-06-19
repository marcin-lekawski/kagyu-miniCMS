# pages/admin.py
# w pliku: pages/admin.py

from django.contrib import admin
from .models import Page
from tinymce.widgets import TinyMCE
from django import forms

class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Page
        fields = '__all__'

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    list_display = ('title', 'slug', 'is_published', 'order', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', 'title')

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content')
        }),
        ('Obrazy', {
            'fields': ('header_image', 'thumbnail', 'thumbnail_size', 'thumbnail_custom_width', 'thumbnail_alignment'),
            'description': "Opcjonalne obrazy dla strony.",
            'classes': ('collapse',),
        }),
        ('Ustawienia Strony', {
            'fields': ('is_published', 'order'),
            'classes': ('collapse',),
        }),
    )

    class Media:
        js = ('js/admin_thumbnail_toggle.js',)