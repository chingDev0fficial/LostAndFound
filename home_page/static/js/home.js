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

// Handle image upload and ML prediction
function predictCategory(input) {
    const file = input.files[0];
    if (file) {
        // Show image preview
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').innerHTML = 
                `<img src="${e.target.result}" class="img-fluid" style="max-height: 200px">`;
        }
        reader.readAsDataURL(file);

        // Create FormData and send to ML endpoint
        const formData = new FormData();
        formData.append('image', file);

        // Simulate ML prediction (replace with actual ML endpoint)
        setTimeout(() => {
            const prediction = {
                category: 'wallet',
                confidence: 0.92
            };
            
            // Update UI with prediction
            document.getElementById('predictedCategory').value = prediction.category;
            document.getElementById('mlConfidence').textContent = 
                `Confidence: ${(prediction.confidence * 100).toFixed(1)}%`;
            
            // Suggest item name based on prediction
            document.getElementById('itemName').value = 
                `${prediction.category.charAt(0).toUpperCase() + prediction.category.slice(1)}`;
        }, 1000);
    }
}

// Handle form submission
document.getElementById('foundItemForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    $.ajax({
        url: 'submit-found-item/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            if (data.success) {
                alert('Found item report submitted successfully!');
                $('#foundItemModal').modal('hide');
                $('#foundItemForm')[0].reset();
                document.getElementById('imagePreview').innerHTML = '';
            } else {
                alert('Error: ' + data.message);
            }
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
            alert('Error submitting report. Please try again.');
        }
    });
}); 