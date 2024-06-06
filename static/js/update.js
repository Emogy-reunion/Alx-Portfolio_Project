document.getElementById('update-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch(`/update_property/{{ property1.id }}`, {
        method: 'PATCH',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            window.location.href = '/uploads';
        } else {
            alert(`Failed to update property: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating the property.');
    });
});

