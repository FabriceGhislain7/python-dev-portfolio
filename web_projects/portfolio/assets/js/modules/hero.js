/*
===========================================
HERO MODULE - Portfolio
===========================================
Modulo per la gestione della sezione hero con
animazioni, effetti parallax e typing effects
*/

class HeroModule {
    constructor() {
        this.heroSection = null;
        this.typewriterConfig = {
            speed: 80,
            deleteSpeed: 50,
            pauseTime: 2000,
            loop: true
        };
        this.parallaxEnabled = true;
        this.isVisible = false;
        this.animationFrameId = null;
        this.mousePosition = { x: 0, y: 0 };
        
        this.init();
    }

    /**
     * Inizializza il modulo hero
     */
    init() {
        this.heroSection = document.querySelector('#home.hero');
        if (!this.heroSection) {
            console.warn('⚠️ Hero Module: Hero section not found');
            return;
        }

        this.setupElements();
        this.bindEvents();
        this.setupTypewriter();
        this.setupParallax();
        this.setupScrollIndicator();
        this.enhanceAccessibility();
        
        console.log('🦸 Hero Module: Initialized');
    }

    /**
     * Configura gli elementi della sezione hero
     */
    setupElements() {
        // Trova elementi principali
        this.elements = {
            greeting: this.heroSection.querySelector('.hero-greeting'),
            name: this.heroSection.querySelector('.hero-name'),
            profession: this.heroSection.querySelector('.hero-profession'),
            description: this.heroSection.querySelector('.hero-description'),
            buttons: this.heroSection.querySelectorAll('.hero-btn'),
            avatar: this.heroSection.querySelector('.hero-avatar'),
            socialLinks: this.heroSection.querySelectorAll('.hero-social-link'),
            scrollIndicator: this.heroSection.querySelector('.hero-scroll'),
            shapes: this.heroSection.querySelectorAll('.hero-shape')
        };

        // Verifica che gli elementi essenziali esistano
        this.validateElements();
    }

    /**
     * Verifica che gli elementi principali esistano
     */
    validateElements() {
        const required = ['name', 'profession'];
        const missing = required.filter(key => !this.elements[key]);
        
        if (missing.length > 0) {
            console.warn(`⚠️ Hero Module: Missing elements: ${missing.join(', ')}`);
        }
    }

