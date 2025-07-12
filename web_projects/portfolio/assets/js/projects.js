// Projects Management Module

const ProjectsManager = {
    // Initialize projects management
    init() {
        this.projectsGrid = Utils.dom.get('#projects-grid');
        this.projectCards = [];
        this.projects = [];
        this.isLoading = false;
        
        if (!this.projectsGrid) {
            console.warn('Projects grid not found');
            return;
        }
        
        this.loadProjects();
        this.setupEventListeners();
        
        console.log('Projects Manager initialized');
    },
    
    // Load projects from JSON
    async loadProjects() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.showLoadingState();
        
        try {
            const response = await Utils.api.get(CONFIG.api.projects);
            this.projects = response.projects || [];
            this.renderProjects();
            this.setupProjectInteractions();
            
        } catch (error) {
            console.error('Error loading projects:', error);
            this.showErrorState();
        } finally {
            this.hideLoadingState();
            this.isLoading = false;
        }
    },
    
    // Render projects to grid
    renderProjects(projectsToRender = null) {
        const projects = projectsToRender || this.projects;
        
        if (!projects || projects.length === 0) {
            this.showEmptyState();
            return;
        }
        
        // Clear existing content
        this.projectsGrid.innerHTML = '';
        
        // Create project cards
        projects.forEach((project, index) => {
            const projectCard = this.createProjectCard(project, index);
            this.projectsGrid.appendChild(projectCard);
        });
        
        // Update project cards reference
        this.projectCards = Utils.dom.getAll('.project-card');
        
        // Setup scroll animations
        this.setupScrollAnimations();
        
        // Initialize filters if available
        if (window.ProjectFilters) {
            setTimeout(() => {
                window.ProjectFilters.init();
            }, 100);
        }
    },
    
    // Create individual project card
    createProjectCard(project, index) {
        const card = Utils.dom.create('div', `project-card ${project.category} scroll-animate`);
        card.setAttribute('data-category', project.category);
        card.setAttribute('data-index', index);
        card.style.animationDelay = `${index * 0.1}s`;
        
        const statusClass = project.status === 'completed' ? 'status-completed' : 'status-in-progress';
        const statusText = project.status === 'completed' ? 'Completato' : 'In Corso';
        
        card.innerHTML = `
            <div class="project-image">
                <img src="${project.image}" alt="${project.title}" loading="lazy" class="project-img">
                <div class="project-overlay">
                    ${this.createProjectLinks(project.links)}
                </div>
                <div class="project-status-badge ${statusClass}">
                    ${statusText}
                </div>
            </div>
            <div class="project-content">
                <h3 class="project-title">${project.title}</h3>
                <p class="project-description">${project.description}</p>
                ${project.features ? this.createFeaturesList(project.features) : ''}
                <div class="project-tech">
                    ${project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                </div>
                <div class="project-meta">
                    <div class="project-info">
                        <span class="project-date">
                            <i class="fas fa-calendar"></i>
                            ${this.formatDate(project.date)}
                        </span>
                        ${project.duration ? `<span class="project-duration">
                            <i class="fas fa-clock"></i>
                            ${project.duration}
                        </span>` : ''}
                    </div>
                    ${project.highlights ? this.createHighlights(project.highlights) : ''}
                </div>
            </div>
        `;
        
        return card;
    },
    
    // Create project links
    createProjectLinks(links) {
        if (!links) return '';
        
        let linksHtml = '';
        
        if (links.live) {
            linksHtml += `
                <a href="${links.live}" class="project-link" target="_blank" rel="noopener" aria-label="Visualizza progetto live">
                    <i class="fas fa-external-link-alt"></i>
                </a>
            `;
        }
        
        if (links.github) {
            linksHtml += `
                <a href="${links.github}" class="project-link" target="_blank" rel="noopener" aria-label="Visualizza codice su GitHub">
                    <i class="fab fa-github"></i>
                </a>
            `;
        }
        
        if (links.demo) {
            linksHtml += `
                <a href="${links.demo}" class="project-link" target="_blank" rel="noopener" aria-label="Visualizza demo">
                    <i class="fas fa-play"></i>
                </a>
            `;
        }
        
        return linksHtml;
    },
    
    // Create features list
    createFeaturesList(features) {
        if (!features || features.length === 0) return '';
        
        return `
            <div class="project-features">
                <h4>Caratteristiche principali:</h4>
                <ul>
                    ${features.map(feature => `<li>${feature}</li>`).join('')}
                </ul>
            </div>
        `;
    },
    
    // Create highlights
    createHighlights(highlights) {
        if (!highlights || highlights.length === 0) return '';
        
        return `
            <div class="project-highlights">
                ${highlights.map(highlight => `
                    <span class="highlight-badge">
                        <i class="fas fa-star"></i>
                        ${highlight}
                    </span>
                `).join('')}
            </div>
        `;
    },
    
    // Setup event listeners
    setupEventListeners() {
        // Project card click for mobile
        document.addEventListener('click', (e) => {
            const projectCard = e.target.closest('.project-card');
            if (projectCard && Utils.device.isTouchDevice()) {
                this.handleProjectCardClick(projectCard);
            }
        });
        
        // Image lazy loading
        this.setupLazyLoading();
        
        // Keyboard navigation
        this.setupKeyboardNavigation();
    },
    
    // Setup project interactions
    setupProjectInteractions() {
        this.projectCards.forEach(card => {
            // Hover effects for desktop
            if (!Utils.device.isTouchDevice()) {
                this.setupHoverEffects(card);
            }
            
            // Click tracking
            this.setupClickTracking(card);
            
            // Accessibility
            this.setupAccessibility(card);
        });
    },
    
    // Setup hover effects
    setupHoverEffects(card) {
        const image = card.querySelector('.project-img');
        const overlay = card.querySelector('.project-overlay');
        
        card.addEventListener('mouseenter', () => {
            Utils.dom.addClass(card, 'hover');
            if (image) {
                Utils.dom.addClass(image, 'hover-scale');
            }
        });
        
        card.addEventListener('mouseleave', () => {
            Utils.dom.removeClass(card, 'hover');
            if (image) {
                Utils.dom.removeClass(image, 'hover-scale');
            }
        });
    },
    
    // Setup click tracking
    setupClickTracking(card) {
        const links = card.querySelectorAll('.project-link');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                const project = this.getProjectFromCard(card);
                const linkType = this.getLinkType(link);
                
                // Track click event
                this.trackProjectClick(project, linkType);
            });
        });
    },
    
    // Setup accessibility
    setupAccessibility(card) {
        // Add keyboard navigation
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'article');
        
        // Add ARIA labels
        const title = card.querySelector('.project-title')?.textContent;
        if (title) {
            card.setAttribute('aria-label', `Progetto: ${title}`);
        }
        
        // Keyboard interaction
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.handleProjectCardClick(card);
            }
        });
    },
    
    // Handle project card click
    handleProjectCardClick(card) {
        const project = this.getProjectFromCard(card);
        
        if (project && project.links) {
            // Priority: live > demo > github
            if (project.links.live) {
                window.open(project.links.live, '_blank', 'noopener');
            } else if (project.links.demo) {
                window.open(project.links.demo, '_blank', 'noopener');
            } else if (project.links.github) {
                window.open(project.links.github, '_blank', 'noopener');
            }
        }
    },
    
    // Get project data from card
    getProjectFromCard(card) {
        const index = parseInt(card.getAttribute('data-index'));
        return this.projects[index];
    },
    
    // Get link type from link element
    getLinkType(linkElement) {
        if (linkElement.href.includes('github')) return 'github';
        if (linkElement.querySelector('.fa-external-link-alt')) return 'live';
        if (linkElement.querySelector('.fa-play')) return 'demo';
        return 'unknown';
    },
    
    // Track project click
    trackProjectClick(project, linkType) {
        // Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'project_click', {
                event_category: 'Projects',
                event_label: project.title,
                link_type: linkType
            });
        }
        
        console.log(`Project clicked: ${project.title} (${linkType})`);
    },
    
    // Setup lazy loading for images
    setupLazyLoading() {
        const images = Utils.dom.getAll('.project-img[loading="lazy"]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = Utils.performance.createObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        Utils.performance.lazyLoadImage(img);
                        imageObserver.unobserve(img);
                    }
                });
            }, { rootMargin: '50px' });
            
            images.forEach(img => imageObserver.observe(img));
        }
    },
    
    // Setup keyboard navigation
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (e.target.closest('.project-card')) {
                const currentCard = e.target.closest('.project-card');
                const cards = Array.from(this.projectCards);
                const currentIndex = cards.indexOf(currentCard);
                
                let nextIndex = currentIndex;
                
                switch (e.key) {
                    case 'ArrowRight':
                    case 'ArrowDown':
                        e.preventDefault();
                        nextIndex = (currentIndex + 1) % cards.length;
                        break;
                    case 'ArrowLeft':
                    case 'ArrowUp':
                        e.preventDefault();
                        nextIndex = (currentIndex - 1 + cards.length) % cards.length;
                        break;
                    case 'Home':
                        e.preventDefault();
                        nextIndex = 0;
                        break;
                    case 'End':
                        e.preventDefault();
                        nextIndex = cards.length - 1;
                        break;
                }
                
                if (nextIndex !== currentIndex) {
                    cards[nextIndex].focus();
                }
            }
        });
    },
    
    // Setup scroll animations
    setupScrollAnimations() {
        const animatedCards = Utils.dom.getAll('.project-card.scroll-animate');
        
        if (window.AnimationManager && animatedCards.length > 0) {
            // Use existing animation manager
            animatedCards.forEach(card => {
                const observer = Utils.performance.createObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            Utils.dom.addClass(entry.target, 'in-view');
                            observer.unobserve(entry.target);
                        }
                    });
                });
                
                observer.observe(card);
            });
        }
    },
    
    // Show loading state
    showLoadingState() {
        this.projectsGrid.innerHTML = `
            <div class="projects-loading">
                <div class="loading-spinner"></div>
                <p>Caricamento progetti...</p>
            </div>
        `;
    },
    
    // Hide loading state
    hideLoadingState() {
        const loadingElement = Utils.dom.get('.projects-loading');
        if (loadingElement) {
            loadingElement.remove();
        }
    },
    
    // Show error state
    showErrorState() {
        this.projectsGrid.innerHTML = `
            <div class="projects-error">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Errore nel caricamento</h3>
                <p>Non è stato possibile caricare i progetti. Riprova più tardi.</p>
                <button class="btn btn-primary" onclick="ProjectsManager.loadProjects()">
                    <i class="fas fa-refresh"></i>
                    Riprova
                </button>
            </div>
        `;
    },
    
    // Show empty state
    showEmptyState() {
        this.projectsGrid.innerHTML = `
            <div class="projects-empty">
                <i class="fas fa-folder-open"></i>
                <h3>Nessun progetto trovato</h3>
                <p>Non ci sono progetti da mostrare al momento.</p>
            </div>
        `;
    },
    
    // Format date
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('it-IT', {
            year: 'numeric',
            month: 'long'
        });
    },
    
    // Filter projects by category
    filterByCategory(category) {
        if (category === 'all') {
            this.renderProjects();
        } else {
            const filteredProjects = this.projects.filter(project => 
                project.category === category
            );
            this.renderProjects(filteredProjects);
        }
    },
    
    // Search projects
    searchProjects(query) {
        if (!query || query.trim() === '') {
            this.renderProjects();
            return;
        }
        
        const searchTerm = query.toLowerCase().trim();
        const filteredProjects = this.projects.filter(project => 
            project.title.toLowerCase().includes(searchTerm) ||
            project.description.toLowerCase().includes(searchTerm) ||
            project.technologies.some(tech => 
                tech.toLowerCase().includes(searchTerm)
            )
        );
        
        this.renderProjects(filteredProjects);
    },
    
    // Get project by ID
    getProjectById(id) {
        return this.projects.find(project => project.id === id);
    },
    
    // Get projects by category
    getProjectsByCategory(category) {
        return this.projects.filter(project => project.category === category);
    },
    
    // Get featured projects
    getFeaturedProjects() {
        return this.projects.filter(project => project.featured);
    }
};

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    ProjectsManager.init();
});

// Export for other modules
window.ProjectsManager = ProjectsManager;