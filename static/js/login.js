function checkScreenWidth() {
    if (window.innerWidth > 800) {
        hideSidebar();
    }
}

function showSidebar(){
        const sidebar = document.querySelector('.sidebar')
        sidebar.style.display = 'flex'
}

 function hideSidebar() {
         const sidebar = document.querySelector('.sidebar')
         sidebar.style.display = 'none'
}

document.addEventListener("DOMContentLoaded", function() {
    var links = document.querySelectorAll('nav ul a');

    links.forEach(function(link) {
        link.addEventListener('click', function() {
            // Remove active class from all links
            links.forEach(function(link) {
                link.classList.remove('active');
            });

            // Add active class to the clicked link
            this.classList.add('active');
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(loginForm);
        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Invalid username or password. Please try again.');
            }
        })
        .catch(error => {
            alert(error.message);
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
