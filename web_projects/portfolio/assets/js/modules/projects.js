/*
===========================================
PROJECTS MODULE
===========================================
Carica e gestisce la sezione progetti
*/

(function() {
    'use strict';

    // Variabili del modulo
    let projectsData = null;
    let projectsGrid = null;
    let filterButtons = null;
    let currentFilter = 'all';
    let projectsLoaded = false;
    let isAnimating = false;

    /* ================================ */
    /* INIZIALIZZAZIONE                 */
    /* ================================ */
    function init() {
        // Ottieni riferimenti elementi DOM
        projectsGrid = document.getElementById('projects-grid');
        filterButtons = document.querySelectorAll('.projects-filter .filter-btn');

        if (!projectsGrid) {
            console.warn('Projects grid not found');
            return;
        }

        // Setup filtri
        setupFilters();

        // Carica dati progetti
        loadProjectsData();

        window.PortfolioConfig.utils.log('debug', 'Projects module initialized');
    }

    /* ================================ */
    /* CARICAMENTO DATI                 */
    /* ================================ */
    async function loadProjectsData() {
        try {
            showLoadingState();

            const response = await fetch(window.PortfolioConfig.paths.data.projects);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            projectsData = await response.json();
            
            // Valida dati
            if (!projectsData || !projectsData.projects || !Array.isArray(projectsData.projects)) {
                throw new Error('Invalid projects data format');
            }

            // Ordina progetti per priorità e data
            projectsData.projects.sort((a, b) => {
                if (a.priority !== b.priority) {
                    return a.priority - b.priority;
                }
                return new Date(b.date_updated) - new Date(a.date_updated);
            });

            // Renderizza progetti
            renderProjects();
            setupProjectsAnimations();
            
            projectsLoaded = true;
            window.PortfolioConfig.utils.log('info', `Loaded ${projectsData.projects.length} projects`);

        } catch (error) {
            console.error('Error loading projects data:', error);
            showErrorMessage();
        }
    }

    /* ================================ */
    /* RENDERING PROGETTI               */
    /* ================================ */
    function renderProjects() {
        if (!projectsData || !projectsGrid) return;

        // Filtra progetti in base al filtro corrente
        const filteredProjects = filterProjects(projectsData.projects, currentFilter);

        if (filteredProjects.length === 0) {
            showEmptyState();
            return;
        }

        // Genera HTML
        const projectsHTML = filteredProjects.map(project => createProjectCard(project)).join('');

        // Aggiorna grid
        projectsGrid.innerHTML = projectsHTML;

        // Avvia animazioni
        animateProjectCards();
    }

    function createProjectCard(project) {
        const statusInfo = getProjectStatus(project.status);
        const techTags = project.technologies.slice(0, 4); // Mostra prime 4 tecnologie
        const isFeatured = project.featured ? 'featured' : '';

        return `
            <div class="project-card ${isFeatured}" data-category="${project.category}" data-status="${project.status}">
                <div class="project-image">
                    <img src="${project.image}" alt="${project.title}" loading="lazy" onerror="this.src='assets/images/projects/placeholder.jpg'">
                    <div class="project-overlay">
                        <div class="project-links">
                            ${project.links.github ? `
                                <a href="${project.links.github}" class="project-link" target="_blank" rel="noopener" title="Codice GitHub">
                                    <i class="fab fa-github"></i>
                                </a>
                            ` : ''}
                            ${project.links.live ? `
                                <a href="${project.links.live}" class="project-link" target="_blank" rel="noopener" title="Sito Live">
                                    <i class="fas fa-external-link-alt"></i>
                                </a>
                            ` : ''}
                            ${project.links.demo ? `
                                <a href="${project.links.demo}" class="project-link" target="_blank" rel="noopener" title="Demo">
                                    <i class="fas fa-play"></i>
                                </a>
                            ` : ''}
                        </div>
                        <button class="project-details-btn" onclick="window.ProjectsModule.showDetails('${project.id}')">
                            <i class="fas fa-info-circle"></i>
                            Dettagli
                        </button>
                    </div>
                    ${project.featured ? '<div class="project-featured-badge">In Evidenza</div>' : ''}
                    <div class="project-status" style="background-color: ${statusInfo.color};">
                        <i class="${statusInfo.icon}"></i>
                        <span>${statusInfo.label}</span>
                    </div>
                </div>
                
                <div class="project-content">
                    <div class="project-header">
                        <h3 class="project-title">${project.title}</h3>
                        <div class="project-meta">
                            <span class="project-date">${formatDate(project.date_updated)}</span>
                            <span class="project-duration">${project.duration}</span>
                        </div>
                    </div>
                    
                    <p class="project-description">${truncateText(project.description, 120)}</p>
                    
                    <div class="project-technologies">
                        ${techTags.map(tech => `
                            <span class="tech-tag">${tech}</span>
                        `).join('')}
                        ${project.technologies.length > 4 ? `
                            <span class="tech-more">+${project.technologies.length - 4}</span>
                        ` : ''}
                    </div>
                    
                    <div class="project-footer">
                        <div class="project-stats">
                            <span class="stat-item">
                                <i class="fas fa-code"></i>
                                ${project.technologies.length} tech
                            </span>
                            <span class="stat-item">
                                <i class="fas fa-calendar"></i>
                                ${project.duration}
                            </span>
                            ${project.team_size > 1 ? `
                                <span class="stat-item">
                                    <i class="fas fa-users"></i>
                                    ${project.team_size} membri
                                </span>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /* ================================ */
    /* FILTRI PROGETTI                  */
    /* ================================ */
    function setupFilters() {
        if (!filterButtons.length) return;

        filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                
                const category = button.getAttribute('data-filter');
                if (category && category !== currentFilter && !isAnimating) {
                    updateFilter(category);
                }
            });
        });
    }

    function updateFilter(newFilter) {
        if (isAnimating) return;
        
        currentFilter = newFilter;
        isAnimating = true;

        // Aggiorna UI filtri
        filterButtons.forEach(button => {
            const category = button.getAttribute('data-filter');
            button.classList.toggle('active', category === currentFilter);
        });

        // Anima uscita progetti correnti
        const currentCards = projectsGrid.querySelectorAll('.project-card');
        
        Promise.all(Array.from(currentCards).map((card, index) => {
            return new Promise(resolve => {
                setTimeout(() => {
                    card.style.transition = 'all 0.3s ease';
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px) scale(0.9)';
                    resolve();
                }, index * 50);
            });
        })).then(() => {
            // Re-renderizza progetti dopo animazione uscita
            setTimeout(() => {
                if (projectsLoaded) {
                    renderProjects();
                }
                isAnimating = false;
            }, 300);
        });

        window.PortfolioConfig.utils.log('debug', `Projects filtered by: ${currentFilter}`);
    }

    function filterProjects(projects, category) {
        if (category === 'all') {
            return projects;
        }
        return projects.filter(project => project.category === category);
    }

    /* ================================ */
    /* DETTAGLI PROGETTO                */
    /* ================================ */
    function showProjectDetails(projectId) {
        const project = projectsData.projects.find(p => p.id === projectId);
        if (!project) return;

        // Crea e mostra modal con dettagli completi
        const modal = createProjectModal(project);
        document.body.appendChild(modal);
        
        // Mostra modal con animazione
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);

        // Gestisci chiusura modal
        setupModalClosing(modal);

        window.PortfolioConfig.utils.log('debug', `Showing details for project: ${projectId}`);
    }

    function createProjectModal(project) {
        const statusInfo = getProjectStatus(project.status);
        
        const modal = document.createElement('div');
        modal.className = 'project-modal';
        modal.innerHTML = `
            <div class="modal-backdrop"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h2>${project.title}</h2>
                    <button class="modal-close" aria-label="Chiudi">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <div class="modal-body">
                    <div class="project-detail-image">
                        <img src="${project.image}" alt="${project.title}">
                        <div class="project-status-large" style="background-color: ${statusInfo.color};">
                            <i class="${statusInfo.icon}"></i>
                            ${statusInfo.label}
                        </div>
                    </div>
                    
                    <div class="project-detail-info">
                        <div class="project-description-full">
                            <h3>Descrizione</h3>
                            <p>${project.description}</p>
                        </div>
                        
                        <div class="project-features">
                            <h3>Caratteristiche Principali</h3>
                            <ul>
                                ${project.features.map(feature => `<li>${feature}</li>`).join('')}
                            </ul>
                        </div>
                        
                        <div class="project-technologies-full">
                            <h3>Tecnologie Utilizzate</h3>
                            <div class="tech-tags">
                                ${project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                            </div>
                        </div>
                        
                        <div class="project-challenges">
                            <h3>Sfide Affrontate</h3>
                            <ul>
                                ${project.challenges.map(challenge => `<li>${challenge}</li>`).join('')}
                            </ul>
                        </div>
                        
                        <div class="project-learnings">
                            <h3>Competenze Acquisite</h3>
                            <ul>
                                ${project.learnings.map(learning => `<li>${learning}</li>`).join('')}
                            </ul>
                        </div>
                        
                        <div class="project-meta-full">
                            <div class="meta-item">
                                <strong>Ruolo:</strong> ${project.role}
                            </div>
                            <div class="meta-item">
                                <strong>Durata:</strong> ${project.duration}
                            </div>
                            <div class="meta-item">
                                <strong>Team:</strong> ${project.team_size} ${project.team_size === 1 ? 'persona' : 'persone'}
                            </div>
                            <div class="meta-item">
                                <strong>Ultimo aggiornamento:</strong> ${formatDate(project.date_updated)}
                            </div>
                        </div>
                        
                        <div class="project-links-full">
                            ${project.links.github ? `
                                <a href="${project.links.github}" class="btn btn-primary" target="_blank" rel="noopener">
                                    <i class="fab fa-github"></i>
                                    Codice GitHub
                                </a>
                            ` : ''}
                            ${project.links.live ? `
                                <a href="${project.links.live}" class="btn btn-secondary" target="_blank" rel="noopener">
                                    <i class="fas fa-external-link-alt"></i>
                                    Sito Live
                                </a>
                            ` : ''}
                            ${project.links.demo ? `
                                <a href="${project.links.demo}" class="btn btn-outline" target="_blank" rel="noopener">
                                    <i class="fas fa-play"></i>
                                    Demo
                                </a>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        return modal;
    }

    function setupModalClosing(modal) {
        const closeBtn = modal.querySelector('.modal-close');
        const backdrop = modal.querySelector('.modal-backdrop');
        
        const closeModal = () => {
            modal.classList.remove('active');
            setTimeout(() => {
                document.body.removeChild(modal);
            }, 300);
        };
        
        closeBtn.addEventListener('click', closeModal);
        backdrop.addEventListener('click', closeModal);
        
        // Chiudi con ESC
        const handleKeydown = (e) => {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', handleKeydown);
            }
        };
        document.addEventListener('keydown', handleKeydown);
    }

    /* ================================ */
    /* ANIMAZIONI                       */
    /* ================================ */
    function setupProjectsAnimations() {
        const observer = window.PortfolioConfig.utils.createObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateProjectCards();
                    observer.unobserve(entry.target);
                }
            });
        });

        const projectsSection = document.getElementById('projects');
        if (projectsSection) {
            observer.observe(projectsSection);
        }
    }

    function animateProjectCards() {
        const projectCards = projectsGrid.querySelectorAll('.project-card');
        
        projectCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 150);
        });
    }

    /* ================================ */
    /* STATI SPECIALI                   */
    /* ================================ */
    function showLoadingState() {
        if (!projectsGrid) return;
        
        projectsGrid.innerHTML = `
            <div class="projects-loading">
                ${Array(6).fill(0).map(() => `
                    <div class="project-skeleton">
                        <div class="skeleton-image"></div>
                        <div class="skeleton-content">
                            <div class="skeleton-title"></div>
                            <div class="skeleton-description"></div>
                            <div class="skeleton-tags"></div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    function showErrorMessage() {
        if (!projectsGrid) return;
        
        projectsGrid.innerHTML = `
            <div class="projects-error">
                <div class="error-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3>Errore nel caricamento dei progetti</h3>
                <p>Non è stato possibile caricare i dati dei progetti. Riprova più tardi.</p>
                <button class="btn btn-primary" onclick="window.ProjectsModule.reload()">
                    <i class="fas fa-redo"></i>
                    Riprova
                </button>
            </div>
        `;
    }

    function showEmptyState() {
        if (!projectsGrid) return;
        
        projectsGrid.innerHTML = `
            <div class="projects-empty">
                <div class="empty-icon">
                    <i class="fas fa-folder-open"></i>
                </div>
                <h3>Nessun progetto trovato</h3>
                <p>Non ci sono progetti per la categoria selezionata.</p>
                <button class="btn btn-secondary" onclick="window.ProjectsModule.filter('all')">
                    Mostra tutti i progetti
                </button>
            </div>
        `;
    }

    /* ================================ */
    /* UTILITIES                        */
    /* ================================ */
    function getProjectStatus(status) {
        if (!projectsData || !projectsData.project_status) {
            return { label: status, color: '#6b7280', icon: 'fas fa-circle' };
        }
        return projectsData.project_status[status] || { label: status, color: '#6b7280', icon: 'fas fa-circle' };
    }

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('it-IT', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    function truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength) + '...';
    }

    /* ================================ */
    /* API PUBBLICA                     */
    /* ================================ */
    window.ProjectsModule = {
        init,
        reload: () => {
            projectsLoaded = false;
            loadProjectsData();
        },
        filter: updateFilter,
        showDetails: showProjectDetails,
        getData: () => projectsData,
        getCurrentFilter: () => currentFilter
    };

    /* ================================ */
    /* AUTO-INIZIALIZZAZIONE            */
    /* ================================ */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Cerca questa funzione e sostituiscila COMPLETAMENTE
