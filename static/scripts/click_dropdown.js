function toggleBackgroundColor(event) {
    // Get the element that triggered the event.
    var div = event.currentTarget;
    // Check if the element has the 'active' class.
    if (div.classList.contains('active')) {
        // If the element has the 'active' class, remove it.
        div.classList.remove('active');
    } else {
        // Otherwise, add the 'active' class to the element.
        div.classList.add('active');
    }
}




