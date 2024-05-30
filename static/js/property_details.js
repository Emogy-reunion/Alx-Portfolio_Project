document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('inquiry');
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();

        var userId = form.dataset.userid;
        var formData = new FormData(form);
        var url = `/send_email/${userId}`;

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(function(response) {
            if (response.ok) {
                alert('Email sent successfully');
            } else {
                return response.text().then(function(text) {
                    throw new Error(text);
                });
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            alert('Failed to send email: ' + error.message);
        });
    });
});


const slides = document.querySelector('.slides');
const slideCount = document.querySelectorAll('.slide').length;
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');
let currentIndex = 0;

prevButton.addEventListener('click', () => {
    moveToPrevSlide();
});

nextButton.addEventListener('click', () => {
    moveToNextSlide();
});

function moveToPrevSlide() {
    currentIndex = (currentIndex === 0) ? slideCount - 1 : currentIndex - 1;
    updateSlidePosition();
}

function moveToNextSlide() {
    currentIndex = (currentIndex === slideCount - 1) ? 0 : currentIndex + 1;
    updateSlidePosition();
}

function updateSlidePosition() {
    const offset = -currentIndex * 100;
    slides.style.transform = `translateX(${offset}%)`;
}
