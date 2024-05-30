document.addEventListener('DOMContentLoaded', function() {
    var registerForm = document.getElementById('register-form');
    var firstNameInput = document.getElementById('first_name');
    var lastNameInput = document.getElementById('last_name');
    var emailInput = document.getElementById('email');
    var phoneNumberInput = document.getElementById('phone_number');
    var passwordInput = document.getElementById('password');
    var firstNameError = document.getElementById('first-name-error');
    var lastNameError = document.getElementById('last-name-error');
    var emailError = document.getElementById('email-error');
    var phoneNumberError = document.getElementById('phone-number-error');
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

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        firstNameError.textContent = '';
        lastNameError.textContent = '';
        emailError.textContent = '';
        phoneNumberError.textContent = '';
        passwordError.textContent = '';

        var firstName = firstNameInput.value.trim();
        var lastName = lastNameInput.value.trim();
        var email = emailInput.value.trim();
        var phoneNumber = phoneNumberInput.value.trim();
        var password = passwordInput.value.trim();
        var valid = true;

        if (!firstName) {
            firstNameError.textContent = 'First name is required.';
            valid = false;
        }

        if (!lastName) {
            lastNameError.textContent = 'Last name is required.';
            valid = false;
        }

        if (!email) {
            emailError.textContent = 'Email is required.';
            valid = false;
        } else if (!validateEmail(email)) {
            emailError.textContent = 'Invalid email format.';
            valid = false;
        }

        if (!phoneNumber) {
            phoneNumberError.textContent = 'Phone number is required.';
            valid = false;
        }

        if (!password) {
            passwordError.textContent = 'Password is required.';
            valid = false;
        }

        if (valid) {
            var formData = new FormData(registerForm);

            fetch('/register', {
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

