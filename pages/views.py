from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Page

def page_detail(request, slug):
    """
    Widok wyświetlający szczegóły pojedynczej strony.
    Pobiera stronę na podstawie jej 'slug' (unikalnego identyfikatora URL).
    """
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'pages/page_detail.html', {'page': page})