// Add this script at the bottom of your template
document.getElementById('lostItemForm').addEventListener('submit', function(e) {
    e.preventDefault();

    document.getElementById('loadingOverlay').classList.remove('d-none');
    
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
            console.log("Hello")
            if (data.success) {
                console.log(`Data: ${data}`)
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
        },
        complete: function() {
            // Hide loading overlay
            document.getElementById('loadingOverlay').classList.add('d-none');
        }
    });
});

// $('#submit-btn').click(function() {
//     console.loga('Button clicked!');
// })

// Handle image upload and ML prediction
function predictCategory(input) {
    console.log('Predecting...1')
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

    document.getElementById('loadingOverlay').classList.remove('d-none');
    
    const formData = new FormData(this);
    
    $.ajax({
        url: 'submit-found-item/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            if (data.success) {
                console.log(data)
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
        },
        complete: function() {
            // Hide loading overlay
            document.getElementById('loadingOverlay').classList.add('d-none');
        }
    });
});

let stream = null;

function handleImageUpload(input) {
    console.log('Predecting...2')
    const preview = document.getElementById('preview');
    const file = input.files[0];

    if (file) {
        console.log('File selected:', file.name);
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.remove('d-none');
            predictCategory(input);
        }

        reader.onerror = function(e) {
            console.error('Error loading file:', e);
        }
        
        reader.readAsDataURL(file);
    } else {
        console.log('No file selected');
    }
}

// Add direct event listener to file input
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('itemImage');
    if (fileInput) {
        // Remove required attribute when hidden
        // fileInput.removeAttribute('required');
        
        fileInput.addEventListener('change', function() {
            console.log('File input changed');
            handleImageUpload(this);
        });
    }
});

function openCamera() {
    const video = document.getElementById('cameraPreview');
    const preview = document.getElementById('preview');
    
    // Hide the preview and show video
    preview.classList.add('d-none');
    video.classList.remove('d-none');
    
    navigator.mediaDevices.getUserMedia({ 
        video: { 
            facingMode: 'environment',
            width: { ideal: 1280 },
            height: { ideal: 720 }
        }, 
        audio: false 
    })
    .then(function(mediaStream) {
        stream = mediaStream;
        video.srcObject = mediaStream;
        
        // Create capture button if it doesn't exist
        if (!document.getElementById('captureBtn')) {
            const captureBtn = document.createElement('button');
            captureBtn.id = 'captureBtn';
            captureBtn.className = 'btn btn-color mt-2';
            captureBtn.innerHTML = '<i class="fas fa-camera"></i> Capture Photo';
            captureBtn.onclick = capturePhoto;
            video.parentElement.insertBefore(captureBtn, video.nextSibling);
        }
    })
    .catch(function(error) {
        console.error("Camera error: ", error);
        alert("Unable to access camera. Please check permissions.");
    });
}

function capturePhoto() {
    const video = document.getElementById('cameraPreview');
    const canvas = document.getElementById('imageCanvas');
    const preview = document.getElementById('preview');
    const captureBtn = document.getElementById('captureBtn');
    
    // Set canvas size to video size
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    // Convert canvas to blob
    canvas.toBlob(function(blob) {
        const file = new File([blob], "camera-capture.jpg", { type: "image/jpeg" });
        
        // Create a preview
        preview.src = URL.createObjectURL(blob);
        preview.classList.remove('d-none');
        
        // Stop camera stream and hide video
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        video.classList.add('d-none');
        
        // Remove capture button
        if (captureBtn) {
            captureBtn.remove();
        }

        // Add file to input
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        document.getElementById('itemImage').files = dataTransfer.files;
        
        // Trigger prediction
        predictCategory(document.getElementById('itemImage'));
    }, 'image/jpeg');
}

// // Add this if you haven't implemented predictCategory yet
// function predictCategory(input) {
//     // Your ML prediction code here
//     console.log("Predicting category for uploaded image...");
// }