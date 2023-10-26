// Wait until the document's content has fully loaded before executing the function.
document.addEventListener('DOMContentLoaded', function() { 
    // Attach an event listener to the window object that listens for the 'resize' event.
    window.addEventListener('resize', function() { 
        // Get the enlarged card element (the parent) and its histogram-container child.
        var parent = document.querySelector('.enlarged-card'); 
        var child = document.querySelector('.enlarged-card .histogram-container');
        console.log(parent, child); // Log both elements to the console for debugging.
        // Ensure both the parent and child elements exist before proceeding.
        if (parent && child) { 
            // Get the current width of the parent element.
            var parentWidth = parent.offsetWidth;
            // This is the original width of the histogram for scaling calculations.
            var originalWidth = 700;
            // Calculate the scale value based on the parent's current width relative to the histogram's original width.
            var scaleValue = (parentWidth/originalWidth)/1.5;
            // var mediaQuery = window.matchMedia("(max-width: 880px)");
            // if (mediaQuery.matches) {
            //     scaleValue = (parentWidth/originalWidth)/2.5; // Adjust the scaling factor for smaller screens.
            // }
            // Apply the scaling transformation to the child (histogram-container).
            child.style.transform = 'scale(' + scaleValue + ')';
        }
    });
});
                                                                                                                                                                                                      
