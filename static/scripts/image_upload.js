// Function to programmatically trigger the file input element when called.
function triggerFileInput() 
{
    // Trigger a click event on the file input element with ID 'file'.
    // This opens the file picker dialog for the user.
    document.getElementById('file').click();
}
// Wait until the document's content has fully loaded before executing the function.
document.addEventListener('DOMContentLoaded', function() {
    // Set a timer to execute after 5 seconds.
    setTimeout(function() {
        // Get all elements with class 'flash' - typically used for temporary notification messages.
        var flashes = document.querySelectorAll('.flash');
        // Iterate through each flash message.
        flashes.forEach(function(flash) {
            // Gradually fade out the flash message by setting its opacity to 0.
            flash.style.opacity = 0;
            // When the CSS opacity transition ends, hide the flash message completely.
            flash.addEventListener('transitionend', function() {
                flash.style.display = 'none';
            });
        });
    }, 5000);
});
