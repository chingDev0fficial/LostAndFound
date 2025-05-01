// Add this script at the bottom of your template
document.getElementById('lostItemForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Create FormData object
    const formData = new FormData(this);
    
    // Add your form submission logic here
    // Example:
    $.ajax({
        url: 'submit-lost-item/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            if (data.success) {
                alert('Report submitted successfully!');
                $('#lostItemModal').modal('hide');
                $('#lostItemForm')[0].reset(); // Adjust form ID accordingly
            } else {
                alert('Error submitting report. Please try again.');
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('Error submitting report. Please try again.');
        }
    });
});

// $('#submit-btn').click(function() {
//     console.loga('Button clicked!');
// })