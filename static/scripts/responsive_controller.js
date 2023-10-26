// Ensure that the code runs after the document's content has fully loaded.
document.addEventListener('DOMContentLoaded', function() {
    // Select the relevant elements from the DOM.
    const nav = document.querySelector('nav');
    const main = document.querySelector('main');
    const header = document.querySelector('header');
    // Function to collapse all expanded sections.
    function collapseAll() {
        // Find all elements with the 'show' class (indicating they're currently expanded).
        const openElements = document.querySelectorAll('.collapse.show');
        openElements.forEach(element => {
            // Remove the 'show' class, which will collapse the section.
            element.classList.remove('show');
        });
        // Remove the 'active' class from all navigation titles.
        const activeTitles = document.querySelectorAll('.nav-item-title.active');
        activeTitles.forEach(title => {
            title.classList.remove('active');
        });
    }
    // Add a click event listener to the navigation.
    nav.addEventListener('click', function(e) {
        // Prevent the click event from bubbling up and being captured by other event listeners.
        e.stopPropagation();  
        // Check if the window's inner width is 870 pixels or less.
        if (window.innerWidth <= 870) {
            // Adjust the styles for a mobile-friendly expanded navigation view.
            nav.classList.add('expanded');  
            main.classList.add('nav-expanded');
            header.classList.add('header-expanded');
            // Dynamically set a CSS variable to adjust overlay height based on the main content's scroll height.
            main.style.setProperty('--overlay-height', `${main.scrollHeight}px`);
        }
    });
    // Add a click event listener to the entire document.
    document.addEventListener('click', function(e) {
        // If the clicked element is not a part of the navigation,
        if (!nav.contains(e.target)) {
            // Remove the expanded styles and collapse all sections.
            nav.classList.remove('expanded');
            main.classList.remove('nav-expanded');
            header.classList.remove('header-expanded');
            collapseAll();
        }
    });
});

