document.addEventListener('DOMContentLoaded', function() {
    const popup = document.querySelector('.popup-logo');
    popup.classList.add('animate-on-load');
    
    // Remove animation class after it's done
    popup.addEventListener('animationend', function() {
        popup.classList.remove('animate-on-load');
        popup.classList.add('show');
    });
});

function toggleLogo() {
    const popup = document.querySelector('.popup-logo');
    popup.classList.toggle('show');
}

// Close popup when clicking outside
document.addEventListener('click', function(event) {
    const popup = document.querySelector('.popup-logo');
    const button = document.querySelector('.logo-button');
    if (!popup.contains(event.target) && !button.contains(event.target)) {
        popup.classList.remove('show');
    }
});