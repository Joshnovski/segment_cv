// Wait until the document's content has fully loaded before executing the function
document.addEventListener('DOMContentLoaded', function() {

    // Get overlay and various child elements for later use
    const overlay = document.getElementById("overlay");
    let enlargedCardHeader = overlay.querySelector('.card-header');
    const enlargedCardContainer = overlay.querySelector('.card-container');
    const enlargedCard = overlay.querySelector('.enlarged-card');

    // Attach event listeners to all expand-icons to enable card enlargement
    document.querySelectorAll('.expand-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            // Find the closest ancestor card of the clicked expand-icon
            const originalCard = icon.closest('.card');
            
            // Extract header text from the original card
            const headerText = originalCard.querySelector('.card-header').firstChild.textContent.trim();
            
            // Clone the icon-container from the original card
            const originalHeaderContent = originalCard.querySelector('.icon-container').cloneNode(true);
            
            // Clear existing content and set header text and icons to the enlarged card's header
            enlargedCardHeader.innerHTML = headerText;
            enlargedCardHeader.appendChild(originalHeaderContent);

            // Update the cloned expand-icon to a close icon in the enlarged card's header
            const newExpandIcon = enlargedCardHeader.querySelector('.expand-icon');
            newExpandIcon.classList.remove('expand-icon');
            newExpandIcon.classList.add('fa-times', 'close-icon');
            
            // Attach an event listener to the close icon to hide the overlay and reset the enlarged card width
            newExpandIcon.addEventListener('click', function() {
                overlay.style.display = 'none';
                enlargedCard.style.width = "";
            });
            
            // Clone main content from the original card for display in the enlarged card
            let originalMainContent;
            if (originalCard.querySelector('.card-container')) {
                originalMainContent = originalCard.querySelector('.card-container').cloneNode(true);
            }
            if (originalCard.querySelector('.histogram-container')) {
                originalMainContent = originalCard.querySelector('.histogram-container').cloneNode(true);
            }
            // Clear existing content and set main content in the enlarged card
            enlargedCardContainer.innerHTML = "";
            enlargedCardContainer.appendChild(originalMainContent);

            // Adjust the styling for any images in the enlarged card
            const enlargedImage = enlargedCardContainer.querySelector('.grid-img');
            if (enlargedImage) {
                enlargedImage.classList.add('enlarged-image');

                // Compute and set the width of the enlarged card based on the enlarged image width
                const computedWidth = getComputedStyle(enlargedImage).width;
                enlargedCard.style.width = computedWidth;
            }

            // Make the overlay (containing the enlarged card) visible
            overlay.style.display = 'flex';
        });
    });
});




