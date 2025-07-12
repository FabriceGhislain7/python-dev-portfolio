// Main Portfolio JavaScript

class Portfolio {
    constructor() {
        this.isLoaded = false;
        this.loadingScreen = Utils.dom.get('#loading-screen');
        this.backToTopBtn = Utils.dom.get('#back-to-top');
        this.observers = new Map();
        
        this.init();
    }
    
    async init() {
        console.log('🚀 Portfolio initialization started');
        
        try {
            // Show loading screen
            this.showLoadingScreen();
            
            // Initialize core components
            await this.initializeComponents();
            
            // Load data
            await this.loadData();
            
            // Setup interactions
            this.setupInteractions();
            
            // Setup scroll animations
            this.setupScrollAnimations();
            
            // Hide loading screen
            await this.hideLoadingScreen();
            
            this.isLoaded = true;
            console.log('✅ Portfolio loaded successfully');
            
        } catch (error) {
            console.error('❌ Portfolio initialization failed:', error);
            this.hideLoadingScreen();
        }
    }
    
    async initializeComponents() {
        // Components are already initialized via their modules
        // Just wait a bit to ensure everything is ready
        await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    async loadData() {
        try {
            // Load skills data
            const skillsData = await Utils.api.get(CONFIG.api.skills);
            this.renderSkills(skillsData.skills);
            
            // Load projects data
            const projectsData = await Utils.api.get(CONFIG.api.projects);
            this.renderProjects(projectsData.projects);
            
        } catch (error) {
            console.error('Error loading data:', error);
            // Fallback to static content if data loading fails
            this.showFallbackContent();
        }
    }
    
    renderSkills(skills) {
        const skillsGrid = Utils.dom.get('#skills-grid');
        if (!skillsGrid || !skills) return;
        
        skillsGrid.innerHTML = '';
        
        skills.forEach((skill, index) => {
            const skillCard = this.createSkillCard(skill);
            skillCard.classList.add('scroll-animate');
            skillCard.style.animationDelay = `${index * 0.1}s`;
            skillsGrid.appendChild(skillCard);
        });
    }
    
    createSkillCard(skill) {
        const card = Utils.dom.create('div', 'skill-card');
        
        card.innerHTML = `
            <div class="skill-header">
                <div class="skill-icon">
                    <i class="${skill.icon}"></i>
                </div>
                <div class="skill-info">
                    <h3>${skill.name}</h3>
                    <span class="skill-category">${skill.category}</span>
                </div>
            </div>
            <div class="skill-progress">
                <div class="progress-label">
                    <span>Competenza</span>
                    <span>${skill.level}%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" data-progress="${skill.level}"></div>
                </div>
            </div>
            <p>${skill.description}</p>
            <div class="skill-tags">
                ${skill.tags.map(tag => `<span class="skill-tag">${tag}</span>`).join('')}
            </div>
        `;
        
        return card;
    }
    
    renderProjects(projects) {
        const projectsGrid = Utils.dom.get('#projects-grid');
        if (!projectsGrid || !projects) return;
        
        projectsGrid.innerHTML = '';
        
        projects.forEach((project, index) => {
            const projectCard = this.createProjectCard(project);
            projectCard.classList.add('scroll-animate');
            projectCard.style.animationDelay = `${index * 0.1}s`;
            projectsGrid.appendChild(projectCard);
        });
        
        // Initialize project filters after rendering
        if (window.ProjectFilters) {
            window.ProjectFilters.init();
        }
    }
    
    createProjectCard(project) {
        const card = Utils.dom.create('div', `project-card ${project.category}`);
        card.setAttribute('data-category', project.category);
        
        const statusClass = project.status === 'completed' ? 'status-completed' : 'status-in-progress';
        const statusText = project.status === 'completed' ? 'Completato' : 'In Corso';
        
        card.innerHTML = `
            <div class="project-image">
                <img src="${project.image}" alt="${project.title}" loading="lazy">
                <div class="project-overlay">
                    ${project.links.live ? `<a href="${project.links.live}" class="project-link" target="_blank" rel="noopener">
                        <i class="fas fa-external-link-alt"></i>
                    </a>` : ''}
                    ${project.links.github ? `<a href="${project.links.github}" class="project-link" target="_blank" rel="noopener">
                        <i class="fab fa-github"></i>
                    </a>` : ''}
                </div>
            </div>
            <div class="project-content">
                <h3 class="project-title">${project.title}</h3>
                <p class="project-description">${project.description}</p>
                <div class="project-tech">
                    ${project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                </div>
                <div class="project-meta">
                    <span class="project-date">${this.formatDate(project.date)}</span>
                    <span class="project-status ${statusClass}">${statusText}</span>
                </div>
            </div>
        `;
        
        return card;
    }
    
    setupInteractions() {
        // Back to top button
        this.setupBackToTop();
        
        // Contact form
        this.setupContactForm();
        
        // Smooth scrolling for all anchor links
        this.setupSmoothScrolling();
        
        // Statistics counter animation
        this.setupStatsCounter();
        
        // Parallax effects
        this.setupParallax();
    }
    
    setupBackToTop() {
        if (!this.backToTopBtn) return;
        
        const toggleBackToTop = () => {
            if (window.scrollY > 300) {
                Utils.dom.addClass(this.backToTopBtn, 'visible');
            } else {
                Utils.dom.removeClass(this.backToTopBtn, 'visible');
            }
        };
        
        // Initial check
        toggleBackToTop();
        
        // Listen to scroll
        window.addEventListener('scroll', Utils.events.throttle(toggleBackToTop, 100));
        
        // Click handler
        this.backToTopBtn.addEventListener('click', () => {
            Utils.animation.scrollTo(document.body, 800);
        });
    }
    
    setupContactForm() {
        const contactForm = Utils.dom.get('#contact-form');
        if (!contactForm) return;
        
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = Utils.form.getData(contactForm);
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Validate form
            if (!this.validateContactForm(formData)) {
                return;
            }
            
            try {
                // Show loading state
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Invio in corso...';
                submitBtn.disabled = true;
                
                // Simulate API call (replace with actual endpoint)
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Show success message
                this.showNotification('Messaggio inviato con successo!', 'success');
                Utils.form.reset(contactForm);
                
            } catch (error) {
                console.error('Contact form error:', error);
                this.showNotification('Errore nell\'invio del messaggio. Riprova più tardi.', 'error');
            } finally {
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }
    
    validateContactForm(data) {
        let isValid = true;
        
        // Validate name
        if (!data.name || data.name.trim().length < 2) {
            this.showFieldError('name', 'Il nome deve essere di almeno 2 caratteri');
            isValid = false;
        }
        
        // Validate email
        if (!data.email || !Utils.form.isValidEmail(data.email)) {
            this.showFieldError('email', 'Inserisci un indirizzo email valido');
            isValid = false;
        }
        
        // Validate subject
        if (!data.subject || data.subject.trim().length < 5) {
            this.showFieldError('subject', 'L\'oggetto deve essere di almeno 5 caratteri');
            isValid = false;
        }
        
        // Validate message
        if (!data.message || data.message.trim().length < 10) {
            this.showFieldError('message', 'Il messaggio deve essere di almeno 10 caratteri');
            isValid = false;
        }
        
        return isValid;
    }
    
    showFieldError(fieldName, message) {
        const field = Utils.dom.get(`#${fieldName}`);
        if (field) {
            Utils.dom.addClass(field, 'error');
            
            // Remove existing error message
            const existingError = field.parentNode.querySelector('.error-message');
            if (existingError) {
                existingError.remove();
            }
            
            // Add error message
            const errorDiv = Utils.dom.create('div', 'error-message', message);
            field.parentNode.appendChild(errorDiv);
            
            // Remove error on input
            const removeError = () => {
                Utils.dom.removeClass(field, 'error');
                const errorMsg = field.parentNode.querySelector('.error-message');
                if (errorMsg) errorMsg.remove();
                field.removeEventListener('input', removeError);
            };
            
            field.addEventListener('input', removeError);
        }
    }
    
    setupSmoothScrolling() {
        // Already handled by NavigationManager, but add additional anchor links
        const anchorLinks = Utils.dom.getAll('a[href^="#"]:not(.nav-link)');
        
        anchorLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = Utils.dom.get(`#${targetId}`);
                
                if (targetElement) {
                    Utils.animation.scrollTo(targetElement, CONFIG.scroll.speed, CONFIG.scroll.offset);
                }
            });
        });
    }
    
    setupStatsCounter() {
        const stats = Utils.dom.getAll('.stat-number');
        
        stats.forEach(stat => {
            const targetValue = parseInt(stat.getAttribute('data-count'));
            
            // Create observer for this stat
            const observer = Utils.performance.createObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !stat.classList.contains('counted')) {
                        Utils.dom.addClass(stat, 'counted');
                        Utils.animation.countUp(stat, targetValue, CONFIG.skills.countUpDuration);
                        observer.unobserve(stat);
                    }
                });
            });
            
            observer.observe(stat);
        });
    }
    
    setupParallax() {
        const parallaxElements = Utils.dom.getAll('.hero-shapes .shape');
        
        if (parallaxElements.length === 0) return;
        
        const handleParallax = Utils.events.throttle(() => {
            const scrollY = window.scrollY;
            
            parallaxElements.forEach((element, index) => {
                const speed = 0.5 + (index * 0.1);
                const yPos = -(scrollY * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        }, 16);
        
        window.addEventListener('scroll', handleParallax);
    }
    
    setupScrollAnimations() {
        const animatedElements = Utils.dom.getAll('.scroll-animate');
        
        if (animatedElements.length === 0) return;
        
        const observer = Utils.performance.createObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    Utils.dom.addClass(entry.target, 'in-view');
                    
                    // Animate skill progress bars
                    if (entry.target.classList.contains('skill-card')) {
                        this.animateSkillProgress(entry.target);
                    }
                    
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
        
        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }
    
    animateSkillProgress(skillCard) {
        const progressBar = skillCard.querySelector('.progress-fill');
        if (progressBar) {
            const progress = progressBar.getAttribute('data-progress');
            setTimeout(() => {
                progressBar.style.width = `${progress}%`;
            }, 200);
        }
    }
    
    showLoadingScreen() {
        if (this.loadingScreen) {
            Utils.dom.removeClass(this.loadingScreen, 'hidden');
        }
    }
    
    async hideLoadingScreen() {
        if (!this.loadingScreen) return;
        
        // Ensure minimum loading time for better UX
        await new Promise(resolve => setTimeout(resolve, CONFIG.loading.minDuration));
        
        // Fade out loading screen
        Utils.dom.addClass(this.loadingScreen, 'hidden');
        
        // Remove from DOM after animation
        setTimeout(() => {
            if (this.loadingScreen.parentNode) {
                this.loadingScreen.parentNode.removeChild(this.loadingScreen);
            }
        }, CONFIG.loading.fadeOutDuration);
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = Utils.dom.create('div', `notification notification-${type}`);
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
                <button class="notification-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => Utils.dom.addClass(notification, 'show'), 100);
        
        // Auto hide after 5 seconds
        setTimeout(() => this.hideNotification(notification), 5000);
        
        // Close button handler
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => this.hideNotification(notification));
    }
    
    hideNotification(notification) {
        Utils.dom.removeClass(notification, 'show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
    
    getNotificationIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }
    
    showFallbackContent() {
        // Show static content if data loading fails
        console.log('Loading fallback content...');
        
        // You can add fallback HTML content here
        const skillsGrid = Utils.dom.get('#skills-grid');
        if (skillsGrid) {
            skillsGrid.innerHTML = '<p>Contenuto in caricamento...</p>';
        }
        
        const projectsGrid = Utils.dom.get('#projects-grid');
        if (projectsGrid) {
            projectsGrid.innerHTML = '<p>Progetti in caricamento...</p>';
        }
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('it-IT', {
            year: 'numeric',
            month: 'long'
        });
    }
    
    // Public methods for external access
    scrollToSection(sectionId) {
        if (window.NavigationManager) {
            window.NavigationManager.navigateToSection(sectionId);
        }
    }
    
    getCurrentTheme() {
        if (window.ThemeManager) {
            return window.ThemeManager.getCurrentTheme();
        }
        return 'light';
    }
    
    toggleTheme() {
        if (window.ThemeManager) {
            window.ThemeManager.toggleTheme();
        }
    }
}

// Initialize portfolio when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.portfolio = new Portfolio();
});

// Export for global access
window.Portfolio = Portfolio;