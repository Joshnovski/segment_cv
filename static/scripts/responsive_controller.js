document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('nav');
    const main = document.querySelector('main');
    const header = document.querySelector('header');

    function collapseAll() {
        const openElements = document.querySelectorAll('.collapse.show');
        openElements.forEach(element => {
            element.classList.remove('show');
        });
        // Remove active class from nav-item-title
        const activeTitles = document.querySelectorAll('.nav-item-title.active');
        activeTitles.forEach(title => {
            title.classList.remove('active');
        });
    }

    nav.addEventListener('click', function(e) {
        e.stopPropagation();  // Prevent the click from propagating to the document

        if (window.innerWidth <= 870) {
            nav.classList.add('expanded');  // Add the expanded state
            main.classList.add('nav-expanded');
            header.classList.add('header-expanded');

            main.style.setProperty('--overlay-height', `${main.scrollHeight}px`);
        }
    });

    document.addEventListener('click', function(e) {
        if (!nav.contains(e.target)) {
            nav.classList.remove('expanded');
            main.classList.remove('nav-expanded');
            header.classList.remove('header-expanded');
            collapseAll();
        }
    });
});
