// Upewniamy się, że kod uruchomi się po załadowaniu struktury strony
document.addEventListener('DOMContentLoaded', function() {
    // Sprawdzamy, czy jesteśmy na stronie edycji artykułu w Django admin
    if (document.body.classList.contains('change-form') && document.body.id === 'news-article-change-form') {

        const sizeSelect = document.querySelector('#id_thumbnail_size');
        const customWidthRow = document.querySelector('.field-thumbnail_custom_width');

        if (sizeSelect && customWidthRow) {
            
            // Funkcja do pokazywania/ukrywania pola
            function toggleCustomWidthField() {
                if (sizeSelect.value === 'CUSTOM') {
                    customWidthRow.style.display = 'block';
                } else {
                    customWidthRow.style.display = 'none';
                }
            }

            // Uruchom funkcję od razu po załadowaniu strony
            toggleCustomWidthField();
            
            // Uruchom funkcję za każdym razem, gdy zmieni się wybór w dropdownie
            sizeSelect.addEventListener('change', toggleCustomWidthField);
        }
    }
});
