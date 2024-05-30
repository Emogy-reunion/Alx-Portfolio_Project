document.addEventListener('DOMContentLoaded', function() {
    var loginForm = document.getElementById('login-form');
    var emailInput = document.getElementById('email');
    var passwordInput = document.getElementById('password');
    var emailError = document.getElementById('email-error');
    var passwordError = document.getElementById('password-error');
    var togglePassword = document.querySelector('.toggle-password');

    togglePassword.addEventListener('click', function() {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            togglePassword.textContent = 'Hide';
        } else {
            passwordInput.type = 'password';
            togglePassword.textContent = 'Show';
        }
    });

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        emailError.textContent = '';
        passwordError.textContent = '';

        var email = emailInput.value.trim();
        var password = passwordInput.value.trim();
        var valid = true;

        if (!email) {
            emailError.textContent = 'Email is required.';
            valid = false;
        } else if (!validateEmail(email)) {
            emailError.textContent = 'Invalid email format.';
            valid = false;
        }

        if (!password) {
            passwordError.textContent = 'Password is required.';
            valid = false;
        }

        if (valid) {
            var formData = new FormData(loginForm);

            fetch('/login', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(function(response) {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.text();
                }
            })
            .then(function(text) {
                if (text) {
                    alert(text);
                }
            })
            .catch(function(error) {
                console.error('Error:', error);
                alert('An error occurred while submitting the form.');
            });
        }
    });

    function validateEmail(email) {
        var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});

