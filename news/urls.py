# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Najpierw umieść bardziej specyficzne wzorce URL dla archiwum
    path('archiwum/', views.archive_view, name='archive_all'),
    path('archiwum/<int:year>/', views.archive_view, name='archive_year'),
    path('archiwum/<int:year>/<int:month>/', views.archive_view, name='archive_month'),

    # Następnie lista aktualności (bardziej ogólna)
    path('', views.ArticleListView.as_view(), name='list'),

    # Na końcu szczegóły pojedynczej aktualności (catch-all dla slugów)
    path('<slug:slug>/', views.article_detail, name='article_detail'), # ZMIENIONO: name='detail' na name='article_detail'
]