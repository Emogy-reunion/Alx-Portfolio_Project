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




document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.item');

    items.forEach(item => {
        const image = item.querySelector('.image img');

        image.addEventListener('click', function() {
            const propertyId = item.dataset.property_id;

            fetch(`/details/${propertyId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(data => {
                    document.getElementById('details-container').innerHTML = data;
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        });
    });
});
