document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(registerForm);
        fetch('/register', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.redirected) {
                // Follow the redirect URL
                window.location.href = response.url;
            } else {
                // Handle other responses here if needed
                console.log('Registration successful');
            }
        })
        .catch(error => {
            const errorContainer = document.getElementById('error-message');
            if (errorContainer) {
                errorContainer.textContent = 'An error occurred during registration.';
                errorContainer.style.display = 'block';
            } else {
                alert('An error occurred during registration.');
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const togglePassword = document.querySelector('.toggle-password');

    togglePassword.addEventListener('click', function() {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            togglePassword.textContent = 'Hide';
        } else {
            passwordInput.type = 'password';
            togglePassword.textContent = 'Show';
        }
    });
});
