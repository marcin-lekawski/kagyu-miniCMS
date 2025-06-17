// static/js/script.js

$(document).ready(function() {
    // === Burger Menu Logic ===
    // Obsługa kliknięcia ikony burgera
    $('.burger-wrap .burger').on('click', function() {
        $(this).toggleClass('open'); // Animacja burgera
        $('.main-menu').toggleClass('open'); // Otwieranie/zamykanie menu bocznego
        $('body').toggleClass('overlay-open'); // Pokazywanie/ukrywanie overlay'a
        $('body').toggleClass('overlay-full'); // Zapewnienie, że overlay jest pełny
        $('body').toggleClass('overflow-hidden'); // Zapobiega przewijaniu tła, gdy menu jest otwarte (opcjonalnie)
    });

    // Obsługa kliknięcia przycisku zamykania w menu
    $('.main-menu .close-menu').on('click', function() {
        $('.burger-wrap .burger').removeClass('open');
        $('.main-menu').removeClass('open');
        $('body').removeClass('overlay-open');
        $('body').removeClass('overlay-full');
        $('body').removeClass('overflow-hidden');
    });

    // Obsługa kliknięcia na overlay
    $('.overlay').on('click', function() {
        $('.burger-wrap .burger').removeClass('open');
        $('.main-menu').removeClass('open');
        $('body').removeClass('overlay-open');
        $('body').removeClass('overlay-full');
        $('body').removeClass('overflow-hidden');
    });

    // === Aktywne linki w głównym menu + efekt opac ===
    $('#menu-main li a').on('mouseenter', function() {
        $('#menu-main li a').not(this).addClass('opac');
    }).on('mouseleave', function() {
        $('#menu-main li a').removeClass('opac');
    });

    // === Dodatkowa obsługa, aby zamknąć menu po kliknięciu linku z menu głównego ===
    $('#menu-main li a, .extra-menu-links li a').on('click', function() {
        // Dodatkowe opóźnienie, aby animacja zamknięcia menu była widoczna
        setTimeout(function() {
            $('.burger-wrap .burger').removeClass('open');
            $('.main-menu').removeClass('open');
            $('body').removeClass('overlay-open');
            $('body').removeClass('overlay-full');
            $('body').removeClass('overflow-hidden');
        }, 300);
    });


    // === DYNAMICZNY SPIS TREŚCI W BURGER MENU (PRZENIESIONY Z table_of_contents.js) ===
    function generateTableOfContents() {
        // Ważne: #page-content to kontener, w którym znajduje się treść strony,
        // skrypt będzie szukał nagłówków w nim
        const $pageContent = $('#page-content');
        const $tocContainerUl = $('#main-menu-table-of-contents ul'); // Lista <ul> w nowym kontenerze TOC w burger menu
        const $tocWrapper = $('#main-menu-table-of-contents'); // Cały div spisu treści w menu

        $tocContainerUl.empty(); // Wyczyść poprzedni spis treści przed regeneracją

        // Szukaj nagłówków TYLKO jeśli #page-content istnieje na stronie
        if ($pageContent.length === 0) {
            $tocWrapper.hide(); // Ukryj blok spisu treści, jeśli nie ma kontenera treści
            return;
        }

        const headings = $pageContent.find('h2, h3'); // Skanuj nagłówki h2 i h3

        if (headings.length === 0) {
            $tocWrapper.hide(); // Ukryj cały blok spisu treści w menu, jeśli nie ma nagłówków
            return;
        }

        $tocWrapper.show(); // Pokaż blok spisu treści, jeśli są nagłówki

        let currentLevel = 0;
        let $currentList = $tocContainerUl; // Rozpoczynamy od głównego <ul> w #main-menu-table-of-contents

        headings.each(function(index) {
            const $heading = $(this);
            let id = $heading.attr('id');
            // Upewnij się, że ID jest unikalne i zgodne z konwencją
            if (!id) {
                id = 'section-' + (index + 1) + '-' + $heading.text().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-*|-*$/g, '');
                $heading.attr('id', id);
            }

            const headingText = $heading.text();
            const headingLevel = parseInt(this.tagName.substring(1)); // H2 -> 2, H3 -> 3

            // Obsługa zagnieżdżonych list dla H2 i H3
            if (headingLevel > currentLevel) {
                for (let i = currentLevel; i < headingLevel; i++) {
                    const newSubList = $('<ul></ul>');
                    $currentList.append($('<li></li>').append(newSubList));
                    $currentList = newSubList;
                }
            } else if (headingLevel < currentLevel) {
                for (let i = currentLevel; i > headingLevel; i--) {
                    // Wychodzimy o jeden poziom wyżej
                    $currentList = $currentList.parent().closest('ul');
                }
            }
            currentLevel = headingLevel;

            let listItem = $('<li><a href="#' + id + '">' + headingText + '</a></li>');
            // Dodaj klasę dla H3, jeśli chcesz inne stylowanie w menu
            if (headingLevel === 3) {
                listItem.find('a').addClass('ms-3'); // Dodaj wcięcie dla H3, jak w starym skrypcie
            }
            $currentList.append(listItem);
        });

        // Płynne przewijanie dla linków spisu treści w burger menu
        // Użyj delegacji zdarzeń na kontenerze spisu treści, aby obsłużyć linki dodane dynamicznie
        // Użyj .off() aby uniknąć wielokrotnego przypinania zdarzeń po regeneracji TOC
        $tocContainerUl.off('click', 'a').on('click', 'a', function(e) {
            e.preventDefault();
            const targetId = $(this).attr('href');
            // Offset uwzględnia wysokość nagłówka fixed i mały bufor
            $('html, body').animate({
                scrollTop: $(targetId).offset().top - $('header').outerHeight() - 20
            }, 800);

            // Zamknij menu boczne po kliknięciu linku spisu treści
            $('.burger-wrap .burger').removeClass('open');
            $('.main-menu').removeClass('open');
            $('body').removeClass('overlay-open');
            $('body').removeClass('overlay-full');
            $('body').removeClass('overflow-hidden');
        });
    }

    // Wywołaj funkcję generującą spis treści po załadowaniu DOM
    // Upewnij się, że #page-content istnieje na danej stronie przed próbą generowania TOC
    // Chociaż funkcja sama to sprawdza, to jest to dodatkowy warunek
    if ($('#page-content').length) {
        generateTableOfContents();
    }


    // === Aktywny link w spisie treści podczas scrollowania ===
    // Ten kod musi działać niezależnie od tego, czy menu jest otwarte, czy zamknięte
    $(window).on('scroll', function() {
        const scrollPos = $(document).scrollTop();
        const headerHeight = $('header').outerHeight();
        const offset = headerHeight + 10; // Bufor dla sticky headera

        let currentActiveHeadingId = null;
        const $pageContent = $('#page-content');

        // Tylko jeśli jesteśmy na stronie z treścią i nagłówkami
        if ($pageContent.length > 0) {
            const headingsInContent = $pageContent.find('h2, h3'); // Pobieraj nagłówki z treści
            const headingPositions = headingsInContent.map(function() {
                // Sprawdź, czy element istnieje i ma offset()
                if ($(this).length && $(this).offset()) {
                    return {
                        id: $(this).attr('id'),
                        top: $(this).offset().top
                    };
                }
                return null; // Zwróć null dla elementów, które nie istnieją lub nie mają offsetu
            }).get().filter(n => n); // Odfiltruj nulle

            for (let i = headingPositions.length - 1; i >= 0; i--) {
                if (scrollPos >= headingPositions[i].top - offset) {
                    currentActiveHeadingId = headingPositions[i].id;
                    break;
                }
            }
        }

        // Zaktualizuj klasy dla linków w spisie treści w menu bocznym
        // Dodano selektor dla ul, aby upewnić się, że celujemy we właściwe linki
        $('#main-menu-table-of-contents ul').find('a').removeClass('active-toc-link');
        if (currentActiveHeadingId) {
            $('#main-menu-table-of-contents ul').find(`a[href="#${currentActiveHeadingId}"]`).addClass('active-toc-link');
        }

        // === Funkcjonalność przycisku "Powrót na górę" ===
        // Upewnij się, że ten przycisk jest w base.html lub na każdej stronie i ma ID #back-to-top
        const $backToTopButton = $('#back-to-top');
        if ($backToTopButton.length) { // Sprawdź, czy przycisk istnieje w DOM
            if (scrollPos > 300) {
                $backToTopButton.fadeIn();
            } else {
                $backToTopButton.fadeOut();
            }
        }
    });

    // === Funkcjonalność przycisku "Powrót na górę" (kliknięcie) ===
    $('#back-to-top').on('click', function() {
        $('html, body').animate({
            scrollTop: 0
        }, 800);
    });

    // --- Inne skrypty, które możesz mieć w przyszłości ---
});