    /**
     * Imposta gli event listeners
     */
    bindEvents() {
        // Intersection Observer per attivare animazioni
        this.setupIntersectionObserver();
        
        // Mouse movement per effetti parallax
        if (this.parallaxEnabled) {
            this.heroSection.addEventListener('mousemove', (e) => {
                this.handleMouseMove(e);
            });
            
            this.heroSection.addEventListener('mouseleave', () => {
                this.resetParallax();
            });
        }

        // Click sui bottoni hero
        this.elements.buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleButtonClick(e);
            });
        });

        // Scroll indicator click
        if (this.elements.scrollIndicator) {
            this.elements.scrollIndicator.addEventListener('click', (e) => {
                this.handleScrollClick(e);
            });
        }

        // Social links tracking
        this.elements.socialLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                this.trackSocialClick(e);
            });
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardNavigation(e);
        });

        // Window resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        // Visibility change per pausare/riprendere animazioni
        document.addEventListener('visibilitychange', () => {
            this.handleVisibilityChange();
        });
    }

    /**
     * Configura l'Intersection Observer
     */
    setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !this.isVisible) {
                    this.isVisible = true;
                    this.startHeroAnimations();
                } else if (!entry.isIntersecting && this.isVisible) {
                    this.isVisible = false;
                    this.pauseAnimations();
                }
            });
        }, options);

        this.observer.observe(this.heroSection);
    }

    /**
     * Avvia le animazioni della sezione hero
     */
    startHeroAnimations() {
        // Le animazioni CSS si attivano automaticamente, qui gestiamo quelle JS
        this.animateAvatar();
        this.startParallax();
        
        // Avvia typewriter dopo un delay
        setTimeout(() => {
            this.startTypewriter();
        }, 1500);

        console.log('🎬 Hero animations started');
    }

    /**
     * Configura l'effetto typewriter per la professione
     */
    setupTypewriter() {
        if (!this.elements.profession) return;

        // Salva il testo originale
        this.originalProfessionText = this.elements.profession.textContent;
        
        // Array di professioni da alternare
        this.professionTexts = [
            'Python Developer',
            'AI/ML Enthusiast', 
            'Full Stack Developer',
            'Data Scientist',
            'IoT Developer'
        ];
        
        this.currentTextIndex = 0;
        this.typewriterActive = false;
    }

    /**
     * Avvia l'effetto typewriter
     */
    startTypewriter() {
        if (!this.elements.profession || this.typewriterActive) return;
        
        this.typewriterActive = true;
        this.typeCurrentText();
    }

    /**
     * Scrive il testo corrente con effetto typewriter
     */
    async typeCurrentText() {
        if (!this.typewriterActive) return;

        const text = this.professionTexts[this.currentTextIndex];
        const element = this.elements.profession;
        
        // Cancella il testo esistente
        await this.deleteText(element);
        
        // Scrivi il nuovo testo
        await this.typeText(element, text);
        
        // Attendi prima del prossimo ciclo
        setTimeout(() => {
            if (this.typewriterActive) {
                this.currentTextIndex = (this.currentTextIndex + 1) % this.professionTexts.length;
                this.typeCurrentText();
            }
        }, this.typewriterConfig.pauseTime);
    }

    /**
     * Scrive il testo carattere per carattere
     */
    typeText(element, text) {
        return new Promise(resolve => {
            let i = 0;
            const timer = setInterval(() => {
                if (!this.typewriterActive) {
                    clearInterval(timer);
                    resolve();
                    return;
                }

                element.textContent = text.slice(0, i + 1);
                i++;
                
                if (i >= text.length) {
                    clearInterval(timer);
                    resolve();
                }
            }, this.typewriterConfig.speed);
        });
    }

    /**
     * Cancella il testo carattere per carattere
     */
    deleteText(element) {
        return new Promise(resolve => {
            const currentText = element.textContent;
            let i = currentText.length;
            
            const timer = setInterval(() => {
                if (!this.typewriterActive) {
                    clearInterval(timer);
                    resolve();
                    return;
                }

                element.textContent = currentText.slice(0, i);
                i--;
                
                if (i < 0) {
                    clearInterval(timer);
                    resolve();
                }
            }, this.typewriterConfig.deleteSpeed);
        });
    }

    /**
     * Anima l'avatar con effetti aggiuntivi
     */
    animateAvatar() {
        if (!this.elements.avatar) return;

        const img = this.elements.avatar.querySelector('img');
        if (!img) return;

        // Aggiungi classe per animazioni CSS personalizzate
        this.elements.avatar.classList.add('hero-avatar-animated');
        
        // Effetto pulse periodico
        setInterval(() => {
            if (this.isVisible && !document.hidden) {
                img.style.transform = 'scale(1.02)';
                setTimeout(() => {
                    img.style.transform = 'scale(1)';
                }, 200);
            }
        }, 4000);
    }

    /**
     * Configura gli effetti parallax
     */
    setupParallax() {
        if (!this.parallaxEnabled || window.innerWidth <= 768) return;

        this.parallaxElements = Array.from(this.elements.shapes).map((shape, index) => ({
            element: shape,
            speed: 0.5 + (index * 0.3), // Velocità differenti per ogni shape
            originalTransform: this.getTransformValues(shape)
        }));
    }

    /**
     * Avvia gli effetti parallax
     */
    startParallax() {
        if (!this.parallaxEnabled || !this.parallaxElements) return;

        this.animationFrameId = requestAnimationFrame(() => this.updateParallax());
    }

    /**
     * Aggiorna gli effetti parallax
     */
    updateParallax() {
        if (!this.isVisible || !this.parallaxElements) return;

        const centerX = this.heroSection.offsetWidth / 2;
        const centerY = this.heroSection.offsetHeight / 2;
        const moveX = (this.mousePosition.x - centerX) * 0.01;
        const moveY = (this.mousePosition.y - centerY) * 0.01;

        this.parallaxElements.forEach(({ element, speed, originalTransform }) => {
            const x = originalTransform.x + (moveX * speed);
            const y = originalTransform.y + (moveY * speed);
            
            element.style.transform = `translate(${x}px, ${y}px) ${originalTransform.others}`;
        });

        if (this.parallaxEnabled) {
            this.animationFrameId = requestAnimationFrame(() => this.updateParallax());
        }
    }

    /**
     * Gestisce il movimento del mouse per parallax
     */
    handleMouseMove(e) {
        const rect = this.heroSection.getBoundingClientRect();
        this.mousePosition.x = e.clientX - rect.left;
        this.mousePosition.y = e.clientY - rect.top;
    }

    /**
     * Reset degli effetti parallax
     */
    resetParallax() {
        if (!this.parallaxElements) return;

        this.parallaxElements.forEach(({ element, originalTransform }) => {
            element.style.transform = `translate(${originalTransform.x}px, ${originalTransform.y}px) ${originalTransform.others}`;
        });
    }

    /**
     * Ottiene i valori di transform di un elemento
     */
    getTransformValues(element) {
        const computedStyle = window.getComputedStyle(element);
        const matrix = computedStyle.transform;
        
        if (matrix === 'none') {
            return { x: 0, y: 0, others: '' };
        }

        const values = matrix.match(/matrix\(([^)]+)\)/);
        if (values) {
            const matrixValues = values[1].split(',').map(parseFloat);
            return {
                x: matrixValues[4] || 0,
                y: matrixValues[5] || 0,
                others: ''
            };
        }

        return { x: 0, y: 0, others: '' };
    }

    /**
     * Configura l'indicatore di scroll
     */
    setupScrollIndicator() {
        if (!this.elements.scrollIndicator) return;

        // Aggiorna l'indicatore basandosi sullo scroll
        window.addEventListener('scroll', () => {
            this.updateScrollIndicator();
        });
    }

    /**
     * Aggiorna l'animazione dell'indicatore di scroll
     */
    updateScrollIndicator() {
        if (!this.elements.scrollIndicator) return;

        const scrollY = window.scrollY;
        const heroHeight = this.heroSection.offsetHeight;
        const scrollProgress = Math.min(scrollY / (heroHeight * 0.3), 1);
        
        // Fai sparire l'indicatore quando si inizia a scrollare
        this.elements.scrollIndicator.style.opacity = 1 - scrollProgress;
    }

    /**
     * Gestisce il click sui bottoni hero
     */
    handleButtonClick(e) {
        const button = e.currentTarget;
        const href = button.getAttribute('href');
        
        // Effetto visivo al click
        this.addClickEffect(button);
        
        // Smooth scroll per link interni
        if (href && href.startsWith('#')) {
            e.preventDefault();
            this.smoothScrollToSection(href);
        }
        
        // Tracking
        this.trackButtonClick(button);
    }

    /**
     * Aggiunge effetto visivo al click
     */
    addClickEffect(button) {
        button.style.transform = 'translateY(-2px) scale(0.98)';
        setTimeout(() => {
            button.style.transform = '';
        }, 150);
    }

    /**
     * Smooth scroll verso una sezione
     */
    smoothScrollToSection(sectionId) {
        const targetSection = document.querySelector(sectionId);
        if (!targetSection) return;

        const headerHeight = document.querySelector('header')?.offsetHeight || 0;
        const targetPosition = targetSection.offsetTop - headerHeight - 20;

        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }

    /**
     * Gestisce il click sull'indicatore di scroll
     */
    handleScrollClick(e) {
        e.preventDefault();
        const nextSection = document.querySelector('#about');
        if (nextSection) {
            this.smoothScrollToSection('#about');
        }
    }

    /**
     * Gestisce la navigazione da tastiera
     */
    handleKeyboardNavigation(e) {
        // Escape per fermare il typewriter
        if (e.key === 'Escape' && this.typewriterActive) {
            this.stopTypewriter();
        }
        
        // Spazio per fermare/avviare animazioni
        if (e.key === ' ' && e.ctrlKey) {
            e.preventDefault();
            this.toggleAnimations();
        }
    }

    /**
     * Gestisce il resize della finestra
     */
    handleResize() {
        // Disabilita parallax su mobile
        if (window.innerWidth <= 768 && this.parallaxEnabled) {
            this.parallaxEnabled = false;
            this.resetParallax();
            if (this.animationFrameId) {
                cancelAnimationFrame(this.animationFrameId);
            }
        } else if (window.innerWidth > 768 && !this.parallaxEnabled) {
            this.parallaxEnabled = true;
            this.setupParallax();
            if (this.isVisible) {
                this.startParallax();
            }
        }
        
        // Riposiziona elementi se necessario
        this.updateLayout();
    }

    /**
     * Gestisce il cambio di visibilità della pagina
     */
    handleVisibilityChange() {
        if (document.hidden) {
            this.pauseAnimations();
        } else if (this.isVisible) {
            this.resumeAnimations();
        }
    }

    /**
     * Mette in pausa le animazioni
     */
    pauseAnimations() {
        this.typewriterActive = false;
        
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }

    /**
     * Riprende le animazioni
     */
    resumeAnimations() {
        if (!this.typewriterActive && this.isVisible) {
            this.typewriterActive = true;
            this.typeCurrentText();
        }
        
        if (this.parallaxEnabled && this.isVisible) {
            this.startParallax();
        }
    }

    /**
     * Toggle delle animazioni
     */
    toggleAnimations() {
        if (this.typewriterActive) {
            this.pauseAnimations();
        } else {
            this.resumeAnimations();
        }
    }

    /**
     * Ferma l'effetto typewriter
     */
    stopTypewriter() {
        this.typewriterActive = false;
        if (this.elements.profession) {
            this.elements.profession.textContent = this.originalProfessionText;
        }
    }

    /**
     * Migliora l'accessibilità
     */
    enhanceAccessibility() {
        // Aggiungi ARIA labels
        if (this.elements.scrollIndicator) {
            this.elements.scrollIndicator.setAttribute('aria-label', 'Scorri alla sezione successiva');
        }

        // Gestisci prefers-reduced-motion
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            this.typewriterConfig.speed = 0;
            this.typewriterConfig.deleteSpeed = 0;
            this.parallaxEnabled = false;
        }

        // Focus management
        this.setupFocusManagement();
    }

    /**
     * Configura la gestione del focus
     */
    setupFocusManagement() {
        const focusableElements = this.heroSection.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );

        focusableElements.forEach(element => {
            element.addEventListener('focus', () => {
                element.classList.add('hero-focused');
            });
            
            element.addEventListener('blur', () => {
                element.classList.remove('hero-focused');
            });
        });
    }

    /**
     * Aggiorna il layout dopo resize
     */
    updateLayout() {
        // Ricalcola posizioni per parallax
        if (this.parallaxEnabled && this.parallaxElements) {
            this.parallaxElements.forEach(item => {
                item.originalTransform = this.getTransformValues(item.element);
            });
        }
    }

    /**
     * Tracking dei click sui bottoni
     */
    trackButtonClick(button) {
        const buttonText = button.textContent.trim();
        const href = button.getAttribute('href');
        
        console.log(`🔘 Hero button clicked: ${buttonText} -> ${href}`);
        
        // Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'hero_button_click', {
                'button_text': buttonText,
                'button_href': href
            });
        }
    }

    /**
     * Tracking dei click sui social
     */
    trackSocialClick(e) {
        const link = e.currentTarget;
        const platform = this.getSocialPlatform(link);
        
        console.log(`📱 Social link clicked: ${platform}`);
        
        // Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'social_click', {
                'platform': platform,
                'location': 'hero'
            });
        }
    }

    /**
     * Identifica la piattaforma social dal link
     */
    getSocialPlatform(link) {
        const href = link.getAttribute('href') || '';
        const icon = link.querySelector('i');
        
        if (href.includes('github.com') || (icon && icon.classList.contains('fa-github'))) {
            return 'github';
        } else if (href.includes('linkedin.com') || (icon && icon.classList.contains('fa-linkedin'))) {
            return 'linkedin';
        } else if (href.includes('mailto:') || (icon && icon.classList.contains('fa-envelope'))) {
            return 'email';
        } else if (href.includes('twitter.com') || (icon && icon.classList.contains('fa-twitter'))) {
            return 'twitter';
        }
        
        return 'unknown';
    }

    /**
     * Metodi pubblici per controllo esterno
     */
    startTypewriterEffect() {
        if (!this.typewriterActive) {
            this.startTypewriter();
        }
    }

    stopTypewriterEffect() {
        this.stopTypewriter();
    }

    setTypewriterTexts(texts) {
        this.professionTexts = texts;
        this.currentTextIndex = 0;
    }

    enableParallax() {
        this.parallaxEnabled = true;
        this.setupParallax();
        if (this.isVisible) {
            this.startParallax();
        }
    }

    disableParallax() {
        this.parallaxEnabled = false;
        this.resetParallax();
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
    }

    /**
     * Cleanup
     */
    destroy() {
        // Ferma tutte le animazioni
        this.pauseAnimations();
        
        // Disconnetti observer
        if (this.observer) {
            this.observer.disconnect();
        }
        
        // Cancella animation frame
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }
        
        console.log('🗑️ Hero Module: Destroyed');
    }
}

// Export per uso modulare
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HeroModule;
}

// Inizializzazione automatica quando il DOM è pronto
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.heroModule = new HeroModule();
        });
    } else {
        window.heroModule = new HeroModule();
    }
}