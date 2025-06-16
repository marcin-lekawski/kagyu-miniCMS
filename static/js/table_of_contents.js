// static/js/table_of_contents.js

$(document).ready(function() {
    const $pageContent = $('#page-content');
    const headings = $pageContent.find('h2, h3');

    // REFERENCJE DO GŁÓWNYCH KONTENERÓW KOLUMN/KART SPISU TREŚCI
    // Będziemy ukrywać/pokazywać całe te bloki
    const $desktopTocColumn = $('.col-md-3.order-md-1');
    const $mobileTocCard = $('#mobile-toc-container'); // To już jest referencja do karty mobilnej

    // Jeśli nie ma nagłówków, UKRYJ CAŁE KONTENERY SPISÓW TREŚCI I ZAKOŃCZ SKRYPT
    if (headings.length === 0) {
        $desktopTocColumn.hide(); // Ukryj całą kolumnę desktopową
        $mobileTocCard.hide();    // Ukryj całą kartę mobilną (wraz z przyciskiem)
        return; // WAŻNE: Zakończ wykonywanie skryptu, jeśli nie ma nagłówków
    }

    // --- Jeśli są nagłówki, kontynuuj generowanie spisu treści ---

    let tocHTML = '<nav class="nav flex-column">'; // Rozpocznij budowanie HTML spisu treści z tagiem <nav>
    headings.each(function(index) {
        const $heading = $(this);
        let id = $heading.attr('id');
        if (!id) {
            id = 'section-' + (index + 1) + '-' + $heading.text().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
            $heading.attr('id', id);
        }

        let className = 'nav-link';
        if ($heading.prop('tagName') === 'H3') {
            className += ' ms-3';
        }

        tocHTML += `<a class="${className}" href="#${id}">${$heading.text()}</a>`;
    });
    tocHTML += '</nav>'; // Zamknij tag <nav>

    // Wstaw wygenerowany HTML do kontenerów spisu treści
    $('#table-of-contents-desktop').html(tocHTML);
    $('#table-of-contents-mobile').html(tocHTML);

    // Pokaż kontenery spisu treści, jeśli są nagłówki (bo na początku mogły być ukryte)
    $desktopTocColumn.show(); // Pokaż całą kolumnę desktopową
    $mobileTocCard.show();    // Pokaż całą kartę mobilną


    // --- Reszta kodu odpowiedzialna za funkcjonalność spisu treści ---

    // Konieczne jest ponowne pobranie referencji do <nav>,
    // ponieważ zostały one dynamicznie wstawione do DOM.
    const $tocDesktop = $('#table-of-contents-desktop nav');
    const $tocMobile = $('#table-of-contents-mobile nav');
    
    // Upewnij się, że przycisk mobilny "Pokaż spis treści" jest zawsze widoczny,
    // jeśli spis treści jest generowany.
    // Pamiętaj, że cała karta mobilna ($mobileTocCard) jest pokazywana wyżej.

    // Smooth scrolling dla obu spisów treści
    $([$tocDesktop[0], $tocMobile[0]]).on('click', 'a.nav-link', function(e) {
        e.preventDefault();
        const targetId = $(this).attr('href');
        $('html, body').animate({
            scrollTop: $(targetId).offset().top - $('header').outerHeight() - 20
        }, 800);

        if ($(window).width() < 768) {
            $('#table-of-contents-mobile-collapse').collapse('hide');
        }
    });

    // Aktywny link w spisie treści podczas scrollowania
    const $allTocLinks = $tocDesktop.find('.nav-link').add($tocMobile.find('.nav-link'));
    const headingPositions = headings.map(function() {
        return {
            id: $(this).attr('id'),
            top: $(this).offset().top
        };
    }).get();

    $(window).on('scroll', function() {
        const scrollPos = $(document).scrollTop();
        const headerHeight = $('header').outerHeight();
        const offset = headerHeight + 10;

        let currentActiveHeadingId = null;

        for (let i = headingPositions.length - 1; i >= 0; i--) {
            if (scrollPos >= headingPositions[i].top - offset) {
                currentActiveHeadingId = headingPositions[i].id;
                break;
            }
        }

        $allTocLinks.removeClass('active-toc-link');
        if (currentActiveHeadingId) {
            $(`a[href="#${currentActiveHeadingId}"]`, $allTocLinks).addClass('active-toc-link');
        }

        // Pokaż/ukryj przycisk "Powrót na górę"
        const $backToTopButton = $('#back-to-top');
        if (scrollPos > 300) {
            $backToTopButton.fadeIn();
        } else {
            $backToTopButton.fadeOut();
        }
    });

    // Funkcjonalność przycisku "Powrót na górę"
    $('#back-to-top').on('click', function() {
        $('html, body').animate({
            scrollTop: 0
        }, 800);
    });
});