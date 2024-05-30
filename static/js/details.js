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
