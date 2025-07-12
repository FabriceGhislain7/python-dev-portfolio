// Portfolio Configuration
const CONFIG = {
    // Animation settings
    animation: {
        duration: 600,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
        stagger: 100,
        threshold: 0.1
    },
    
    // Scroll settings
    scroll: {
        offset: 100,
        smooth: true,
        speed: 1000
    },
    
    // Theme settings
    theme: {
        default: 'light',
        storageKey: 'portfolio-theme',
        transition: 300
    },
    
    // Contact form settings
    contact: {
        endpoint: 'https://formspree.io/f/your-form-id', // Replace with your endpoint
        timeout: 10000,
        successMessage: 'Messaggio inviato con successo!',
        errorMessage: 'Errore nell\'invio del messaggio. Riprova più tardi.'
    },
    
    // Loading screen
    loading: {
        minDuration: 1000,
        fadeOutDuration: 500
    },
    
    // Navigation settings
    navigation: {
        stickyOffset: 100,
        mobileBreakpoint: 768,
        activeClass: 'active',
        scrolledClass: 'scrolled'
    },
    
    // Project filters
    projects: {
        animationDelay: 50,
        filterTransition: 300,
        categories: ['all', 'web', 'mobile', 'design']
    },
    
    // Skills animation
    skills: {
        animationDelay: 200,
        progressDuration: 1500,
        countUpDuration: 2000
    },
    
    // Breakpoints
    breakpoints: {
        sm: 640,
        md: 768,
        lg: 1024,
        xl: 1280,
        '2xl': 1536
    },
    
    // API endpoints
    api: {
        skills: 'data/skills.json',
        projects: 'data/projects.json',
        experience: 'data/experience.json',
        testimonials: 'data/testimonials.json'
    },
    
    // Social media links
    social: {
        github: 'https://github.com/yourusername',
        linkedin: 'https://linkedin.com/in/yourusername',
        twitter: 'https://twitter.com/yourusername',
        email: 'mailto:your.email@example.com'
    },
    
    // Performance settings
    performance: {
        debounceDelay: 250,
        throttleDelay: 16,
        intersectionThreshold: 0.1,
        lazyLoadOffset: 50
    }
};

// Export for modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}