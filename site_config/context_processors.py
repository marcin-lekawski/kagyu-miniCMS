# site_config/context_processors.py
from .models import HeaderContent, FooterContent
from pages.models import Page
from news.models import Article # Jeśli potrzebujesz najnowszych artykułów w stopce

def global_website_content(request):
    header_content = HeaderContent.objects.first()
    footer_content = FooterContent.objects.first()

    all_pages = Page.objects.filter(is_published=True).order_by('order', 'title')

    # latest_articles = Article.objects.filter(is_published=True).order_by('-published_date')[:3] # Odkomentuj, jeśli potrzebujesz

    return {
        'header_content': header_content,
        'footer_content': footer_content,
        'all_pages': all_pages,
        # 'latest_articles': latest_articles, # Odkomentuj, jeśli potrzebujesz
    }