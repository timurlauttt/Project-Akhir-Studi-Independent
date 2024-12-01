document.addEventListener('DOMContentLoaded', function() {
    // Show/hide password functionality
    const togglePasswordButton = document.getElementById('toggle-password');
    const passwordField = document.getElementById('password');

    togglePasswordButton.addEventListener('click', function() {
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            togglePasswordButton.textContent = 'Hide';
        } else {
            passwordField.type = 'password';
            togglePasswordButton.textContent = 'Show';
        }
    });

    // Aktifkan tombol login jika checkbox Keep Me Logged In dicentang
    const keepLoggedInCheckbox = document.getElementById('keepLoggedIn');
    const loginButton = document.getElementById('login-button');

    keepLoggedInCheckbox.addEventListener('change', function() {
        loginButton.disabled = !keepLoggedInCheckbox.checked;
    });

    // Menampilkan pesan error di modal jika ada
    const djangoMessages = document.querySelectorAll('#django-messages .message');
    djangoMessages.forEach(function(messageElement) {
        const messageText = messageElement.textContent;
        const messageTags = messageElement.getAttribute('data-tags');
        if (messageTags.includes('error')) {
            document.getElementById('error-message').innerText = messageText;
            const errorModal = new bootstrap.Modal(document.getElementById('loginErrorModal'));
            errorModal.show();
        }
    });
});