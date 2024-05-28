document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.item');

    items.forEach(item => {
        item.addEventListener('click', function() {
            const propertyId = this.dataset.property_id;

            fetch(`/property_details/${propertyId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        });
    });
});

