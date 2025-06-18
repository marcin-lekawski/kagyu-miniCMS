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
    # DODAJEMY 'pin_order' DO LISTY
    list_display = ('title', 'published_date', 'is_published', 'is_pinned', 'pin_order', 'updated_at')
    list_filter = ('is_published', 'is_pinned', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'thumbnail', 'content')
        }),
        ('Ustawienia Publikacji', {
            # DODAJEMY 'pin_order' DO FORMULARZA
            'fields': ('published_date', 'is_published', 'is_pinned', 'pin_order'),
            'classes': ('collapse',),
        }),
    )