// script.js

$(document).ready(function() {
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
        $('.burger-wrap .burger').removeClass('open'); // Zamknięcie animacji burgera
        $('.main-menu').removeClass('open'); // Zamykanie menu bocznego
        $('body').removeClass('overlay-open'); // Ukrywanie overlay'a
        $('body').removeClass('overlay-full');
        $('body').removeClass('overflow-hidden');
    });

    // Obsługa kliknięcia na overlay (zasłaniającą warstwę)
    $('.overlay').on('click', function() {
        $('.burger-wrap .burger').removeClass('open');
        $('.main-menu').removeClass('open');
        $('body').removeClass('overlay-open');
        $('body').removeClass('overlay-full');
        $('body').removeClass('overflow-hidden');
    });

    // Funkcja do obsługi klas 'opac' dla linków w menu głównym
    // (opac to 'opacity' z dostarczonych stylów)
    $('#menu-main li a').on('mouseenter', function() {
        $('#menu-main li a').not(this).addClass('opac');
    }).on('mouseleave', function() {
        $('#menu-main li a').removeClass('opac');
    });

    // Dodatkowa obsługa, aby zamknąć menu po kliknięciu linku (jeśli to potrzebne)
    $('#menu-main li a, .extra-menu-links li a').on('click', function() {
        // Dodaj małe opóźnienie, aby animacja zamknięcia była widoczna
        setTimeout(function() {
            $('.burger-wrap .burger').removeClass('open');
            $('.main-menu').removeClass('open');
            $('body').removeClass('overlay-open');
            $('body').removeClass('overlay-full');
            $('body').removeClass('overflow-hidden');
        }, 300); // Czas opóźnienia w milisekundach
    });

    // --- Inne skrypty, które możesz mieć w przyszłości ---
    // np. obsługa mapy, slidera, itp.
});