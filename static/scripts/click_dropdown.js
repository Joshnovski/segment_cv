function toggleBackgroundColor(event) {
    var div = event.currentTarget;

    if (div.classList.contains('active')) {
        div.classList.remove('active');
    } else {
        div.classList.add('active');
    }
}




