/*
===========================================
ANIMATIONS MODULE
===========================================
Gestisce tutte le animazioni dinamiche del portfolio
*/

(function() {
    'use strict';

    // Stato del modulo animazioni
    let animationsEnabled = true;
    let observers = [];
    let animatedElements = new Set();
    let particles = [];
    let animationFrameId = null;

    /* ================================ */
    /* INIZIALIZZAZIONE                 */
    /* ================================ */
    function init() {
        // Controlla preferenze utente per reduced motion
        checkMotionPreferences();

        if (animationsEnabled) {
            // Setup intersection observers per scroll animations
            setupScrollAnimations();

            // Setup animazioni speciali
            setupParticleSystem();
            setupCounterAnimations();
            setupTypewriterEffects();
            setupHoverAnimations();
            setupLoadingAnimations();

            // Setup animazioni periodiche
            startPeriodicAnimations();
        }

        window.PortfolioConfig.utils.log('debug', 'Animations module initialized');
    }

    /* ================================ */
    /* MOTION PREFERENCES               */
    /* ================================ */
    function checkMotionPreferences() {
        // Controlla se l'utente preferisce reduced motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        if (prefersReducedMotion) {
            animationsEnabled = false;
            document.body.classList.add('reduced-motion');
            window.PortfolioConfig.utils.log('info', 'Reduced motion enabled');
        }

        // Ascolta cambiamenti nelle preferenze
        window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (e) => {
            animationsEnabled = !e.matches;
            if (e.matches) {
                document.body.classList.add('reduced-motion');
                stopAllAnimations();
            } else {
                document.body.classList.remove('reduced-motion');
                init();
            }
        });
    }

    /* ================================ */
    /* SCROLL ANIMATIONS                */
    /* ================================ */
    function setupScrollAnimations() {
        // Elementi che devono animarsi quando entrano in viewport
        const animationTargets = [
            { selector: '.hero-greeting', animation: 'fadeInUp', delay: 200 },
            { selector: '.hero-name', animation: 'fadeInUp', delay: 400 },
            { selector: '.hero-profession', animation: 'fadeInUp', delay: 600 },
            { selector: '.hero-description', animation: 'fadeInUp', delay: 800 },
            { selector: '.hero-buttons', animation: 'fadeInUp', delay: 1000 },
            { selector: '.hero-avatar', animation: 'scaleIn', delay: 1200 },
            { selector: '.about-paragraph', animation: 'fadeInLeft', delay: 0 },
            { selector: '.stat', animation: 'bounceIn', delay: 0 },
            { selector: '.skill-card', animation: 'slideInUp', delay: 0 },
            { selector: '.project-card', animation: 'fadeInUp', delay: 0 },
            { selector: '.timeline-item', animation: 'slideInLeft', delay: 0 },
            { selector: '.contact-item', animation: 'fadeInUp', delay: 0 }
        ];

        animationTargets.forEach(target => {
            const elements = document.querySelectorAll(target.selector);
            elements.forEach((element, index) => {
                setupIntersectionObserver(element, target.animation, target.delay + (index * 100));
            });
        });
    }

    function setupIntersectionObserver(element, animationType, delay) {
        if (!element || animatedElements.has(element)) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !animatedElements.has(entry.target)) {
                    setTimeout(() => {
                        animateElement(entry.target, animationType);
                        animatedElements.add(entry.target);
                    }, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        observer.observe(element);
        observers.push(observer);
    }

    function animateElement(element, animationType) {
        element.classList.add('animate-' + animationType);
        
        // Rimuovi la classe dopo l'animazione per permettere re-triggering
        element.addEventListener('animationend', () => {
            element.classList.remove('animate-' + animationType);
        }, { once: true });
    }

    /* ================================ */
    /* COUNTER ANIMATIONS               */
    /* ================================ */
    function setupCounterAnimations() {
        const counters = document.querySelectorAll('[data-count]');
        
        counters.forEach(counter => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !animatedElements.has(entry.target)) {
                        animateCounter(entry.target);
                        animatedElements.add(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(counter);
            observers.push(observer);
        });
    }

    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000; // 2 secondi
        const startTime = performance.now();
        const startValue = 0;

        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out cubic)
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(startValue + (target - startValue) * easeOut);
            
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target.toLocaleString();
            }
        }
        
        requestAnimationFrame(updateCounter);
    }

    /* ================================ */
    /* TYPEWRITER EFFECTS               */
    /* ================================ */
    function setupTypewriterEffects() {
        const typewriterElements = document.querySelectorAll('[data-typewriter]');
        
        typewriterElements.forEach(element => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !animatedElements.has(entry.target)) {
                        typewriterEffect(entry.target);
                        animatedElements.add(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(element);
            observers.push(observer);
        });
    }

    function typewriterEffect(element) {
        const text = element.textContent;
        const speed = parseInt(element.getAttribute('data-speed')) || 50;
        
        element.textContent = '';
        element.style.borderRight = '2px solid currentColor';
        
        let i = 0;
        function typeChar() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeChar, speed);
            } else {
                // Animazione cursore lampeggiante
                setInterval(() => {
                    element.style.borderRight = element.style.borderRight === 'none' ? 
                        '2px solid currentColor' : 'none';
                }, 500);
            }
        }
        
        typeChar();
    }

    /* ================================ */
    /* PARTICLE SYSTEM                  */
    /* ================================ */
    function setupParticleSystem() {
        const particleContainers = document.querySelectorAll('.particles, .hero-shapes');
        
        particleContainers.forEach(container => {
            createParticles(container);
        });

        if (particles.length > 0) {
            startParticleAnimation();
        }
    }

    function createParticles(container) {
        const particleCount = 20;
        const rect = container.getBoundingClientRect();
        
        for (let i = 0; i < particleCount; i++) {
            const particle = {
                element: createParticleElement(),
                x: Math.random() * rect.width,
                y: Math.random() * rect.height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                size: Math.random() * 4 + 2,
                opacity: Math.random() * 0.5 + 0.1,
                container: container
            };
            
            particle.element.style.left = particle.x + 'px';
            particle.element.style.top = particle.y + 'px';
            particle.element.style.width = particle.size + 'px';
            particle.element.style.height = particle.size + 'px';
            particle.element.style.opacity = particle.opacity;
            
            container.appendChild(particle.element);
            particles.push(particle);
        }
    }

    function createParticleElement() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            background: currentColor;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
        `;
        return particle;
    }

    function startParticleAnimation() {
        function animateParticles() {
            particles.forEach(particle => {
                const rect = particle.container.getBoundingClientRect();
                
                particle.x += particle.vx;
                particle.y += particle.vy;
                
                // Rimbalzo sui bordi
                if (particle.x <= 0 || particle.x >= rect.width) {
                    particle.vx *= -1;
                }
                if (particle.y <= 0 || particle.y >= rect.height) {
                    particle.vy *= -1;
                }
                
                // Mantieni all'interno del container
                particle.x = Math.max(0, Math.min(rect.width, particle.x));
                particle.y = Math.max(0, Math.min(rect.height, particle.y));
                
                particle.element.style.left = particle.x + 'px';
                particle.element.style.top = particle.y + 'px';
            });
            
            animationFrameId = requestAnimationFrame(animateParticles);
        }
        
        animateParticles();
    }

    /* ================================ */
    /* HOVER ANIMATIONS                 */
    /* ================================ */
    function setupHoverAnimations() {
        // Animazioni tilt per cards
        const tiltElements = document.querySelectorAll('.skill-card, .project-card, .contact-item');
        
        tiltElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                startTiltAnimation(e.target);
            });
            
            element.addEventListener('mouseleave', (e) => {
                resetTilt(e.target);
            });
            
            element.addEventListener('mousemove', (e) => {
                updateTilt(e);
            });
        });

        // Animazioni magnetiche per bottoni
        const magneticElements = document.querySelectorAll('.btn, .hero-btn');
        
        magneticElements.forEach(element => {
            element.addEventListener('mouseenter', startMagneticEffect);
            element.addEventListener('mouseleave', resetMagneticEffect);
            element.addEventListener('mousemove', updateMagneticEffect);
        });
    }

    function startTiltAnimation(element) {
        element.style.transition = 'transform 0.1s ease-out';
    }

    function resetTilt(element) {
        element.style.transition = 'transform 0.3s ease-out';
        element.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)';
    }

    function updateTilt(e) {
        const element = e.currentTarget;
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const rotateX = (e.clientY - centerY) / rect.height * -10;
        const rotateY = (e.clientX - centerX) / rect.width * 10;
        
        element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
    }

    function startMagneticEffect(e) {
        e.currentTarget.style.transition = 'transform 0.3s ease-out';
    }

    function resetMagneticEffect(e) {
        e.currentTarget.style.transform = 'translate(0, 0) scale(1)';
    }

    function updateMagneticEffect(e) {
        const element = e.currentTarget;
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const deltaX = (e.clientX - centerX) * 0.1;
        const deltaY = (e.clientY - centerY) * 0.1;
        
        element.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(1.05)`;
    }

    /* ================================ */
    /* LOADING ANIMATIONS               */
    /* ================================ */
    function setupLoadingAnimations() {
        // Animazione progress bar del loading
        const progressBar = document.querySelector('.loading-progress-bar');
        const percentage = document.querySelector('.loading-percentage');
        
        if (progressBar && percentage) {
            animateLoadingProgress(progressBar, percentage);
        }

        // Sequenza di animazioni loading
        const loadingElements = [
            { selector: '.loading-logo', delay: 0 },
            { selector: '.loading-spinner', delay: 500 },
            { selector: '.loading-text', delay: 1000 },
            { selector: '.loading-progress', delay: 1500 }
        ];

        loadingElements.forEach(item => {
            const element = document.querySelector(item.selector);
            if (element) {
                setTimeout(() => {
                    element.classList.add('animate-fadeInUp');
                }, item.delay);
            }
        });
    }

    function animateLoadingProgress(progressBar, percentage) {
        let progress = 0;
        const duration = 3000;
        const startTime = performance.now();
        
        function updateProgress(currentTime) {
            const elapsed = currentTime - startTime;
            const progressPercent = Math.min(elapsed / duration, 1);
            
            // Easing function con alcuni "salti" realistici
            let eased = progressPercent;
            if (progressPercent < 0.3) {
                eased = progressPercent * 2;
            } else if (progressPercent < 0.7) {
                eased = 0.6 + (progressPercent - 0.3) * 0.5;
            } else {
                eased = 0.8 + (progressPercent - 0.7) * 0.67;
            }
            
            progress = Math.floor(eased * 100);
            
            progressBar.style.width = progress + '%';
            percentage.textContent = progress + '%';
            
            if (progressPercent < 1) {
                requestAnimationFrame(updateProgress);
            }
        }
        
        requestAnimationFrame(updateProgress);
    }

    /* ================================ */
    /* PERIODIC ANIMATIONS              */
    /* ================================ */
    function startPeriodicAnimations() {
        // Floating animation per elementi hero
        const floatingElements = document.querySelectorAll('.hero-avatar, .hero-shapes .hero-shape');
        
        floatingElements.forEach((element, index) => {
            element.style.animation = `float ${3 + index * 0.5}s ease-in-out infinite`;
            element.style.animationDelay = `${index * 0.2}s`;
        });

        // Pulse animation per elementi attivi
        const pulseElements = document.querySelectorAll('.status-indicator, .notification-dot');
        
        pulseElements.forEach(element => {
            element.style.animation = 'pulse 2s ease-in-out infinite';
        });

        // Gradient shift per testi gradient
        const gradientTexts = document.querySelectorAll('.hero-name, .gradient-text');
        
        gradientTexts.forEach(element => {
            element.style.animation = 'gradientShift 4s ease-in-out infinite';
        });
    }

    /* ================================ */
    /* SCROLL PROGRESS                  */
    /* ================================ */
    function setupScrollProgress() {
        const progressBar = document.getElementById('scroll-progress');
        
        if (progressBar) {
            window.addEventListener('scroll', window.PortfolioConfig.utils.throttle(() => {
                const scrolled = window.pageYOffset;
                const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
                const progress = (scrolled / maxScroll) * 100;
                
                progressBar.style.width = progress + '%';
            }, 10));
        }
    }

    /* ================================ */
    /* SMOOTH SCROLLING                 */
    /* ================================ */
    function setupSmoothScrolling() {
        // Intercetta tutti i link di navigazione
        const navLinks = document.querySelectorAll('a[href^="#"]');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    smoothScrollTo(targetElement);
                }
            });
        });
    }

    function smoothScrollTo(target) {
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        const duration = 1000;
        let startTime = null;
        
        function animate(currentTime) {
            if (startTime === null) startTime = currentTime;
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-in-out)
            const easeInOutCubic = progress < 0.5 
                ? 4 * progress * progress * progress 
                : 1 - Math.pow(-2 * progress + 2, 3) / 2;
            
            window.scrollTo(0, startPosition + distance * easeInOutCubic);
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }
        
        requestAnimationFrame(animate);
    }

    /* ================================ */
    /* UTILITY FUNCTIONS                */
    /* ================================ */
    function stopAllAnimations() {
        // Ferma tutte le animazioni in corso
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
        }

        // Disconnetti tutti gli observers
        observers.forEach(observer => {
            observer.disconnect();
        });
        observers = [];

        // Rimuovi tutte le particelle
        particles.forEach(particle => {
            if (particle.element && particle.element.parentNode) {
                particle.element.parentNode.removeChild(particle.element);
            }
        });
        particles = [];

        // Reset set di elementi animati
        animatedElements.clear();
    }

    function pauseAnimations() {
        document.body.style.animationPlayState = 'paused';
    }

    function resumeAnimations() {
        document.body.style.animationPlayState = 'running';
    }

    /* ================================ */
    /* API PUBBLICA                     */
    /* ================================ */
    window.AnimationsModule = {
        init,
        stopAllAnimations,
        pauseAnimations,
        resumeAnimations,
        animateElement,
        animateCounter,
        typewriterEffect,
        smoothScrollTo,
        isEnabled: () => animationsEnabled,
        setEnabled: (enabled) => {
            animationsEnabled = enabled;
            if (!enabled) {
                stopAllAnimations();
                document.body.classList.add('reduced-motion');
            } else {
                document.body.classList.remove('reduced-motion');
                init();
            }
        }
    };

    /* ================================ */
    /* AUTO-INIZIALIZZAZIONE            */
    /* ================================ */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();