function createProjectHTML(project) {
    return `
        <div class="project-card" data-category="${project.category}">
            <div class="project-image">
                <img src="${project.image}" alt="${project.title}" loading="lazy">
                <div class="project-overlay">
                    <div class="project-status ${project.status}">
                        ${getStatusLabel(project.status)}
                    </div>
                </div>
            </div>
            
            <div class="project-content">
                <h3 class="project-title">${project.title}</h3>
                <p class="project-description">${project.description}</p>
                
                <div class="project-technologies">
                    ${project.technologies.map(tech => `
                        <span class="tech-tag">${tech}</span>
                    `).join('')}
                </div>
                
                <div class="project-footer">
                    <div class="project-links">
                        ${project.links.github ? `
                            <a href="${project.links.github}" class="project-link" target="_blank" rel="noopener">
                                <i class="fa-brands fa-github"></i>
                                <span>GitHub</span>
                            </a>
                        ` : ''}
                        ${project.links.live ? `
                            <a href="${project.links.live}" class="project-link" target="_blank" rel="noopener">
                                <i class="fa-solid fa-external-link-alt"></i>
                                <span>Demo</span>
                            </a>
                        ` : ''}
                    </div>
                    
                    <div class="project-meta">
                        <span>${project.duration || 'N/A'}</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

})();