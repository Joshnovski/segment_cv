// Ensure that the code runs after the document's content has fully loaded.
document.addEventListener('DOMContentLoaded', function() {
    // Set a timer to execute after 5 seconds (5000 milliseconds).
    setTimeout(function() {
        // Select all elements with the class 'flash'.
        var flashes = document.querySelectorAll('.flash');
        // Iterate through each flash message.
        flashes.forEach(function(flash) {
            // Gradually fade out the flash message by setting its opacity to 0.
            flash.style.opacity = 0;
            // After the fade-out transition ends, the message will be hidden completely.
            flash.addEventListener('transitionend', function() {
                flash.style.display = 'none';
            });
        });
    }, 5000);
});
