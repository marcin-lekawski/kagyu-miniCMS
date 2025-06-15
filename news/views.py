from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView # Do listy artykułów
from .models import Article
from django.utils import timezone # Do filtrowania archiwum

# Create your views here.


class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html' # Strona z listą artykułów
    context_object_name = 'articles' # Nazwa zmiennej w szablonie
    paginate_by = 5 # Opcjonalnie: paginacja, np. 5 artykułów na stronę

    def get_queryset(self):
        # Pobieramy tylko aktualności, które są już opublikowane (data publikacji <= teraz)
        return Article.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

def article_detail(request, slug):
    """
    Widok wyświetlający szczegóły pojedynczej aktualności.
    """
    article = get_object_or_404(Article, slug=slug, published_date__lte=timezone.now())
    return render(request, 'news/article_detail.html', {'article': article})

def archive_view(request, year=None, month=None):
    articles = Article.objects.filter(published_date__lte=timezone.now())

    if year:
        articles = articles.filter(published_date__year=year)
    if month:
        articles = articles.filter(published_date__month=month)

    articles = articles.order_by('-published_date')

    # Pobierz unikalne lata i miesiące do nawigacji archiwum
    dates = Article.objects.filter(published_date__lte=timezone.now()).dates('published_date', 'month', order='DESC')
    archive_years = sorted(list(set([d.year for d in dates])), reverse=True)
    archive_months = {}
    for d in dates:
        if d.year not in archive_months:
            archive_months[d.year] = []
        if d.month not in archive_months[d.year]:
            archive_months[d.year].append(d.month)

    context = {
        'articles': articles,
        'selected_year': year,
        'selected_month': month,
        'archive_years': archive_years,
        'archive_months': archive_months,
    }
    return render(request, 'news/archive_list.html', context)