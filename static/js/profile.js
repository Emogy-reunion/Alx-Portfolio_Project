document.addEventListener('DOMContentLoaded', function() {
    var editProfileButton = document.getElementById('edit-profile');

    editProfileButton.addEventListener('click', function() {
        window.location.href = '/update_profile';
    });
});
