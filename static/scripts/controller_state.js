console.log("controller_state.js loaded");                                                                                                                                                                                                                    
// Run this code when the page loads                                                                                                                                                                              
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOMContentLoaded");                                                                                                                                                        
    // Get all the collapsible elements                                                                                                                                                                             
    var collapses = document.querySelectorAll('[data-bs-toggle="collapse"]');
    console.log("Number of collapses: " + collapses.length);                                                                                                                                      
                                                                                                                                                                                                                    
    collapses.forEach(function(collapse) {
        console.log("Processing a collapse element");                                                                                                                                                                          
        var id = collapse.getAttribute('data-bs-target');                                                                                                                                                            
                                                                                                                                                                                                                    
        // Check the state in local storage                                                                                                                                                                           
        if (localStorage.getItem(id) === 'show') {                                                                                                                                                                    
            var bsCollapse = new bootstrap.Collapse(collapse, {toggle: false});                                                                                                                                         
            bsCollapse.show();    
            console.log("ram");                                                                                                                                                                                      
        }                                                                                                                                                                                                             
                                                                                                                                                                                                                    
        // Add event listeners to update the state in local storage
        // Event listener for when the collapse starts to show                                                                                                                                                   
        collapse.addEventListener('show.bs.collapse', function() {                                                                                                                                                    
            localStorage.setItem(id, 'show');
            console.log("show");                                                                                                                                                                           
        });                                                                                                                                                                                                           
        // Event listener for when the collapse starts to hide
        collapse.addEventListener('hide.bs.collapse', function() {                                                                                                                                                                                                              
            localStorage.setItem(id, 'hide');
            console.log("hide");
        });
        collapse.addEventListener('click', function() {
            console.log("Collapse clicked");
        });
    });
});