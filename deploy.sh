#!/bin/bash

# Aktywuj środowisko wirtualne Django
echo "Aktywowanie środowiska wirtualnego..."
source ~/.virtualenvs/kagyu_env/bin/activate

# 1. Pobierz najnowsze zmiany z GitHuba
echo -e "\n--- Pobieranie najnowszych zmian z GitHub ---"
git pull origin master # Upewnij się, że 'master' to nazwa Twojej głównej gałęzi, zmień na 'main' jeśli to konieczne.
if [ $? -ne 0 ]; then
    echo "BŁĄD: git pull nie powiódł się. Sprawdź konflikty lub lokalne zmiany."
    exit 1
fi
echo "Pobrano zmiany."

# 2. Zbierz pliki statyczne
echo -e "\n--- Zbieranie plików statycznych ---"
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "BŁĄD: collectstatic nie powiódł się."
    exit 1
fi
echo "Pliki statyczne zebrane."

# 3. Zapytaj o wykonanie migracji bazy danych
echo -e "\n--- Sprawdzanie i wykonywanie migracji bazy danych ---"
read -p "Czy chcesz wykonać migracje bazy danych? (y/n): " confirm_migrate
if [[ "$confirm_migrate" =~ ^[Yy]$ ]]; then
    python manage.py makemigrations
    python manage.py migrate
    if [ $? -ne 0 ]; then
        echo "BŁĄD: Migracje nie powiodły się."
        exit 1
    fi
    echo "Migracje wykonane."
else
    echo "Migracje pominięte."
fi

# 4. Przeładuj aplikację WWW na PythonAnywhere
echo -e "\n--- Przeładowywanie aplikacji WWW na PythonAnywhere ---"
# Dotknięcie pliku WSGI powoduje przeładowanie aplikacji
/usr/bin/touch /var/www/marcin108_pythonanywhere_com_wsgi.py
if [ $? -ne 0 ]; then
    echo "BŁĄD: Przeładowanie aplikacji nie powiodło się. Sprawdź ścieżkę do pliku WSGI."
    exit 1
fi
echo "Aplikacja WWW przeładowana."

echo -e "\n--- Wdrożenie zakończone pomyślnie! ---"
