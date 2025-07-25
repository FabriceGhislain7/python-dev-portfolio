/*
===========================================
SCROLL MODULE
===========================================
Gestisce smooth scroll, scroll spy, progress bar e animazioni scroll-based
*/

(function() {
    'use strict';

    /* ================================ */
    /* STATO DEL MODULO                 */
    /* ================================ */
    const ScrollState = {
        isInitialized: false,
        currentSection: '',
        scrollPosition: 0,
        isScrolling: false,
        scrollTimeout: null,
        progressBar: null,
        backToTopButton: null,
        sections: [],
        navLinks: [],
        observers: [],
        scrollAnimationFrame: null,
        lastScrollTop: 0,
        scrollDirection: 'down',
        isUserScrolling: true
    };

    /* ================================ */
    /* MODULO PRINCIPALE                */
    /* ================================ */
    const ScrollModule = {
        
        /* ================================ */
        /* INIZIALIZZAZIONE                 */
        /* ================================ */
        init() {
            if (ScrollState.isInitialized) {
                window.PortfolioConfig.utils.log('warn', 'Scroll module already initialized');
                return;
            }

            try {
                window.PortfolioConfig.utils.log('info', 'Initializing Scroll module');
                
                // Setup elementi DOM
                this.setupDOMElements();
                
                // Setup scroll progress bar
                this.setupProgressBar();
                
                // Setup back to top button
                this.setupBackToTop();
                
                // Setup smooth scroll
                this.setupSmoothScroll();
                
                // Setup scroll spy
                this.setupScrollSpy();
                
                // Setup scroll animations
                this.setupScrollAnimations();
                
                // Setup event listeners
                this.setupEventListeners();
                
                // Initial setup
                this.updateScrollState();
                
                ScrollState.isInitialized = true;
                window.PortfolioConfig.utils.log('info', 'Scroll module initialized successfully');
                
            } catch (error) {
                window.PortfolioConfig.utils.log('error', 'Scroll module initialization failed', error);
                this.handleError(error);
            }
        },

        /* ================================ */
        /* SETUP DOM ELEMENTS               */
        /* ================================ */
        setupDOMElements() {
            // Trova tutti i section con ID
            ScrollState.sections = Array.from(document.querySelectorAll('section[id]'));
            
            // Trova tutti i link di navigazione
            ScrollState.navLinks = Array.from(document.querySelectorAll('a[href^="#"]')).filter(link => {
                const href = link.getAttribute('href');
                return href !== '#' && document.querySelector(href);
            });
            
            // Progress bar
            ScrollState.progressBar = document.getElementById('scroll-progress') || this.createProgressBar();
            
            // Back to top button
            ScrollState.backToTopButton = document.getElementById('back-to-top') || this.createBackToTop();
            
            window.PortfolioConfig.utils.log('debug', `Found ${ScrollState.sections.length} sections and ${ScrollState.navLinks.length} nav links`);
        },

        /* ================================ */
        /* CREAZIONE PROGRESS BAR           */
        /* ================================ */
        createProgressBar() {
            if (!window.PortfolioConfig.ui.scroll.progressBarEnabled) {
                return null;
            }

            const progressBar = document.createElement('div');
            progressBar.id = 'scroll-progress';
            progressBar.className = 'scroll-progress';
            progressBar.innerHTML = '<div class="scroll-progress-bar"></div>';
            
            // Stili inline se non definiti nel CSS
            progressBar.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 3px;
                background: rgba(255,255,255,0.1);
                z-index: 1000;
                pointer-events: none;
            `;
            
            const bar = progressBar.querySelector('.scroll-progress-bar');
            bar.style.cssText = `
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
                transition: width 0.1s ease;
            `;
            
            document.body.appendChild(progressBar);
            return progressBar;
        },

        /* ================================ */
        /* CREAZIONE BACK TO TOP            */
        /* ================================ */
        createBackToTop() {
            const button = document.createElement('button');
            button.id = 'back-to-top';
            button.className = 'back-to-top';
            button.innerHTML = '<i class="fas fa-chevron-up"></i>';
            button.setAttribute('aria-label', 'Torna all\'inizio');
            button.setAttribute('title', 'Torna all\'inizio');
            
            // Stili inline se non definiti nel CSS
            button.style.cssText = `
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 50px;
                height: 50px;
                border: none;
                border-radius: 50%;
                background: var(--color-primary);
                color: white;
                font-size: 18px;
                cursor: pointer;
                z-index: 1000;
                opacity: 0;
                visibility: hidden;
                transform: translateY(20px);
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            `;
            
            document.body.appendChild(button);
            return button;
        },

        /* ================================ */
        /* SETUP PROGRESS BAR               */
        /* ================================ */
        setupProgressBar() {
            if (!ScrollState.progressBar) return;
            
            this.updateProgressBar();
        },

        /* ================================ */
        /* SETUP BACK TO TOP                */
        /* ================================ */
        setupBackToTop() {
            if (!ScrollState.backToTopButton) return;
            
            ScrollState.backToTopButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.scrollToTop();
            });
            
            // Setup visibility
            this.updateBackToTopVisibility();
        },

        /* ================================ */
        /* SETUP SMOOTH SCROLL              */
        /* ================================ */
        setupSmoothScroll() {
            ScrollState.navLinks.forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    
                    const targetId = link.getAttribute('href').substring(1);
                    const targetElement = document.getElementById(targetId);
                    
                    if (targetElement) {
                        this.scrollToElement(targetElement);
                        
                        // Update URL without triggering scroll
                        if (history.pushState) {
                            history.pushState(null, null, `#${targetId}`);
                        }
                        
                        // Update active nav
                        this.updateActiveNavigation(targetId);
                        
                        window.PortfolioConfig.utils.log('debug', `Smooth scroll to: ${targetId}`);
                    }
                });
            });
        },

        /* ================================ */
        /* SETUP SCROLL SPY                 */
        /* ================================ */
        setupScrollSpy() {
            // Intersection Observer per le sezioni
            const observerOptions = {
                rootMargin: `-${window.PortfolioConfig.ui.navigation.highlightOffset}px 0px -50% 0px`,
                threshold: 0
            };
            
            const sectionObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const sectionId = entry.target.id;
                        if (sectionId !== ScrollState.currentSection) {
                            ScrollState.currentSection = sectionId;
                            this.updateActiveNavigation(sectionId);
                            
                            // Dispatch evento
                            document.dispatchEvent(new CustomEvent('sectionChanged', {
                                detail: { sectionId, element: entry.target }
                            }));
                        }
                    }
                });
            }, observerOptions);
            
            // Osserva tutte le sezioni
            ScrollState.sections.forEach(section => {
                sectionObserver.observe(section);
            });
            
            ScrollState.observers.push(sectionObserver);
        },

        /* ================================ */
        /* SETUP SCROLL ANIMATIONS          */
        /* ================================ */
        setupScrollAnimations() {
            // Observer per elementi con animazioni scroll-based
            const animationElements = document.querySelectorAll('[data-scroll-animation]');
            
            if (animationElements.length === 0) return;
            
            const animationObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    const element = entry.target;
                    const animationType = element.dataset.scrollAnimation;
                    
                    if (entry.isIntersecting) {
                        this.triggerScrollAnimation(element, animationType);
                    } else if (element.dataset.scrollRepeat === 'true') {
                        this.resetScrollAnimation(element, animationType);
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '50px'
            });
            
            animationElements.forEach(element => {
                animationObserver.observe(element);
            });
            
            ScrollState.observers.push(animationObserver);
        },

        /* ================================ */
        /* SETUP EVENT LISTENERS            */
        /* ================================ */
        setupEventListeners() {
            // Main scroll handler
            const throttledScrollHandler = window.PortfolioConfig.utils.throttle(
                this.handleScroll.bind(this), 
                10
            );
            
            window.addEventListener('scroll', throttledScrollHandler, { passive: true });
            
            // Resize handler
            window.addEventListener('resize', window.PortfolioConfig.utils.debounce(
                this.handleResize.bind(this), 
                250
            ));
            
            // Keyboard navigation
            document.addEventListener('keydown', this.handleKeyboard.bind(this));
            
            // Hash change
            window.addEventListener('hashchange', this.handleHashChange.bind(this));
            
            // Page visibility
            document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
            
            // Portfolio resize event
            document.addEventListener('portfolioResize', this.handlePortfolioResize.bind(this));
        },

        /* ================================ */
        /* GESTIONE EVENTI                  */
        /* ================================ */
        handleScroll() {
            ScrollState.scrollPosition = window.pageYOffset;
            
            // Determina direzione scroll
            if (ScrollState.scrollPosition > ScrollState.lastScrollTop) {
                ScrollState.scrollDirection = 'down';
            } else if (ScrollState.scrollPosition < ScrollState.lastScrollTop) {
                ScrollState.scrollDirection = 'up';
            }
            ScrollState.lastScrollTop = ScrollState.scrollPosition;
            
            // Update UI elements
            this.updateScrollState();
            
            // Set scrolling state
            ScrollState.isScrolling = true;
            clearTimeout(ScrollState.scrollTimeout);
            ScrollState.scrollTimeout = setTimeout(() => {
                ScrollState.isScrolling = false;
                document.dispatchEvent(new CustomEvent('scrollEnd'));
            }, 150);
            
            // Dispatch scroll event
            document.dispatchEvent(new CustomEvent('portfolioScroll', {
                detail: {
                    position: ScrollState.scrollPosition,
                    direction: ScrollState.scrollDirection,
                    isScrolling: ScrollState.isScrolling
                }
            }));
        },

        handleResize() {
            // Re-calcola posizioni dopo resize
            this.updateScrollState();
            window.PortfolioConfig.utils.log('debug', 'Scroll positions recalculated after resize');
        },

        handleKeyboard(e) {
            // Keyboard navigation
            switch (e.key) {
                case 'Home':
                    if (e.ctrlKey) {
                        e.preventDefault();
                        this.scrollToTop();
                    }
                    break;
                case 'End':
                    if (e.ctrlKey) {
                        e.preventDefault();
                        this.scrollToBottom();
                    }
                    break;
                case 'PageUp':
                    e.preventDefault();
                    this.scrollByViewport(-0.8);
                    break;
                case 'PageDown':
                    e.preventDefault();
                    this.scrollByViewport(0.8);
                    break;
                case 'ArrowUp':
                    if (e.ctrlKey) {
                        e.preventDefault();
                        this.scrollToPreviousSection();
                    }
                    break;
                case 'ArrowDown':
                    if (e.ctrlKey) {
                        e.preventDefault();
                        this.scrollToNextSection();
                    }
                    break;
            }
        },

        handleHashChange() {
            const hash = window.location.hash.substring(1);
            if (hash && document.getElementById(hash)) {
                this.scrollToElement(document.getElementById(hash));
            }
        },

        handleVisibilityChange() {
            if (document.visibilityState === 'visible') {
                // Re-sync scroll state quando la pagina diventa visibile
                this.updateScrollState();
            }
        },

        handlePortfolioResize(e) {
            // Gestisce il resize event personalizzato del portfolio
            this.updateScrollState();
        },

        /* ================================ */
        /* AGGIORNAMENTO STATO SCROLL       */
        /* ================================ */
        updateScrollState() {
            this.updateProgressBar();
            this.updateBackToTopVisibility();
            this.updateNavigationState();
        },

        /* ================================ */
        /* AGGIORNAMENTO PROGRESS BAR       */
        /* ================================ */
        updateProgressBar() {
            if (!ScrollState.progressBar) return;
            
            const scrollTop = window.pageYOffset;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
            
            const progressBarElement = ScrollState.progressBar.querySelector('.scroll-progress-bar') || ScrollState.progressBar;
            progressBarElement.style.width = `${Math.min(scrollPercent, 100)}%`;
        },

        /* ================================ */
        /* AGGIORNAMENTO BACK TO TOP        */
        /* ================================ */
        updateBackToTopVisibility() {
            if (!ScrollState.backToTopButton) return;
            
            const shouldShow = ScrollState.scrollPosition > window.PortfolioConfig.ui.scroll.backToTopOffset;
            
            if (shouldShow) {
                ScrollState.backToTopButton.style.opacity = '1';
                ScrollState.backToTopButton.style.visibility = 'visible';
                ScrollState.backToTopButton.style.transform = 'translateY(0)';
            } else {
                ScrollState.backToTopButton.style.opacity = '0';
                ScrollState.backToTopButton.style.visibility = 'hidden';
                ScrollState.backToTopButton.style.transform = 'translateY(20px)';
            }
        },

        /* ================================ */
        /* AGGIORNAMENTO NAVIGAZIONE         */
        /* ================================ */
        updateNavigationState() {
            // Aggiungi/rimuovi classe per navbar quando si scrolla
            const navbar = document.querySelector('.navbar') || document.querySelector('header');
            if (navbar) {
                if (ScrollState.scrollPosition > 100) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
                
                // Nascondi/mostra navbar basato sulla direzione dello scroll
                if (ScrollState.scrollPosition > 200) {
                    if (ScrollState.scrollDirection === 'down' && ScrollState.isUserScrolling) {
                        navbar.classList.add('navbar-hidden');
                    } else if (ScrollState.scrollDirection === 'up') {
                        navbar.classList.remove('navbar-hidden');
                    }
                }
            }
        },

        /* ================================ */
        /* AGGIORNAMENTO NAVIGAZIONE ATTIVA  */
        /* ================================ */
        updateActiveNavigation(activeSectionId) {
            // Rimuovi classe active da tutti i link
            ScrollState.navLinks.forEach(link => {
                link.classList.remove('active');
                const parentLi = link.closest('li');
                if (parentLi) parentLi.classList.remove('active');
            });
            
            // Aggiungi classe active al link corrispondente
            const activeLink = ScrollState.navLinks.find(link => {
                return link.getAttribute('href') === `#${activeSectionId}`;
            });
            
            if (activeLink) {
                activeLink.classList.add('active');
                const parentLi = activeLink.closest('li');
                if (parentLi) parentLi.classList.add('active');
            }
            
            window.PortfolioConfig.utils.log('debug', `Active section: ${activeSectionId}`);
        },

        /* ================================ */
        /* SCROLL TO ELEMENT                */
        /* ================================ */
        scrollToElement(element, offset = null) {
            if (!element) return;
            
            ScrollState.isUserScrolling = false;
            
            const elementTop = element.getBoundingClientRect().top + window.pageYOffset;
            const offsetValue = offset !== null ? offset : window.PortfolioConfig.ui.navigation.offset;
            const targetPosition = elementTop - offsetValue;
            
            this.smoothScrollTo(targetPosition);
        },

        /* ================================ */
        /* SMOOTH SCROLL TO POSITION        */
        /* ================================ */
        smoothScrollTo(targetPosition) {
            const startPosition = window.pageYOffset;
            const distance = targetPosition - startPosition;
            const duration = window.PortfolioConfig.ui.scroll.smoothDuration;
            let startTime = null;
            
            const animation = (currentTime) => {
                if (startTime === null) startTime = currentTime;
                const timeElapsed = currentTime - startTime;
                const progress = Math.min(timeElapsed / duration, 1);
                
                // Easing function (ease-in-out-cubic)
                const easeInOutCubic = progress < 0.5
                    ? 4 * progress * progress * progress
                    : 1 - Math.pow(-2 * progress + 2, 3) / 2;
                
                const currentPosition = startPosition + (distance * easeInOutCubic);
                window.scrollTo(0, currentPosition);
                
                if (progress < 1) {
                    ScrollState.scrollAnimationFrame = requestAnimationFrame(animation);
                } else {
                    // Scroll completato
                    ScrollState.isUserScrolling = true;
                    document.dispatchEvent(new CustomEvent('smoothScrollComplete', {
                        detail: { targetPosition, duration: timeElapsed }
                    }));
                }
            };
            
            // Cancella animazione precedente se esistente
            if (ScrollState.scrollAnimationFrame) {
                cancelAnimationFrame(ScrollState.scrollAnimationFrame);
            }
            
            ScrollState.scrollAnimationFrame = requestAnimationFrame(animation);
        },

        /* ================================ */
        /* SCROLL UTILITIES                 */
        /* ================================ */
        scrollToTop() {
            this.smoothScrollTo(0);
        },

        scrollToBottom() {
            const documentHeight = document.documentElement.scrollHeight;
            const windowHeight = window.innerHeight;
            this.smoothScrollTo(documentHeight - windowHeight);
        },

        scrollByViewport(factor) {
            const currentPosition = window.pageYOffset;
            const viewportHeight = window.innerHeight;
            const targetPosition = currentPosition + (viewportHeight * factor);
            this.smoothScrollTo(Math.max(0, targetPosition));
        },

        scrollToPreviousSection() {
            const currentIndex = ScrollState.sections.findIndex(section => section.id === ScrollState.currentSection);
            if (currentIndex > 0) {
                this.scrollToElement(ScrollState.sections[currentIndex - 1]);
            }
        },

        scrollToNextSection() {
            const currentIndex = ScrollState.sections.findIndex(section => section.id === ScrollState.currentSection);
            if (currentIndex < ScrollState.sections.length - 1) {
                this.scrollToElement(ScrollState.sections[currentIndex + 1]);
            }
        },

        /* ================================ */
        /* SCROLL ANIMATIONS                */
        /* ================================ */
        triggerScrollAnimation(element, animationType) {
            element.classList.add('scroll-animated');
            
            switch (animationType) {
                case 'fadeIn':
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                    break;
                case 'fadeInUp':
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                    break;
                case 'fadeInDown':
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                    break;
                case 'fadeInLeft':
                    element.style.opacity = '1';
                    element.style.transform = 'translateX(0)';
                    break;
                case 'fadeInRight':
                    element.style.opacity = '1';
                    element.style.transform = 'translateX(0)';
                    break;
                case 'scaleIn':
                    element.style.opacity = '1';
                    element.style.transform = 'scale(1)';
                    break;
                case 'rotateIn':
                    element.style.opacity = '1';
                    element.style.transform = 'rotate(0deg) scale(1)';
                    break;
                default:
                    element.classList.add('animate');
                    break;
            }
            
            // Dispatch evento
            element.dispatchEvent(new CustomEvent('scrollAnimationTriggered', {
                detail: { animationType }
            }));
        },

        resetScrollAnimation(element, animationType) {
            element.classList.remove('scroll-animated');
            
            switch (animationType) {
                case 'fadeIn':
                case 'fadeInUp':
                    element.style.opacity = '0';
                    element.style.transform = 'translateY(30px)';
                    break;
                case 'fadeInDown':
                    element.style.opacity = '0';
                    element.style.transform = 'translateY(-30px)';
                    break;
                case 'fadeInLeft':
                    element.style.opacity = '0';
                    element.style.transform = 'translateX(-30px)';
                    break;
                case 'fadeInRight':
                    element.style.opacity = '0';
                    element.style.transform = 'translateX(30px)';
                    break;
                case 'scaleIn':
                    element.style.opacity = '0';
                    element.style.transform = 'scale(0.8)';
                    break;
                case 'rotateIn':
                    element.style.opacity = '0';
                    element.style.transform = 'rotate(-180deg) scale(0.8)';
                    break;
                default:
                    element.classList.remove('animate');
                    break;
            }
        },

        /* ================================ */
        /* API PUBBLICA                     */
        /* ================================ */
        
        // Scroll to specific section by ID
        scrollTo(sectionId, offset = null) {
            const element = document.getElementById(sectionId);
            if (element) {
                this.scrollToElement(element, offset);
                return true;
            }
            return false;
        },

        // Get current section
        getCurrentSection() {
            return ScrollState.currentSection;
        },

        // Get scroll position
        getScrollPosition() {
            return ScrollState.scrollPosition;
        },

        // Get scroll direction
        getScrollDirection() {
            return ScrollState.scrollDirection;
        },

        // Check if scrolling
        isScrolling() {
            return ScrollState.isScrolling;
        },

        // Enable/disable smooth scroll
        setSmoothScroll(enabled) {
            if (enabled) {
                document.documentElement.style.scrollBehavior = 'smooth';
            } else {
                document.documentElement.style.scrollBehavior = 'auto';
            }
        },

        // Add scroll animation to element
        addScrollAnimation(element, animationType = 'fadeIn', options = {}) {
            if (typeof element === 'string') {
                element = document.querySelector(element);
            }
            
            if (!element) return false;
            
            element.dataset.scrollAnimation = animationType;
            if (options.repeat) {
                element.dataset.scrollRepeat = 'true';
            }
            
            // Setup initial state
            this.resetScrollAnimation(element, animationType);
            
            // Create observer for this element
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.triggerScrollAnimation(entry.target, animationType);
                    } else if (options.repeat) {
                        this.resetScrollAnimation(entry.target, animationType);
                    }
                });
            }, {
                threshold: options.threshold || 0.1,
                rootMargin: options.rootMargin || '50px'
            });
            
            observer.observe(element);
            ScrollState.observers.push(observer);
            
            return true;
        },

        // Get state
        getState() {
            return {
                currentSection: ScrollState.currentSection,
                scrollPosition: ScrollState.scrollPosition,
                scrollDirection: ScrollState.scrollDirection,
                isScrolling: ScrollState.isScrolling,
                sectionsCount: ScrollState.sections.length,
                navLinksCount: ScrollState.navLinks.length
            };
        },

        /* ================================ */
        /* GESTIONE ERRORI                  */
        /* ================================ */
        handleError(error) {
            window.PortfolioConfig.utils.log('error', 'Scroll module error', error);
            
            // Fallback: abilita scroll nativo del browser
            document.documentElement.style.scrollBehavior = 'smooth';
        },

        /* ================================ */
        /* CLEANUP                          */
        /* ================================ */
        cleanup() {
            // Cancella animation frames
            if (ScrollState.scrollAnimationFrame) {
                cancelAnimationFrame(ScrollState.scrollAnimationFrame);
            }
            
            // Cancella timeout
            if (ScrollState.scrollTimeout) {
                clearTimeout(ScrollState.scrollTimeout);
            }
            
            // Disconnetti observers
            ScrollState.observers.forEach(observer => {
                observer.disconnect();
            });
            ScrollState.observers = [];
            
            // Remove event listeners
            window.removeEventListener('scroll', this.handleScroll);
            window.removeEventListener('resize', this.handleResize);
            document.removeEventListener('keydown', this.handleKeyboard);
            window.removeEventListener('hashchange', this.handleHashChange);
            document.removeEventListener('visibilitychange', this.handleVisibilityChange);
            document.removeEventListener('portfolioResize', this.handlePortfolioResize);
            
            // Reset states
            ScrollState.isInitialized = false;
            ScrollState.currentSection = '';
            ScrollState.scrollPosition = 0;
            
            window.PortfolioConfig.utils.log('info', 'Scroll module cleaned up');
        }
    };

    /* ================================ */
    /* ESPORTAZIONE GLOBALE             */
    /* ================================ */
    window.ScrollModule = ScrollModule;

    window.PortfolioConfig.utils.log('debug', 'Scroll module script loaded');

})();