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

        // Show loading state
        const category = document.getElementById('predictedCategory');
        category.value = '';
        document.getElementById('mlConfidence-cat').textContent = 'Analyzing image...';

        const item = document.getElementById('foundItemName');
        item.value = ''
        document.getElementById('mlConfidence-item').textContent = 'Analyzing image...';
        // Simulate ML prediction (replace with actual ML endpoint)
        $.ajax({
            url: 'recognize-image/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {

                // console.log(response)

                category.value = `${response.category[0]}`
                document.getElementById('mlConfidence-cat').textContent = `${(response.category[1] * 100).toFixed(1)}%`
                item.value = `${response.item[0]}`
                document.getElementById('mlConfidence-item').textContent = `${(response.item[1] * 100).toFixed(1)}%`
            },
            error: function(xhs, status, error) {
                console.error('Error:', error);
                alert('Error submitting report. Please try again.');
            }
        })
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