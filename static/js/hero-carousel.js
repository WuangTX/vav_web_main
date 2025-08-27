/**
 * VAV Furniture - Hero Carousel Manager
 * Enhanced carousel with thumbnails, auto-play, and touch support
 */

class HeroCarousel {
    constructor(carouselId, options = {}) {
        this.carousel = document.getElementById(carouselId);
        this.options = {
            interval: options.interval || 5000,
            wrap: options.wrap !== false,
            touch: options.touch !== false,
            keyboard: options.keyboard !== false,
            pauseOnHover: options.pauseOnHover !== false,
            ...options
        };
        
        this.isInitialized = false;
        this.init();
    }
    
    init() {
        if (!this.carousel || this.isInitialized) return;
        
        // Initialize Bootstrap carousel
        this.bootstrapCarousel = new bootstrap.Carousel(this.carousel, {
            interval: this.options.interval,
            wrap: this.options.wrap,
            touch: this.options.touch
        });
        
        this.setupEventListeners();
        this.setupThumbnails();
        this.setupAccessibility();
        
        if (this.options.keyboard) {
            this.setupKeyboardNavigation();
        }
        
        if (this.options.touch) {
            this.setupTouchNavigation();
        }
        
        this.isInitialized = true;
        console.log('Hero Carousel initialized successfully');
    }
    
    setupEventListeners() {
        // Carousel slide events
        this.carousel.addEventListener('slide.bs.carousel', (event) => {
            this.updateThumbnails(event.to);
            this.announceSlideChange(event.to);
        });
        
        // Pause on hover
        if (this.options.pauseOnHover) {
            this.carousel.addEventListener('mouseenter', () => this.pause());
            this.carousel.addEventListener('mouseleave', () => this.cycle());
        }
        
        // Intersection Observer for performance
        this.setupIntersectionObserver();
    }
    
    setupThumbnails() {
        const thumbnails = this.carousel.querySelectorAll('.thumbnail-btn');
        
        thumbnails.forEach((thumbnail, index) => {
            thumbnail.addEventListener('click', (e) => {
                e.preventDefault();
                this.goToSlide(index);
            });
            
            // Hover effects
            thumbnail.addEventListener('mouseenter', () => this.pause());
            thumbnail.addEventListener('mouseleave', () => this.cycle());
        });
    }
    
    setupAccessibility() {
        const slides = this.carousel.querySelectorAll('.carousel-item');
        const controls = this.carousel.querySelectorAll('.carousel-control-prev, .carousel-control-next');
        
        // Add ARIA labels
        slides.forEach((slide, index) => {
            slide.setAttribute('aria-label', `Slide ${index + 1} of ${slides.length}`);
        });
        
        // Enhance control buttons
        controls.forEach(control => {
            control.addEventListener('mouseenter', () => this.pause());
            control.addEventListener('mouseleave', () => this.cycle());
        });
    }
    
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (!this.isCarouselInView()) return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    this.prev();
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    this.next();
                    break;
                case 'Home':
                    e.preventDefault();
                    this.goToSlide(0);
                    break;
                case 'End':
                    e.preventDefault();
                    const lastIndex = this.carousel.querySelectorAll('.carousel-item').length - 1;
                    this.goToSlide(lastIndex);
                    break;
                case ' ':
                case 'Enter':
                    if (e.target.classList.contains('thumbnail-btn')) {
                        e.preventDefault();
                        e.target.click();
                    }
                    break;
            }
        });
    }
    
    setupTouchNavigation() {
        let startX = 0;
        let startY = 0;
        let endX = 0;
        let endY = 0;
        
        this.carousel.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        }, { passive: true });
        
        this.carousel.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            this.handleSwipe(startX, startY, endX, endY);
        }, { passive: true });
    }
    
    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.cycle();
                } else {
                    this.pause();
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(this.carousel);
    }
    
    handleSwipe(startX, startY, endX, endY) {
        const threshold = 50;
        const restraint = 100;
        const allowedTime = 300;
        
        const diffX = startX - endX;
        const diffY = Math.abs(startY - endY);
        
        // Check if it's a horizontal swipe
        if (Math.abs(diffX) > threshold && diffY < restraint) {
            if (diffX > 0) {
                this.next(); // Swipe left - next slide
            } else {
                this.prev(); // Swipe right - previous slide
            }
        }
    }
    
    updateThumbnails(activeIndex) {
        const thumbnails = this.carousel.querySelectorAll('.thumbnail-btn');
        
        thumbnails.forEach((thumbnail, index) => {
            if (index === activeIndex) {
                thumbnail.classList.add('active');
                thumbnail.setAttribute('aria-pressed', 'true');
            } else {
                thumbnail.classList.remove('active');
                thumbnail.setAttribute('aria-pressed', 'false');
            }
        });
    }
    
    announceSlideChange(slideIndex) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = `Slide ${slideIndex + 1} is now active`;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }
    
    isCarouselInView() {
        const rect = this.carousel.getBoundingClientRect();
        return rect.top < window.innerHeight && rect.bottom > 0;
    }
    
    // Public methods
    next() {
        this.bootstrapCarousel.next();
    }
    
    prev() {
        this.bootstrapCarousel.prev();
    }
    
    goToSlide(index) {
        this.bootstrapCarousel.to(index);
    }
    
    pause() {
        this.bootstrapCarousel.pause();
    }
    
    cycle() {
        this.bootstrapCarousel.cycle();
    }
    
    dispose() {
        this.bootstrapCarousel.dispose();
        this.isInitialized = false;
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const heroCarouselElement = document.getElementById('heroCarousel');
    
    if (heroCarouselElement) {
        window.heroCarousel = new HeroCarousel('heroCarousel', {
            interval: 5000,
            wrap: true,
            touch: true,
            keyboard: true,
            pauseOnHover: true
        });
    }
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HeroCarousel;
}
