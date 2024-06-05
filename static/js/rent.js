idocument.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.item');

    items.forEach(item => {
        item.addEventListener('click', function() {
            const propertyId = this.dataset.property_id;

            fetch(`/property_details/${propertyId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    // Handle the response if necessary
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        });
    });
});


window.onload = checkScreenWidth;
window.onresize = checkScreenWidth;

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
