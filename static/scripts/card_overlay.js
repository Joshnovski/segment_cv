document.addEventListener('DOMContentLoaded', function() {

    const overlay = document.getElementById("overlay");
    let enlargedCardHeader = overlay.querySelector('.card-header');
    const enlargedCardContainer = overlay.querySelector('.card-container');

    // Show the enlarged card when the expand-icon is clicked
    document.querySelectorAll('.expand-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const originalCard = icon.closest('.card');

            // Get header text
            const headerText = originalCard.querySelector('.card-header').firstChild.textContent.trim();

            // Copying header inner content
            const originalHeaderContent = originalCard.querySelector('.icon-container').cloneNode(true);

            // Clearing and appending text and icons to the enlarged card's header
            enlargedCardHeader.innerHTML = headerText;
            enlargedCardHeader.appendChild(originalHeaderContent);

            const newExpandIcon = enlargedCardHeader.querySelector('.expand-icon');
            newExpandIcon.classList.remove('expand-icon');
            newExpandIcon.classList.add('fa-times', 'close-icon');

            // Need to bind the close event to the new close icon
            newExpandIcon.addEventListener('click', function() {
                overlay.style.display = 'none';
            });

            // Copying main content
            const originalMainContent = originalCard.querySelector('.card-container').innerHTML;
            enlargedCardContainer.innerHTML = originalMainContent;

            // Displaying the overlay
            overlay.style.display = 'flex';
        });
    });
});

