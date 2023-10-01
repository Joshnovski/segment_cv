// Hide flask message after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
      var flashes = document.querySelectorAll('.flash');
      flashes.forEach(function(flash) {
        flash.style.opacity = 0;
        flash.addEventListener('transitionend', function() {
          flash.style.display = 'none';
        });
      });
    }, 3000);
  });