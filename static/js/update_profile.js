document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('update-profile-form');
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        var formData = new FormData(form);
        
        fetch('/update_profile', {
            method: 'PATCH',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Failed to update profile');
            }
        })
        .then(data => {
            alert('Profile updated successfully');
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating profile');
        });
    });
});
