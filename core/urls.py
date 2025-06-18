"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from news.views import ArticleListView 

# Dodaj importy do obsługi plików statycznych i mediów
from django.conf import settings
from django.conf.urls.static import static
from site_config.views import upload_image


urlpatterns = [
    path('admin/', admin.site.urls),

    # Dodajemy adres URL dla TinyMCE, aby umożliwić edycję treści stron
    # Wzorzec 'tinymce/' przekierowuje do aplikacji TinyMCE, która obsługuje edycję treści
    # Dzięki temu użytkownicy będą mogli korzystać z edytora TinyMCE do tworzenia i edycji treści stron.
    path('tinymce/', include('tinymce.urls')),

    # NOWY ADRES URL DLA UPLOADERA
    path('tinymce/upload-image/', upload_image, name='tinymce-upload-image'),

    # Strona główna - teraz będzie wyświetlać listę aktualności
    # Możemy zmienić to na TemplateView jeśli chcemy statyczną stronę główną
    # lub użyć widoku listy aktualności
    
    path('', ArticleListView.as_view(), name='home'), # Strona główna pokazuje aktualności
    # Jeśli chcesz, żeby home.html był statyczny, a lista aktualności pod /aktualnosci/ wtedy zahaszuj powyższą linię i odkomentuj poniższą linię:
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('aktualnosci/', include('news.urls')), # Dołącz adresy URL z aplikacji news pod /aktualnosci/

    # Dołącz adresy URL z naszej aplikacji 'pages'
    # Każdy adres URL nie pasujący do 'admin/' ani '/' zostanie przekazany do 'pages.urls'
    path('', include('pages.urls')),
]

 # * `path('', TemplateView.as_view(template_name='home.html'), name='home')`: Dodałem podstawową stronę główną, która po prostu wyświetli szablon `home.html`. Dostępna będzie pod adresem `/`.
 # * `path('', include('pages.urls'))`: Ta linia jest kluczowa. Mówi Django, że dla wszystkich ścieżek, które nie pasują do wcześniejszych wzorców (czyli `/admin/` czy `/`), ma szukać dalszych wzorców w pliku `pages/urls.py`. Dzięki temu `/o-nas/` zostanie przekazane do `pages/urls.py`, a tam zostanie dopasowane przez `<slug:slug>/`.



# Dodaj tę sekcję TYLKO w trybie deweloperskim (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Jeśli planujesz również serwować pliki statyczne w DEBUG=True (dla dev), możesz dodać:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)