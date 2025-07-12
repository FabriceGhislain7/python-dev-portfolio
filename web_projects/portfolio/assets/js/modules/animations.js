// Animation Manager Module

const AnimationManager = {
    // Initialize animation system
    init() {
        this.observers = new Map();
        this.animatedElements = new Set();
        this.particleSystem = null;
        
        this.setupScrollAnimations();
        this.setupTextAnimations();
        this.setupParticleSystem();
        this.setupHoverEffects();
        this.setupLoadingAnimations();
        
        console.log('Animation Manager initialized');
    },
    
    // Setup scroll-triggered animations
    setupScrollAnimations() {
        const animatedElements = Utils.dom.getAll('.scroll-animate');
        
        if (animatedElements.length === 0) return;
        
        const observer = Utils.performance.createObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.triggerElementAnimation(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: CONFIG.animation.threshold,
            rootMargin: '0px 0px -50px 0px'
        });
        
        animatedElements.forEach(element => {
            observer.observe(element);
        });
        
        this.observers.set('scroll', observer);
    },
    
    // Trigger animation for specific element
    triggerElementAnimation(element) {
        if (this.animatedElements.has(element)) return;
        
        this.animatedElements.add(element);
        
        // Add base animation class
        Utils.dom.addClass(element, 'in-view');
        
        // Handle specific element types
        if (element.classList.contains('skill-card')) {
            this.animateSkillCard(element);
        } else if (element.classList.contains('project-card')) {
            this.animateProjectCard(element);
        } else if (element.classList.contains('stat')) {
            this.animateStatCounter(element);
        } else if (element.classList.contains('hero-text')) {
            this.animateHeroText(element);
        }
        
        // Trigger custom animation event
        Utils.events.trigger(element, 'animated', { element });
    },
    
    // Animate skill cards with progress bars
    animateSkillCard(skillCard) {
        const progressBar = skillCard.querySelector('.progress-fill');
        const technologies = skillCard.querySelectorAll('.skill-tag');
        
        // Animate progress bar
        if (progressBar) {
            const progress = progressBar.getAttribute('data-progress');
            setTimeout(() => {
                progressBar.style.width = `${progress}%`;
                progressBar.style.opacity = '1';
            }, 200);
        }
        
        // Stagger animate technology tags
        if (technologies.length > 0) {
            Utils.animation.stagger(technologies, 'fade-in-up', 50);
        }
    },
    
    // Animate project cards
    animateProjectCard(projectCard) {
        const image = projectCard.querySelector('.project-image img');
        const content = projectCard.querySelector('.project-content');
        const techTags = projectCard.querySelectorAll('.tech-tag');
        
        // Animate image with scale effect
        if (image) {
            setTimeout(() => {
                Utils.dom.addClass(image, 'animate-scale-in');
            }, 100);
        }
        
        // Animate content
        if (content) {
            setTimeout(() => {
                Utils.dom.addClass(content, 'animate-fade-in-up');
            }, 200);
        }
        
        // Stagger animate tech tags
        if (techTags.length > 0) {
            setTimeout(() => {
                Utils.animation.stagger(techTags, 'animate-fade-in', 30);
            }, 400);
        }
    },
    
    // Animate statistics counters
    animateStatCounter(statElement) {
        const numberElement = statElement.querySelector('.stat-number');
        if (!numberElement || numberElement.classList.contains('counted')) return;
        
        const targetValue = parseInt(numberElement.getAttribute('data-count')) || 0;
        const suffix = numberElement.textContent.replace(/[0-9]/g, '');
        
        Utils.dom.addClass(numberElement, 'counted');
        Utils.animation.countUp(numberElement, targetValue, CONFIG.skills.countUpDuration, suffix);
    },
    
    // Animate hero text with typewriter effect
    animateHeroText(heroText) {
        const titleElements = heroText.querySelectorAll('.hero-greeting, .hero-name, .hero-profession');
        const description = heroText.querySelector('.hero-description');
        const buttons = heroText.querySelector('.hero-buttons');
        
        // Animate title elements with stagger
        titleElements.forEach((element, index) => {
            setTimeout(() => {
                Utils.dom.addClass(element, 'animate-fade-in-up');
            }, index * 200);
        });
        
        // Animate description
        if (description) {
            setTimeout(() => {
                Utils.dom.addClass(description, 'animate-fade-in');
            }, titleElements.length * 200 + 200);
        }
        
        // Animate buttons
        if (buttons) {
            setTimeout(() => {
                Utils.dom.addClass(buttons, 'animate-fade-in-up');
            }, titleElements.length * 200 + 400);
        }
    },
    
    // Setup text animations (typewriter, text reveal, etc.)
    setupTextAnimations() {
        // Typewriter effect for hero title
        const typewriterElements = Utils.dom.getAll('.typewriter');
        typewriterElements.forEach(element => {
            this.createTypewriterEffect(element);
        });
        
        // Text reveal effect
        const textRevealElements = Utils.dom.getAll('.text-reveal');
        textRevealElements.forEach(element => {
            this.createTextRevealEffect(element);
        });
    },
    
    // Create typewriter effect
    createTypewriterEffect(element) {
        const text = element.textContent;
        const speed = element.getAttribute('data-speed') || 50;
        
        element.textContent = '';
        element.style.opacity = '1';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, speed);
            } else {
                // Remove cursor after typing
                setTimeout(() => {
                    element.style.borderRight = 'none';
                }, 1000);
            }
        };
        
        // Start typing with a delay
        setTimeout(typeWriter, 500);
    },
    
    // Create text reveal effect
    createTextRevealEffect(element) {
        const observer = Utils.performance.createObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    Utils.dom.addClass(entry.target, 'animate-text-reveal');
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(element);
    },
    
    // Setup particle system for hero background
    setupParticleSystem() {
        const heroParticles = Utils.dom.get('.hero-particles');
        if (!heroParticles) return;
        
        this.particleSystem = {
            container: heroParticles,
            particles: [],
            isActive: true
        };
        
        // Create initial particles
        this.createParticles(20);
        
        // Animate particles
        this.animateParticles();
        
        // Handle mouse movement for interactive particles
        this.setupInteractiveParticles();
    },
    
    // Create floating particles
    createParticles(count) {
        if (!this.particleSystem) return;
        
        for (let i = 0; i < count; i++) {
            const particle = Utils.dom.create('div', 'particle');
            
            // Random size and position
            const size = Utils.math.random(2, 6);
            const x = Utils.math.random(0, 100);
            const y = Utils.math.random(0, 100);
            
            particle.style.cssText = `
                width: ${size}px;
                height: ${size}px;
                left: ${x}%;
                top: ${y}%;
                animation-delay: ${Utils.math.random(0, 3)}s;
                animation-duration: ${Utils.math.random(3, 6)}s;
            `;
            
            this.particleSystem.container.appendChild(particle);
            this.particleSystem.particles.push({
                element: particle,
                x: x,
                y: y,
                vx: Utils.math.random(-0.5, 0.5),
                vy: Utils.math.random(-0.5, 0.5),
                size: size
            });
        }
    },
    
    // Animate particles with physics
    animateParticles() {
        if (!this.particleSystem || !this.particleSystem.isActive) return;
        
        this.particleSystem.particles.forEach(particle => {
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Wrap around screen
            if (particle.x > 100) particle.x = -5;
            if (particle.x < -5) particle.x = 100;
            if (particle.y > 100) particle.y = -5;
            if (particle.y < -5) particle.y = 100;
            
            // Apply position
            particle.element.style.left = `${particle.x}%`;
            particle.element.style.top = `${particle.y}%`;
        });
        
        requestAnimationFrame(() => this.animateParticles());
    },
    
    // Setup interactive particles that follow mouse
    setupInteractiveParticles() {
        if (!this.particleSystem) return;
        
        const hero = Utils.dom.get('.hero');
        if (!hero) return;
        
        let mouseX = 0;
        let mouseY = 0;
        
        hero.addEventListener('mousemove', (e) => {
            const rect = hero.getBoundingClientRect();
            mouseX = ((e.clientX - rect.left) / rect.width) * 100;
            mouseY = ((e.clientY - rect.top) / rect.height) * 100;
            
            // Attract particles to mouse
            this.particleSystem.particles.forEach(particle => {
                const dx = mouseX - particle.x;
                const dy = mouseY - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 20) {
                    particle.vx += dx * 0.0001;
                    particle.vy += dy * 0.0001;
                    
                    // Limit velocity
                    particle.vx = Utils.math.clamp(particle.vx, -1, 1);
                    particle.vy = Utils.math.clamp(particle.vy, -1, 1);
                }
            });
        });
    },
    
    // Setup hover effects for interactive elements
    setupHoverEffects() {
        // Magnetic buttons
        const magneticButtons = Utils.dom.getAll('.btn');
        magneticButtons.forEach(button => {
            this.addMagneticEffect(button);
        });
        
        // Tilt effect for cards
        const tiltCards = Utils.dom.getAll('.skill-card, .project-card');
        tiltCards.forEach(card => {
            this.addTiltEffect(card);
        });
        
        // Glow effect for icons
        const glowIcons = Utils.dom.getAll('.skill-icon, .contact-icon');
        glowIcons.forEach(icon => {
            this.addGlowEffect(icon);
        });
    },
    
    // Add magnetic effect to buttons
    addMagneticEffect(element) {
        let isHovering = false;
        
        element.addEventListener('mouseenter', () => {
            isHovering = true;
            Utils.dom.addClass(element, 'magnetic-active');
        });
        
        element.addEventListener('mouseleave', () => {
            isHovering = false;
            Utils.dom.removeClass(element, 'magnetic-active');
            element.style.transform = '';
        });
        
        element.addEventListener('mousemove', (e) => {
            if (!isHovering) return;
            
            const rect = element.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            const moveX = x * 0.1;
            const moveY = y * 0.1;
            
            element.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    },
    
    // Add 3D tilt effect to cards
    addTiltEffect(element) {
        element.addEventListener('mousemove', (e) => {
            const rect = element.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            element.style.transform = `
                perspective(1000px) 
                rotateX(${rotateX}deg) 
                rotateY(${rotateY}deg) 
                scale3d(1.02, 1.02, 1.02)
            `;
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.transform = '';
        });
    },
    
    // Add glow effect to icons
    addGlowEffect(element) {
        element.addEventListener('mouseenter', () => {
            Utils.dom.addClass(element, 'animate-glow');
        });
        
        element.addEventListener('mouseleave', () => {
            Utils.dom.removeClass(element, 'animate-glow');
        });
    },
    
    // Setup loading animations
    setupLoadingAnimations() {
        // Shimmer effect for loading states
        const shimmerElements = Utils.dom.getAll('.shimmer');
        shimmerElements.forEach(element => {
            this.addShimmerEffect(element);
        });
        
        // Skeleton loading for cards
        const skeletonElements = Utils.dom.getAll('.skeleton');
        skeletonElements.forEach(element => {
            this.addSkeletonEffect(element);
        });
    },
    
    // Add shimmer loading effect
    addShimmerEffect(element) {
        const shimmer = Utils.dom.create('div', 'shimmer-animation');
        element.appendChild(shimmer);
        
        // Remove shimmer when content loads
        const removeShimmer = () => {
            if (shimmer.parentNode) {
                shimmer.parentNode.removeChild(shimmer);
            }
        };
        
        // Auto remove after 3 seconds
        setTimeout(removeShimmer, 3000);
        
        // Or remove when 'loaded' class is added
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && 
                    mutation.attributeName === 'class' &&
                    element.classList.contains('loaded')) {
                    removeShimmer();
                    observer.disconnect();
                }
            });
        });
        
        observer.observe(element, { attributes: true });
    },
    
    // Add skeleton loading effect
    addSkeletonEffect(element) {
        Utils.dom.addClass(element, 'skeleton-loading');
        
        // Remove skeleton when loaded
        const removeEffect = () => {
            Utils.dom.removeClass(element, 'skeleton-loading');
            Utils.dom.addClass(element, 'skeleton-loaded');
        };
        
        // Listen for loaded event
        element.addEventListener('loaded', removeEffect);
        
        // Auto remove after 2 seconds
        setTimeout(removeEffect, 2000);
    },
    
    // Create custom animation sequences
    animateSequence(elements, animationClass, delay = 100) {
        return new Promise((resolve) => {
            let completed = 0;
            
            elements.forEach((element, index) => {
                setTimeout(() => {
                    Utils.dom.addClass(element, animationClass);
                    
                    // Listen for animation end
                    const handleAnimationEnd = () => {
                        completed++;
                        if (completed === elements.length) {
                            resolve();
                        }
                        element.removeEventListener('animationend', handleAnimationEnd);
                    };
                    
                    element.addEventListener('animationend', handleAnimationEnd);
                }, index * delay);
            });
        });
    },
    
    // Parallax scroll effect
    setupParallaxScroll() {
        const parallaxElements = Utils.dom.getAll('[data-parallax]');
        
        if (parallaxElements.length === 0) return;
        
        const handleScroll = Utils.events.throttle(() => {
            const scrollY = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = parseFloat(element.getAttribute('data-parallax')) || 0.5;
                const yPos = -(scrollY * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        }, 16);
        
        window.addEventListener('scroll', handleScroll);
    },
    
    // Cleanup animations
    cleanup() {
        // Stop particle system
        if (this.particleSystem) {
            this.particleSystem.isActive = false;
        }
        
        // Disconnect observers
        this.observers.forEach(observer => {
            observer.disconnect();
        });
        
        // Clear animated elements
        this.animatedElements.clear();
        
        console.log('Animation Manager cleaned up');
    },
    
    // Public method to trigger animation manually
    trigger(element, animationType = 'fadeInUp') {
        if (typeof element === 'string') {
            element = Utils.dom.get(element);
        }
        
        if (element) {
            Utils.dom.addClass(element, `animate-${animationType}`);
        }
    },
    
    // Public method to reset animations
    reset(element) {
        if (typeof element === 'string') {
            element = Utils.dom.get(element);
        }
        
        if (element) {
            // Remove all animation classes
            const animationClasses = Array.from(element.classList).filter(cls => 
                cls.startsWith('animate-') || cls === 'in-view'
            );
            
            animationClasses.forEach(cls => {
                Utils.dom.removeClass(element, cls);
            });
            
            // Remove from animated elements set
            this.animatedElements.delete(element);
        }
    }
};

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    AnimationManager.init();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    AnimationManager.cleanup();
});

// Export for other modules
window.AnimationManager = AnimationManager;