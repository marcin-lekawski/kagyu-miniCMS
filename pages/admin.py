# pages/admin.py
from django.contrib import admin
from .models import Page
from tinymce.widgets import TinyMCE # Jeśli używasz TinyMCE dla treści
from django import forms # Potrzebne do formularza TinyMCE

class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Page
        fields = '__all__'

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm # Przypisz formularz z TinyMCE
    list_display = ('title', 'slug', 'is_published', 'order', 'updated_at') # Dodano 'is_published' i 'order'
    list_filter = ('is_published',) # Pozwoli filtrować po statusie publikacji
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', 'title') # Sortowanie w panelu admina po kolejności i tytule

    # Opcjonalnie: fieldsets do lepszej organizacji formularza edycji
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'header_image')
        }),
        ('Ustawienia Strony', {
            'fields': ('is_published', 'order'),
            'classes': ('collapse',), # Zwijany panel dla tych ustawień
        }),
    )