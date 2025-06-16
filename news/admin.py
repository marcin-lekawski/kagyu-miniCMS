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
    list_display = ('title', 'published_date', 'is_published', 'is_pinned', 'updated_at') # Dodano 'is_published', 'is_pinned'
    list_filter = ('is_published', 'is_pinned', 'published_date') # Dodano filtry dla nowych pól
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date' # Używamy published_date
    ordering = ('-published_date',) # Domyślne sortowanie w adminie

    # Opcjonalnie: fieldsets do lepszej organizacji formularza edycji
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'thumbnail', 'content')
        }),
        ('Ustawienia Publikacji', {
            'fields': ('published_date', 'is_published', 'is_pinned'),
            'classes': ('collapse',), # Zwijany panel dla tych ustawień
        }),
    )