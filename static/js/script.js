// script.js

$(document).ready(function() {
    // Obsługa kliknięcia ikony burgera
    // Celujemy bezpośrednio w div.burger z klasą .burger, jak było na początku
    $('.burger-wrap .burger').on('click', function() {
        $(this).toggleClass('open'); // Animacja burgera
        $('.main-menu').toggleClass('open'); // Otwieranie/zamykanie menu bocznego
        $('body').toggleClass('overlay-open'); // Pokazywanie/ukrywanie overlay'a
        $('body').toggleClass('overlay-full'); // Zapewnienie, że overlay jest pełny
        $('body').toggleClass('overflow-hidden'); // Zapobiega przewijaniu tła, gdy menu jest otwarte (opcjonalnie)
    });

    // Obsługa kliknięcia przycisku zamykania w menu
    $('.main-menu .close-menu').on('click', function() {
        // Celujemy w div.burger z klasą .burger
        $('.burger-wrap .burger').removeClass('open'); 
        $('.main-menu').removeClass('open');
        $('body').removeClass('overlay-open');
        $('body').removeClass('overlay-full');
        $('body').removeClass('overflow-hidden');
    });

    // Obsługa kliknięcia na overlay
    $('.overlay').on('click', function() {
        // Celujemy w div.burger z klasą .burger
        $('.burger-wrap .burger').removeClass('open');
        $('.main-menu').removeClass('open');
        $('body').removeClass('overlay-open');
        $('body').removeClass('overlay-full');
        $('body').removeClass('overflow-hidden');
    });

    // Funkcja do obsługi klas 'opac' dla linków w menu głównym (bez zmian)
    $('#menu-main li a').on('mouseenter', function() {
        $('#menu-main li a').not(this).addClass('opac');
    }).on('mouseleave', function() {
        $('#menu-main li a').removeClass('opac');
    });

    // Dodatkowa obsługa, aby zamknąć menu po kliknięciu linku w menu bocznym (bez zmian)
    $('#menu-main li a, .extra-menu-links li a').on('click', function() {
        setTimeout(function() {
            $('.burger-wrap .burger').removeClass('open'); // Celujemy w div.burger
            $('.main-menu').removeClass('open');
            $('body').removeClass('overlay-open');
            $('body').removeClass('overlay-full');
            $('body').removeClass('overflow-hidden');
        }, 300);
    });

    // Funkcjonalność przycisku "Powrót na górę"
    $('#back-to-top').on('click', function() {
        $('html, body').animate({
            scrollTop: 0
        }, 800);
    });
    // --- Inne skrypty, które możesz mieć w przyszłości ---
});