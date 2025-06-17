#!/bin/bash

echo "--- Rozpoczynanie lokalnego procesu deploymentu na GitHub ---"

# 1. Aktywuj środowisko wirtualne
echo -e "\nAktywowanie środowiska wirtualnego..."
source venv/bin/activate # Zakłada, że twoje venv to 'venv' w katalogu projektu
if [ $? -ne 0 ]; then
    echo "BŁĄD: Nie udało się aktywować środowiska wirtualnego. Sprawdź ścieżkę do venv."
    exit 1
fi
echo "Środowisko wirtualne aktywowane."

# 2. Zaktualizuj plik requirements.txt
echo -e "\n--- Aktualizacja requirements.txt ---"
pip freeze > requirements.txt
if [ $? -ne 0 ]; then
    echo "BŁĄD: Nie udało się zaktualizować requirements.txt."
    exit 1
fi
echo "requirements.txt zaktualizowany."

# 3. Dodaj wszystkie zmiany do staging area
echo -e "\n--- Dodawanie zmian do Git staging area ---"
git add .
if [ $? -ne 0 ]; then
    echo "BŁĄD: Nie udało się dodać zmian do staging area."
    exit 1
fi
echo "Wszystkie zmiany dodane."

# 4. Zapytaj o wiadomość commita
echo -e "\n--- Tworzenie commita ---"
read -p "Wprowadź wiadomość dla commita: " commit_message
if [ -z "$commit_message" ]; then
    commit_message="Lokalny deployment"
    echo "Brak wiadomości. Używam domyślnej: '$commit_message'"
fi

git commit -m "$commit_message"
if [ $? -ne 0 ]; then
    echo "BŁĄD: Commit nie powiódł się. Sprawdź, czy są jakieś zmiany do zatwierdzenia."
    # Opcjonalnie: git reset HEAD~1 jeśli chcesz cofnąć ostatnie add.
    exit 1
fi
echo "Zmiany zatwierdzone."

# 5. Wypchnij zmiany na GitHub
echo -e "\n--- Wypychanie zmian na GitHub ---"
git push origin master # Zmień 'master' na 'main', jeśli to nazwa Twojej głównej gałęzi
if [ $? -ne 0 ]; then
    echo "BŁĄD: git push nie powiódł się. Sprawdź połączenie lub uprawnienia."
    exit 1
fi
echo "Zmiany wypchnięte na GitHub!"

echo -e "\n--- Lokalny deployment zakończony pomyślnie! ---"
echo "Teraz możesz przejść na PythonAnywhere i uruchomić ./deploy.sh"
