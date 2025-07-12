// Navigation Management Module

const NavigationManager = {
    // Initialize navigation
    init() {
        this.header = Utils.dom.get('#header');
        this.nav = Utils.dom.get('.nav');
        this.navMenu = Utils.dom.get('#nav-menu');
        this.menuToggle = Utils.dom.get('#menu-toggle');
        this.navLinks = Utils.dom.getAll('.nav-link');
        
        this.isMenuOpen = false;
        this.lastScrollY = window.scrollY;
        this.scrollDirection = 'up';
        
        this.setupEventListeners();
        this.updateActiveLink();
        
        console.log('Navigation Manager initialized');
    },
    
    // Setup event listeners
    setupEventListeners() {
        // Mobile menu toggle
        if (this.menuToggle) {
            this.menuToggle.addEventListener('click', () => {
                this.toggleMobileMenu();
            });
        }
        
        // Navigation links
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                this.handleNavClick(e, link);
            });
        });
        
        // Scroll events
        const throttledScroll = Utils.events.throttle(() => {
            this.handleScroll();
        }, CONFIG.performance.throttleDelay);
        
        window.addEventListener('scroll', throttledScroll);
        
        // Resize events
        const debouncedResize = Utils.events.debounce(() => {
            this.handleResize();
        }, CONFIG.performance.debounceDelay);
        
        window.addEventListener('resize', debouncedResize);
        
        // Close mobile menu on outside click
        document.addEventListener('click', (e) => {
            if (this.isMenuOpen && !this.nav.contains(e.target)) {
                this.closeMobileMenu();
            }
        });
        
        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isMenuOpen) {
                this.closeMobileMenu();
            }
        });
    },
    
    // Handle navigation link clicks
    handleNavClick(e, link) {
        e.preventDefault();
        
        const href = link.getAttribute('href');
        
        // Handle anchor links
        if (href.startsWith('#')) {
            const targetId = href.substring(1);
            const targetElement = Utils.dom.get(`#${targetId}`);
            
            if (targetElement) {
                // Close mobile menu if open
                if (this.isMenuOpen) {
                    this.closeMobileMenu();
                }
                
                // Smooth scroll to target
                Utils.animation.scrollTo(
                    targetElement, 
                    CONFIG.scroll.speed, 
                    CONFIG.scroll.offset
                );
                
                // Update active link
                this.setActiveLink(link);
                
                // Update URL without jumping
                history.pushState(null, null, href);
            }
        }
    },
    
    // Handle scroll events
    handleScroll() {
        const currentScrollY = window.scrollY;
        
        // Update scroll direction
        this.scrollDirection = currentScrollY > this.lastScrollY ? 'down' : 'up';
        this.lastScrollY = currentScrollY;
        
        // Add/remove scrolled class to header
        if (currentScrollY > CONFIG.navigation.stickyOffset) {
            Utils.dom.addClass(this.header, CONFIG.navigation.scrolledClass);
        } else {
            Utils.dom.removeClass(this.header, CONFIG.navigation.scrolledClass);
        }
        
        // Hide/show header on mobile when scrolling
        if (Utils.device.isMobile()) {
            if (this.scrollDirection === 'down' && currentScrollY > 100) {
                Utils.dom.addClass(this.header, 'header-hidden');
            } else {
                Utils.dom.removeClass(this.header, 'header-hidden');
            }
        }
        
        // Update active navigation link based on scroll position
        this.updateActiveLink();
    },
    
    // Handle resize events
    handleResize() {
        // Close mobile menu on desktop
        if (!Utils.device.isMobile() && this.isMenuOpen) {
            this.closeMobileMenu();
        }
    },
    
    // Toggle mobile menu
    toggleMobileMenu() {
        if (this.isMenuOpen) {
            this.closeMobileMenu();
        } else {
            this.openMobileMenu();
        }
    },
    
    // Open mobile menu
    openMobileMenu() {
        this.isMenuOpen = true;
        Utils.dom.addClass(this.menuToggle, 'active');
        Utils.dom.addClass(this.navMenu, 'mobile-menu-open');
        Utils.dom.addClass(document.body, 'menu-open');
        
        // Animate menu items
        const menuItems = this.navMenu.querySelectorAll('.nav-item');
        Utils.animation.stagger(menuItems, 'fade-in-up', 50);
        
        // Update ARIA attributes
        this.menuToggle.setAttribute('aria-expanded', 'true');
        this.navMenu.setAttribute('aria-hidden', 'false');
        
        // Focus first menu item
        const firstLink = this.navMenu.querySelector('.nav-link');
        if (firstLink) firstLink.focus();
    },
    
    // Close mobile menu
    closeMobileMenu() {
        this.isMenuOpen = false;
        Utils.dom.removeClass(this.menuToggle, 'active');
        Utils.dom.removeClass(this.navMenu, 'mobile-menu-open');
        Utils.dom.removeClass(document.body, 'menu-open');
        
        // Update ARIA attributes
        this.menuToggle.setAttribute('aria-expanded', 'false');
        this.navMenu.setAttribute('aria-hidden', 'true');
        
        // Return focus to menu toggle
        this.menuToggle.focus();
    },
    
    // Update active navigation link based on scroll position
    updateActiveLink() {
        const sections = Utils.dom.getAll('section[id]');
        let currentSection = '';
        
        sections.forEach(section => {
            const sectionTop = Utils.dom.getPosition(section).top;
            const sectionHeight = section.offsetHeight;
            const scrollPosition = window.scrollY + CONFIG.scroll.offset + 100;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
            }
        });
        
        // Update active link
        this.navLinks.forEach(link => {
            const href = link.getAttribute('href');
            Utils.dom.removeClass(link, CONFIG.navigation.activeClass);
            
            if (href === `#${currentSection}`) {
                Utils.dom.addClass(link, CONFIG.navigation.activeClass);
            }
        });
    },
    
    // Set active link manually
    setActiveLink(activeLink) {
        this.navLinks.forEach(link => {
            Utils.dom.removeClass(link, CONFIG.navigation.activeClass);
        });
        Utils.dom.addClass(activeLink, CONFIG.navigation.activeClass);
    },
    
    // Navigate to section programmatically
    navigateToSection(sectionId) {
        const targetElement = Utils.dom.get(`#${sectionId}`);
        if (targetElement) {
            Utils.animation.scrollTo(
                targetElement, 
                CONFIG.scroll.speed, 
                CONFIG.scroll.offset
            );
            
            // Update active link
            const targetLink = Utils.dom.get(`a[href="#${sectionId}"]`);
            if (targetLink) {
                this.setActiveLink(targetLink);
            }
        }
    },
    
    // Get current section
    getCurrentSection() {
        const sections = Utils.dom.getAll('section[id]');
        let currentSection = '';
        
        sections.forEach(section => {
            const sectionTop = Utils.dom.getPosition(section).top;
            const sectionHeight = section.offsetHeight;
            const scrollPosition = window.scrollY + CONFIG.scroll.offset + 100;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
            }
        });
        
        return currentSection;
    }
};

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    NavigationManager.init();
});

// Export for other modules
window.NavigationManager = NavigationManager;