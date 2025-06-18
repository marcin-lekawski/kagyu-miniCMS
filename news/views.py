# news/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Article
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Do paginacji
import calendar # Do nazw miesięcy w archiwum
from django.db.models import Count # Do liczenia artykułów w archiwum


class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles' # Zostawiamy 'articles' zgodnie z Twoim plikiem
    paginate_by = 5

    def get_queryset(self):
        # Pobieramy tylko aktualności, które są opublikowane (is_published=True)
        # i których data publikacji jest mniejsza lub równa bieżącej dacie/czasowi.
        # Sortowanie: najpierw przypięte (True to 1, False to 0, więc malejąco),
        # potem data publikacji malejąco (najnowsze na górze).
        queryset = Article.objects.filter(
            is_published=True,
            published_date__lte=timezone.now()
        ).order_by('-is_pinned', 'pin_order', '-published_date') # <-- ZMODYFIKOWANA LINIA
        return queryset


def article_detail(request, slug):
    """
    Widok wyświetlający szczegóły pojedynczej aktualności.
    Artykuł musi być opublikowany i mieć datę publikacji <= bieżącej.
    """
    article = get_object_or_404(
        Article,
        slug=slug,
        is_published=True, # DODANO: upewniamy się, że artykuł jest opublikowany
        published_date__lte=timezone.now()
    )
    return render(request, 'news/article_detail.html', {'article': article})


def archive_view(request, year=None, month=None):
    # Początkowy queryset: tylko opublikowane artykuły z datą publikacji <= teraz
    articles_queryset = Article.objects.filter(
        is_published=True,
        published_date__lte=timezone.now()
    )

    # Filtrowanie po roku i/lub miesiącu, jeśli podano
    if year:
        articles_queryset = articles_queryset.filter(published_date__year=year)
    if month:
        articles_queryset = articles_queryset.filter(published_date__month=month)

    # Sortowanie dla archiwum
    articles_queryset = articles_queryset.order_by('-is_pinned', 'pin_order', '-published_date')

    # --- Paginacja ---
    paginator = Paginator(articles_queryset, 5)
    page_number = request.GET.get('page')
    try:
        articles_paged = paginator.page(page_number)
    except PageNotAnInteger:
        articles_paged = paginator.page(1)
    except EmptyPage:
        articles_paged = paginator.page(paginator.num_pages)
    # ------------------

    # --- Generowanie danych dla paska bocznego archiwum (bez zmian) ---
    archive_data = Article.objects.filter(
        is_published=True,
        published_date__lte=timezone.now()
    ).values('published_date__year', 'published_date__month') \
     .annotate(count=Count('id')) \
     .order_by('-published_date__year', '-published_date__month')
    
    archive_years_structured = {}
    for item in archive_data:
        year_num = item['published_date__year']
        month_num = item['published_date__month']
        if year_num not in archive_years_structured:
            archive_years_structured[year_num] = []
        archive_years_structured[year_num].append({
            'month_num': month_num,
            'month_name': calendar.month_name[month_num],
            'count': item['count']
        })
    for year_val in archive_years_structured:
        archive_years_structured[year_val].sort(key=lambda x: x['month_num'], reverse=True)
    # --------------------------------------------------------

    # W `context` przekazujemy teraz tylko wybrane wartości, bez `archive_title`
    context = {
        'articles': articles_paged,
        'selected_year': year,
        'selected_month': month,
        'archive_years_structured': archive_years_structured,
    }
    return render(request, 'news/archive_list.html', context)