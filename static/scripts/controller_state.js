document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#store-parameters');

    form.querySelectorAll('input').forEach(input => {
        input.addEventListener('change', function() {
            // Process the form
            var formData = new FormData(form);
            fetch('/store-parameters', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Data saved successfully");
                } else {
                    console.error("Error saving data");
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

