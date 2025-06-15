from django.urls import path
from . import views

app_name = 'pages' # Nazwa przestrzeni nazw dla adresów URL

urlpatterns = [
    # Ten wzorzec będzie pasował do adresów typu /o-nas/, /kontakt/, /moja-strona/
    path('<slug:slug>/', views.page_detail, name='detail'),
]