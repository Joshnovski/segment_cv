document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('nav');
    const main = document.querySelector('main');
    const header = document.querySelector('header');

    nav.addEventListener('click', function() {
        if(window.innerWidth <= 870) {
            nav.classList.add('expanded');
            main.classList.add('nav-expanded');
            header.classList.add('header-expanded');
        }
    });

    document.addEventListener('click', function(e) {
        if(!nav.contains(e.target) && nav.classList.contains('expanded')) {
            nav.classList.remove('expanded');
            main.classList.remove('nav-expanded');
            header.classList.remove('header-expanded');
        }
    });
});

