document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility for password1 field
    const togglePasswordButton1 = document.getElementById('toggle-password1');
    const passwordField1 = document.getElementById('password1');

    togglePasswordButton1.addEventListener('click', function() {
        if (passwordField1.type === 'password') {
            passwordField1.type = 'text';
            togglePasswordButton1.textContent = 'Hide';
        } else {
            passwordField1.type = 'password';
            togglePasswordButton1.textContent = 'Show';
        }
    });

    // Toggle password visibility for password2 field
    const togglePasswordButton2 = document.getElementById('toggle-password2');
    const passwordField2 = document.getElementById('password2');

    togglePasswordButton2.addEventListener('click', function() {
        if (passwordField2.type === 'password') {
            passwordField2.type = 'text';
            togglePasswordButton2.textContent = 'Hide';
        } else {
            passwordField2.type = 'password';
            togglePasswordButton2.textContent = 'Show';
        }
    });
});
