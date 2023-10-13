document.addEventListener('DOMContentLoaded', function() {                                                                                                                                                        
    window.addEventListener('resize', function() {                                                                                                                                                                
        var parent = document.querySelector('.enlarged-card');                                                                                                                                                    
        var child = document.querySelector('.enlarged-card .histogram-container');
        console.log(parent, child);                                                                                                                                
        if (parent && child) {                                                                                                                                                                                    
            var parentWidth = parent.offsetWidth;                                                                                                                                                                 
            var originalWidth = 700; // replace this with the original width of the histogram                                                                                                                     
            var scaleValue = (parentWidth/originalWidth)/1.5;
            
            // // Check if media query is active
            // var mediaQuery = window.matchMedia("(max-width: 880px)");
            // if (mediaQuery.matches) {
            //     scaleValue = (parentWidth/originalWidth)/2.5;
            // }
            
            child.style.transform = 'scale(' + scaleValue + ')';                                                                                                                                                  
        }                                                                                                                                                                                                         
    });                                                                                                                                                                                                           
});                                                                                                                                                                                                          