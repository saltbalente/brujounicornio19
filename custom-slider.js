// Custom Slider Implementation to replace missing Elementor carousel functionality
document.addEventListener('DOMContentLoaded', function() {
    // Find the image carousel element
    const carouselElement = document.querySelector('.elementor-widget-image-carousel');
    if (!carouselElement) return;

    const wrapper = carouselElement.querySelector('.elementor-image-carousel');
    const slides = wrapper.querySelectorAll('.swiper-slide');
    const prevButton = carouselElement.querySelector('.elementor-swiper-button-prev');
    const nextButton = carouselElement.querySelector('.elementor-swiper-button-next');
    
    if (slides.length === 0) return;

    let currentIndex = 0;
    let autoplayInterval;
    const autoplaySpeed = 3000; // 3 seconds
    const slidesToShow = window.innerWidth <= 767 ? 1 : 4; // Mobile: 1, Desktop: 4
    
    // Initialize slider
    function initSlider() {
        // Set initial positions
        updateSliderPosition();
        
        // Start autoplay
        startAutoplay();
        
        // Add event listeners
        if (prevButton) {
            prevButton.addEventListener('click', goToPrevSlide);
        }
        
        if (nextButton) {
            nextButton.addEventListener('click', goToNextSlide);
        }
        
        // Pause on hover
        carouselElement.addEventListener('mouseenter', stopAutoplay);
        carouselElement.addEventListener('mouseleave', startAutoplay);
        
        // Handle window resize
        window.addEventListener('resize', handleResize);
    }
    
    function updateSliderPosition() {
        const slideWidth = 100 / slidesToShow;
        const translateX = -(currentIndex * slideWidth);
        
        // Apply transform to wrapper
        wrapper.style.transform = `translateX(${translateX}%)`;
        wrapper.style.transition = 'transform 0.5s ease';
        
        // Update slide widths
        slides.forEach(slide => {
            slide.style.width = `${slideWidth}%`;
            slide.style.flexShrink = '0';
        });
    }
    
    function goToNextSlide() {
        const maxIndex = Math.max(0, slides.length - slidesToShow);
        currentIndex = currentIndex >= maxIndex ? 0 : currentIndex + 1;
        updateSliderPosition();
    }
    
    function goToPrevSlide() {
        const maxIndex = Math.max(0, slides.length - slidesToShow);
        currentIndex = currentIndex <= 0 ? maxIndex : currentIndex - 1;
        updateSliderPosition();
    }
    
    function startAutoplay() {
        stopAutoplay(); // Clear any existing interval
        autoplayInterval = setInterval(goToNextSlide, autoplaySpeed);
    }
    
    function stopAutoplay() {
        if (autoplayInterval) {
            clearInterval(autoplayInterval);
            autoplayInterval = null;
        }
    }
    
    function handleResize() {
        const newSlidesToShow = window.innerWidth <= 767 ? 1 : 4;
        if (newSlidesToShow !== slidesToShow) {
            // Recalculate and update
            location.reload(); // Simple solution for responsive changes
        }
    }
    
    // Initialize the slider
    initSlider();
    
    // Add some basic styling to ensure proper display
    const style = document.createElement('style');
    style.textContent = `
        .elementor-image-carousel-wrapper {
            overflow: hidden;
            position: relative;
        }
        
        .elementor-image-carousel {
            display: flex;
            transition: transform 0.5s ease;
        }
        
        .elementor-image-carousel .swiper-slide {
            flex-shrink: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .elementor-swiper-button {
            opacity: 0.7;
            transition: opacity 0.3s ease;
            z-index: 10;
        }
        
        .elementor-swiper-button:hover {
            opacity: 1;
        }
        
        .elementor-swiper-button-prev::before {
            content: '❮';
            font-size: 24px;
            color: #fff;
            text-shadow: 0 0 3px rgba(0,0,0,0.5);
        }
        
        .elementor-swiper-button-next::before {
            content: '❯';
            font-size: 24px;
            color: #fff;
            text-shadow: 0 0 3px rgba(0,0,0,0.5);
        }
        
        @media (max-width: 767px) {
            .elementor-image-carousel .swiper-slide {
                width: 100% !important;
            }
        }
    `;
    document.head.appendChild(style);
});