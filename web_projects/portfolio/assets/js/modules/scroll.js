// Scroll Management Module

const ScrollManager = {
    // Initialize scroll management
    init() {
        this.lastScrollY = 0;
        this.scrollDirection = 'up';
        this.isScrolling = false;
        this.scrollTimer = null;
        
        this.setupScrollObserver();
        this.setupSmoothScroll();
        this.setupScrollIndicator();
        this.setupProgressBar();
        
        console.log('Scroll Manager initialized');
    },
    
    // Setup scroll event observer
    setupScrollObserver() {
        const throttledScroll = Utils.events.throttle(() => {
            this.handleScroll();
        }, CONFIG.performance.throttleDelay);
        
        window.addEventListener('scroll', throttledScroll, { passive: true });
        
        // Detect scroll start/end
        window.addEventListener('scroll', () => {
            this.isScrolling = true;
            Utils.dom.addClass(document.body, 'is-scrolling');
            
            clearTimeout(this.scrollTimer);
            this.scrollTimer = setTimeout(() => {
                this.isScrolling = false;
                Utils.dom.removeClass(document.body, 'is-scrolling');
            }, 150);
        }, { passive: true });
    },
    
    // Handle scroll events
    handleScroll() {
        const currentScrollY = window.pageYOffset;
        
        // Update scroll direction
        this.scrollDirection = currentScrollY > this.lastScrollY ? 'down' : 'up';
        this.lastScrollY = currentScrollY;
        
        // Update scroll progress
        this.updateScrollProgress();
        
        // Handle header visibility
        this.handleHeaderVisibility(currentScrollY);
        
        // Update scroll indicator
        this.updateScrollIndicator();
        
        // Trigger custom scroll event
        Utils.events.trigger(window, 'customScroll', {
            scrollY: currentScrollY,
            direction: this.scrollDirection,
            progress: this.getScrollProgress()
        });
    },
    
    // Update scroll progress bar
    updateScrollProgress() {
        const progressBar = Utils.dom.get('.scroll-progress');
        if (!progressBar) return;
        
        const progress = this.getScrollProgress();
        progressBar.style.width = `${progress}%`;
    },
    
    // Calculate scroll progress percentage
    getScrollProgress() {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        const scrollTop = window.pageYOffset;
        
        const maxScroll = documentHeight - windowHeight;
        return maxScroll > 0 ? (scrollTop / maxScroll) * 100 : 0;
    },
    
    // Handle header visibility based on scroll
    handleHeaderVisibility(scrollY) {
        const header = Utils.dom.get('#header');
        if (!header) return;
        
        const scrollThreshold = 100;
        const isMobile = Utils.device.isMobile();
        
        // Add scrolled class
        if (scrollY > CONFIG.navigation.stickyOffset) {
            Utils.dom.addClass(header, 'scrolled');
        } else {
            Utils.dom.removeClass(header, 'scrolled');
        }
        
        // Hide/show header on mobile scroll
        if (isMobile) {
            if (this.scrollDirection === 'down' && scrollY > scrollThreshold) {
                Utils.dom.addClass(header, 'header-hidden');
            } else if (this.scrollDirection === 'up') {
                Utils.dom.removeClass(header, 'header-hidden');
            }
        }
    },
    
    // Setup smooth scrolling for anchor links
    setupSmoothScroll() {
        // Handle hash links on page load
        if (window.location.hash) {
            setTimeout(() => {
                this.scrollToElement(window.location.hash);
            }, 100);
        }
        
        // Handle all internal anchor links
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href^="#"]');
            if (!link) return;
            
            e.preventDefault();
            
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = Utils.dom.get(`#${targetId}`);
            
            if (targetElement) {
                this.scrollToElement(targetElement);
                
                // Update URL without triggering scroll
                history.pushState(null, null, `#${targetId}`);
            }
        });
    },
    
    // Scroll to specific element with smooth animation
    scrollToElement(target, options = {}) {
        const element = typeof target === 'string' ? 
            Utils.dom.get(target.startsWith('#') ? target : `#${target}`) : target;
        
        if (!element) return;
        
        const defaultOptions = {
            duration: CONFIG.scroll.speed,
            offset: CONFIG.scroll.offset,
            easing: 'easeInOutCubic'
        };
        
        const settings = { ...defaultOptions, ...options };
        
        // Calculate target position
        const elementTop = Utils.dom.getPosition(element).top;
        const targetPosition = Math.max(0, elementTop - settings.offset);
        
        // Perform smooth scroll
        Utils.animation.scrollTo(element, settings.duration, settings.offset);
        
        // Focus element for accessibility
        setTimeout(() => {
            if (element.tabIndex < 0) {
                element.tabIndex = -1;
            }
            element.focus({ preventScroll: true });
        }, settings.duration);
    },
    
    // Setup scroll indicator
    setupScrollIndicator() {
        const scrollIndicator = Utils.dom.get('.scroll-indicator');
        if (!scrollIndicator) return;
        
        scrollIndicator.addEventListener('click', () => {
            const targetSection = Utils.dom.get('#about') || Utils.dom.get('section:nth-of-type(2)');
            if (targetSection) {
                this.scrollToElement(targetSection);
            }
        });
        
        // Hide indicator when scrolled
        window.addEventListener('scroll', Utils.events.throttle(() => {
            if (window.pageYOffset > 100) {
                Utils.dom.addClass(scrollIndicator, 'hidden');
            } else {
                Utils.dom.removeClass(scrollIndicator, 'hidden');
            }
        }, 100));
    },
    
    // Setup scroll progress bar
    setupProgressBar() {
        // Create progress bar if it doesn't exist
        let progressBar = Utils.dom.get('.scroll-progress');
        
        if (!progressBar) {
            progressBar = Utils.dom.create('div', 'scroll-progress');
            progressBar.innerHTML = '<div class="scroll-progress-fill"></div>';
            document.body.appendChild(progressBar);
        }
        
        // Update progress on scroll
        this.updateScrollProgress();
    },
    
    // Get current section in viewport
    getCurrentSection() {
        const sections = Utils.dom.getAll('section[id]');
        let currentSection = null;
        let maxVisibility = 0;
        
        sections.forEach(section => {
            const rect = section.getBoundingClientRect();
            const viewportHeight = window.innerHeight;
            
            // Calculate visibility percentage
            const visibleTop = Math.max(0, -rect.top);
            const visibleBottom = Math.min(rect.height, viewportHeight - rect.top);
            const visibleHeight = Math.max(0, visibleBottom - visibleTop);
            const visibility = (visibleHeight / rect.height) * 100;
            
            if (visibility > maxVisibility && visibility > 20) {
                maxVisibility = visibility;
                currentSection = section;
            }
        });
        
        return currentSection;
    },
    
    // Check if element is in viewport
    isElementInViewport(element, threshold = 0.1) {
        return Utils.dom.isInViewport(element, threshold);
    },
    
    // Get elements currently in viewport
    getElementsInViewport(selector, threshold = 0.1) {
        const elements = Utils.dom.getAll(selector);
        return Array.from(elements).filter(element => 
            this.isElementInViewport(element, threshold)
        );
    },
    
    // Scroll to top of page
    scrollToTop(duration = 800) {
        Utils.animation.scrollTo(document.body, duration, 0);
    },
    
    // Scroll to bottom of page
    scrollToBottom(duration = 800) {
        const targetPosition = document.documentElement.scrollHeight - window.innerHeight;
        
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        let startTime = null;
        
        const easeInOutCubic = (t) => {
            return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
        };
        
        const animation = (currentTime) => {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const progress = Math.min(timeElapsed / duration, 1);
            
            window.scrollTo(0, startPosition + distance * easeInOutCubic(progress));
            
            if (progress < 1) {
                requestAnimationFrame(animation);
            }
        };
        
        requestAnimationFrame(animation);
    },
    
    // Enable/disable scrolling
    toggleScrolling(enable = true) {
        if (enable) {
            Utils.dom.removeClass(document.body, 'no-scroll');
        } else {
            Utils.dom.addClass(document.body, 'no-scroll');
        }
    },
    
    // Lock scroll (useful for modals)
    lockScroll() {
        this.scrollPosition = window.pageYOffset;
        Utils.dom.addClass(document.body, 'scroll-locked');
        document.body.style.top = `-${this.scrollPosition}px`;
    },
    
    // Unlock scroll
    unlockScroll() {
        Utils.dom.removeClass(document.body, 'scroll-locked');
        document.body.style.top = '';
        
        if (this.scrollPosition !== undefined) {
            window.scrollTo(0, this.scrollPosition);
        }
    },
    
    // Update scroll indicator visibility
    updateScrollIndicator() {
        const indicator = Utils.dom.get('.scroll-indicator');
        if (!indicator) return;
        
        // Hide when near bottom
        const scrollProgress = this.getScrollProgress();
        if (scrollProgress > 90) {
            Utils.dom.addClass(indicator, 'hidden');
        } else if (scrollProgress < 10) {
            Utils.dom.removeClass(indicator, 'hidden');
        }
    },
    
    // Setup infinite scroll (if needed)
    setupInfiniteScroll(callback, threshold = 200) {
        const handleInfiniteScroll = Utils.events.throttle(() => {
            const scrollHeight = document.documentElement.scrollHeight;
            const scrollTop = window.pageYOffset;
            const clientHeight = window.innerHeight;
            
            if (scrollTop + clientHeight >= scrollHeight - threshold) {
                callback();
            }
        }, 250);
        
        window.addEventListener('scroll', handleInfiniteScroll);
        
        return () => {
            window.removeEventListener('scroll', handleInfiniteScroll);
        };
    },
    
    // Setup parallax effects
    setupParallax() {
        const parallaxElements = Utils.dom.getAll('[data-parallax]');
        
        if (parallaxElements.length === 0) return;
        
        const handleParallax = Utils.events.throttle(() => {
            const scrollY = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = parseFloat(element.getAttribute('data-parallax')) || 0.5;
                const rect = element.getBoundingClientRect();
                const elementTop = rect.top + scrollY;
                const elementHeight = rect.height;
                const windowHeight = window.innerHeight;
                
                // Only animate elements in or near viewport
                if (elementTop < scrollY + windowHeight && elementTop + elementHeight > scrollY) {
                    const yPos = -(scrollY - elementTop) * speed;
                    element.style.transform = `translateY(${yPos}px)`;
                }
            });
        }, 16);
        
        window.addEventListener('scroll', handleParallax, { passive: true });
    },
    
    // Scroll spy for navigation
    setupScrollSpy() {
        const sections = Utils.dom.getAll('section[id]');
        const navLinks = Utils.dom.getAll('.nav-link[href^="#"]');
        
        if (sections.length === 0 || navLinks.length === 0) return;
        
        const handleScrollSpy = Utils.events.throttle(() => {
            const currentSection = this.getCurrentSection();
            
            navLinks.forEach(link => {
                Utils.dom.removeClass(link, 'active');
            });
            
            if (currentSection) {
                const activeLink = Utils.dom.get(`a[href="#${currentSection.id}"]`);
                if (activeLink) {
                    Utils.dom.addClass(activeLink, 'active');
                }
            }
        }, 100);
        
        window.addEventListener('scroll', handleScrollSpy);
    },
    
    // Reveal elements on scroll
    revealOnScroll(selector, animationClass = 'fade-in-up', threshold = 0.1) {
        const elements = Utils.dom.getAll(selector);
        
        const observer = Utils.performance.createObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    Utils.dom.addClass(entry.target, animationClass);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold });
        
        elements.forEach(element => {
            observer.observe(element);
        });
        
        return observer;
    },
    
    // Get scroll direction
    getScrollDirection() {
        return this.scrollDirection;
    },
    
    // Get current scroll position
    getScrollPosition() {
        return {
            x: window.pageXOffset,
            y: window.pageYOffset
        };
    },
    
    // Check if scrolled to bottom
    isScrolledToBottom(threshold = 50) {
        const scrollHeight = document.documentElement.scrollHeight;
        const scrollTop = window.pageYOffset;
        const clientHeight = window.innerHeight;
        
        return (scrollTop + clientHeight) >= (scrollHeight - threshold);
    },
    
    // Check if scrolled to top
    isScrolledToTop(threshold = 50) {
        return window.pageYOffset <= threshold;
    },
    
    // Smooth scroll to next section
    scrollToNextSection() {
        const currentSection = this.getCurrentSection();
        if (!currentSection) return;
        
        const sections = Utils.dom.getAll('section[id]');
        const currentIndex = Array.from(sections).indexOf(currentSection);
        const nextSection = sections[currentIndex + 1];
        
        if (nextSection) {
            this.scrollToElement(nextSection);
        }
    },
    
    // Smooth scroll to previous section
    scrollToPreviousSection() {
        const currentSection = this.getCurrentSection();
        if (!currentSection) return;
        
        const sections = Utils.dom.getAll('section[id]');
        const currentIndex = Array.from(sections).indexOf(currentSection);
        const previousSection = sections[currentIndex - 1];
        
        if (previousSection) {
            this.scrollToElement(previousSection);
        }
    },
    
    // Keyboard navigation for sections
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Only handle if no input is focused
            if (document.activeElement.tagName === 'INPUT' || 
                document.activeElement.tagName === 'TEXTAREA') {
                return;
            }
            
            switch (e.key) {
                case 'ArrowDown':
                case 'PageDown':
                    e.preventDefault();
                    this.scrollToNextSection();
                    break;
                    
                case 'ArrowUp':
                case 'PageUp':
                    e.preventDefault();
                    this.scrollToPreviousSection();
                    break;
                    
                case 'Home':
                    e.preventDefault();
                    this.scrollToTop();
                    break;
                    
                case 'End':
                    e.preventDefault();
                    this.scrollToBottom();
                    break;
            }
        });
    },
    
    // Detect scroll performance issues
    detectScrollPerformance() {
        let scrollCount = 0;
        let lastTime = performance.now();
        
        const handlePerformanceCheck = () => {
            scrollCount++;
            const currentTime = performance.now();
            
            if (currentTime - lastTime >= 1000) {
                const fps = scrollCount;
                
                if (fps < 30) {
                    console.warn('Scroll performance is low:', fps, 'fps');
                    Utils.events.trigger(document, 'scroll-performance-warning', { fps });
                }
                
                scrollCount = 0;
                lastTime = currentTime;
            }
        };
        
        window.addEventListener('scroll', handlePerformanceCheck, { passive: true });
    },
    
    // Cleanup scroll manager
    cleanup() {
        // Clear timers
        if (this.scrollTimer) {
            clearTimeout(this.scrollTimer);
        }
        
        // Remove event listeners would need to be tracked if we want full cleanup
        console.log('Scroll Manager cleaned up');
    }
};

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    ScrollManager.init();
    ScrollManager.setupParallax();
    ScrollManager.setupScrollSpy();
    ScrollManager.setupKeyboardNavigation();
});

// Export for other modules
window.ScrollManager = ScrollManager;