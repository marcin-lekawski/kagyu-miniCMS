from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
import os

# Ten dekorator zapewnia, że tylko zalogowani członkowie personelu (np. admini) mogą przesyłać pliki.
@staff_member_required
@csrf_exempt # Wyłączamy ochronę CSRF dla tego widoku, TinyMCE obsługuje to inaczej.
def upload_image(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        if file_obj:
            # Upewnij się, że nazwa pliku jest bezpieczna
            file_name = default_storage.get_available_name(file_obj.name)
            
            # Zapisz plik w domyślnej lokalizacji mediów
            file_path = default_storage.save(file_name, file_obj)
            
            # Pobierz publiczny URL do zapisanego pliku
            file_url = default_storage.url(file_path)
            
            # TinyMCE oczekuje odpowiedzi w formacie JSON z kluczem 'location'
            return JsonResponse({
                'location': file_url
            })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
