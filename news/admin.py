# news/admin.py
from django.contrib import admin
from .models import Article # Upewnij się, że importujesz model Article
from tinymce.widgets import TinyMCE
from django import forms

class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Article
        fields = '__all__'
        
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'published_date', 'is_published', 'is_pinned', 'pin_order', 'updated_at')
    # ... inne ustawienia listy bez zmian ...
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content')
        }),
        ('Miniatura', {
            'fields': ('thumbnail', 'thumbnail_size', 'thumbnail_custom_width', 'thumbnail_alignment'), # <-- Dodajemy nowe pole
            'description': "Opcjonalna miniatura wyświetlana na liście postów."
        }),
        ('Ustawienia Publikacji', {
            'fields': ('published_date', 'is_published', 'is_pinned', 'pin_order'),
            'classes': ('collapse',),
        }),
    )

    # NOWA SEKCJA: Dołączamy plik JS do strony edycji artykułu
    class Media:
        js = ('js/admin_thumbnail_toggle.js',)
