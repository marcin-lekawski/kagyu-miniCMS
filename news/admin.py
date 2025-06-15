from django.contrib import admin
from .models import Article

# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'slug', 'created_at', 'updated_at')
    list_filter = ('published_date',) # Filtr po dacie publikacji
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date' # Ułatwia przeglądanie po dacie
