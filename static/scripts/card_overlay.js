document.addEventListener('DOMContentLoaded', function() {

    const overlay = document.getElementById("overlay");
    const enlargedCardHeader = overlay.querySelector('.card-header');
    const enlargedCardContainer = overlay.querySelector('.card-container');
    const closeIcon = overlay.querySelector('.close-icon');

    // Show the enlarged card when the expand-icon is clicked
    document.querySelectorAll('.expand-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const originalCard = icon.closest('.card');

            // Copying header content
            const originalHeaderContent = originalCard.querySelector('.card-header').cloneNode(true);
            enlargedCardHeader.innerHTML = '';
            enlargedCardHeader.appendChild(originalHeaderContent);
            const newExpandIcon = enlargedCardHeader.querySelector('.expand-icon');
            newExpandIcon.classList.remove('expand-icon');
            newExpandIcon.classList.add('fa-times', 'close-icon');
            
            // Copying main content
            const originalMainContent = originalCard.querySelector('.card-container').innerHTML;
            enlargedCardContainer.innerHTML = originalMainContent;

            // Displaying the overlay
            overlay.style.display = 'flex';
        });
    });

    // Hide the enlarged card when the close-icon (X) is clicked
    closeIcon.addEventListener('click', function() {
        overlay.style.display = 'none';
    });

});
