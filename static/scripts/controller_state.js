// Ensure that the code runs after the document's content has fully loaded.
document.addEventListener('DOMContentLoaded', function() {
    // Select the form with the ID 'store-parameters'.
    const form = document.querySelector('#store-parameters');
    // Loop over each input element within the form.
    form.querySelectorAll('input').forEach(input => {
        // Add an event listener to each input to detect changes.
        input.addEventListener('change', function() {
            // On change, process the form and create a FormData object.
            var formData = new FormData(form);
            // Send a POST request to '/store-parameters' with the form data.
            fetch('/store-parameters', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json()) // Parse the response to JSON.
            .then(data => {
                // Check the 'success' property of the returned data.
                if (data.success) {
                    console.log("Data saved successfully");
                } else {
                    console.error("Error saving data");
                }
            })
            .catch(error => console.error('Error:', error)); // Log any errors that occur during the fetch process.
        });
    });
});


