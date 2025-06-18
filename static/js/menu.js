document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;

    // --- LOGIKA GŁÓWNEGO MENU ---
    const burgerBtn = document.getElementById('burger-menu-icon');
    const sideMenu = document.getElementById('side-menu');
    const closeBtn = document.getElementById('close-menu-btn');
    const mainContent = document.querySelector('main');

    if (!burgerBtn || !sideMenu || !closeBtn || !body) {
        console.error("Brak jednego z kluczowych elementów menu na stronie.");
        return;
    }

    const toggleMenu = () => {
        const isMenuOpen = body.classList.contains('menu-open');
        burgerBtn.classList.toggle('open', !isMenuOpen);
        sideMenu.classList.toggle('open', !isMenuOpen);
        body.classList.toggle('menu-open', !isMenuOpen);
    };

    burgerBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMenu();
    });

    closeBtn.addEventListener('click', toggleMenu);
    
    if (mainContent) {
        mainContent.addEventListener('click', () => {
            if (body.classList.contains('menu-open')) {
                toggleMenu();
            }
        });
    }

    // --- LOGIKA PŁYNNEGO PRZEJŚCIA MIĘDZY STRONAMI ---
    const handlePageTransition = (event) => {
        const link = event.target.closest('a');

        if (link && link.href.startsWith(window.location.origin) && !link.href.includes('#') && link.target !== '_blank') {
            event.preventDefault(); 
            const destination = link.href;
            body.classList.add('is-leaving');
            setTimeout(() => {
                window.location.href = destination;
            }, 400); 
        }
    };

    document.addEventListener('click', handlePageTransition);


    // --- LOGIKA GENEROWANIA SPISU TREŚCI (TOC) ---
    const generateTableOfContents = () => {
        const contentSource = document.getElementById('page-content');
        const tocContainer = document.getElementById('toc-container');

        if (!contentSource || !tocContainer) return;

        const headings = contentSource.querySelectorAll('h2, h3');
        if (headings.length === 0) return;

        let tocHTML = '<ul>';
        headings.forEach((heading, index) => {
            let id = heading.getAttribute('id');
            if (!id) {
                id = 'toc-heading-' + index;
                heading.setAttribute('id', id);
            }
            const isH3 = heading.tagName.toLowerCase() === 'h3';
            const linkClass = isH3 ? 'toc-link toc-h3' : 'toc-link';
            tocHTML += `<li><a href="#${id}" class="${linkClass}">${heading.textContent}</a></li>`;
        });
        tocHTML += '</ul>';
        tocContainer.innerHTML = tocHTML;

        tocContainer.addEventListener('click', (event) => {
            if (event.target.tagName.toLowerCase() === 'a' && event.target.getAttribute('href').startsWith('#')) {
                event.preventDefault();
                event.stopPropagation(); // ZATRZYMUJEMY bąbelkowanie, aby nie uruchomić pageTransition
                const targetId = event.target.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    if (body.classList.contains('menu-open')) {
                        toggleMenu();
                    }
                    setTimeout(() => {
                        const headerOffset = 60;
                        const elementPosition = targetElement.getBoundingClientRect().top;
                        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                        window.scrollTo({ top: offsetPosition, behavior: "smooth" });
                    }, 500);
                }
            }
        });
    };

    generateTableOfContents();
});