/*
===========================================
FILTERS MODULE - Portfolio
===========================================
Modulo per la gestione dei filtri nelle sezioni
Skills e Projects con animazioni fluide
*/

class FiltersModule {
    constructor() {
        this.skillsData = null;
        this.projectsData = null;
        this.activeFilters = {
            skills: 'all',
            projects: 'all'
        };
        this.animationConfig = {
            duration: 300,
            stagger: 50,
            easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
        };
        
        this.init();
    }

    /**
     * Inizializza il modulo filtri
     */
    async init() {
        this.bindEvents();
        await this.loadData();
        this.setupFilters();
        console.log('🔍 Filters Module: Initialized');
    }

    /**
     * Carica i dati da JSON
     */
    async loadData() {
        try {
            // Carica skills data
            const skillsResponse = await fetch('data/skills.json');
            if (skillsResponse.ok) {
                this.skillsData = await skillsResponse.json();
            }

            // Carica projects data (se esiste)
            try {
                const projectsResponse = await fetch('data/projects.json');
                if (projectsResponse.ok) {
                    this.projectsData = await projectsResponse.json();
                }
            } catch (error) {
                console.warn('⚠️ Projects data not found, using fallback');
                this.createProjectsFallback();
            }

        } catch (error) {
            console.error('❌ Error loading filter data:', error);
            this.handleDataError();
        }
    }

    /**
     * Imposta gli event listeners
     */
    bindEvents() {
        // Event delegation per i bottoni filtro
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('filter-btn')) {
                this.handleFilterClick(e);
            }
        });

        // Keyboard navigation per accessibilità
        document.addEventListener('keydown', (e) => {
            if (e.target.classList.contains('filter-btn')) {
                this.handleFilterKeyboard(e);
            }
        });

        // Reset filtri su resize (mobile)
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                this.handleResize();
            }, 250);
        });
    }

    /**
     * Configura i sistemi di filtri
     */
    setupFilters() {
        this.setupSkillsFilters();
        this.setupProjectsFilters();
        this.updateFilterCounts();
    }

    /**
     * Configura i filtri delle competenze
     */
    setupSkillsFilters() {
        const skillsSection = document.querySelector('#skills');
        if (!skillsSection || !this.skillsData) return;

        const filterContainer = skillsSection.querySelector('.skills-filter');
        const gridContainer = skillsSection.querySelector('.skills-grid');

        if (filterContainer && gridContainer) {
            this.updateFilterButtons(filterContainer, this.skillsData.categories, 'skills');
            this.renderSkillsGrid(gridContainer, this.skillsData.skills);
        }
    }

    /**
     * Configura i filtri dei progetti
     */
    setupProjectsFilters() {
        const projectsSection = document.querySelector('#projects');
        if (!projectsSection) return;

        const filterContainer = projectsSection.querySelector('.projects-filter');
        const gridContainer = projectsSection.querySelector('.projects-grid');

        if (filterContainer && gridContainer) {
            if (this.projectsData && this.projectsData.categories) {
                this.updateFilterButtons(filterContainer, this.projectsData.categories, 'projects');
            }
            
            // Se non ci sono dati progetti, mostra messaggio di caricamento
            if (!this.projectsData) {
                this.showProjectsPlaceholder(gridContainer);
            }
        }
    }

    /**
     * Aggiorna i bottoni filtro con i conteggi
     */
    updateFilterButtons(container, categories, type) {
        const buttons = container.querySelectorAll('.filter-btn');
        
        buttons.forEach(button => {
            const filterId = button.getAttribute(`data-${type === 'skills' ? 'category' : 'filter'}`);
            const category = categories.find(cat => cat.id === filterId);
            
            if (category && category.count !== undefined) {
                const currentText = button.textContent.trim();
                if (!currentText.includes('(')) {
                    button.innerHTML = `${currentText} <span class="filter-count">(${category.count})</span>`;
                }
            }
        });
    }

    /**
     * Renderizza la griglia delle competenze
     */
    renderSkillsGrid(container, skills) {
        if (!skills || skills.length === 0) {
            container.innerHTML = this.createEmptyState('skills');
            return;
        }

        container.innerHTML = skills.map(skill => this.createSkillCard(skill)).join('');
        this.animateGridItems(container);
    }

    /**
     * Crea una skill card
     */
    createSkillCard(skill) {
        const technologies = skill.technologies || [];
        const tags = skill.tags || [];
        const levelInfo = this.getSkillLevelInfo(skill.level);

        return `
            <div class="skill-card" data-category="${skill.category}" data-skill-id="${skill.id}">
                <div class="skill-header">
                    <div class="skill-icon">
                        <i class="${skill.icon || 'fas fa-code'}"></i>
                    </div>
                    <div class="skill-info">
                        <h3 class="skill-name">${skill.name}</h3>
                        <div class="skill-level">
                            <div class="skill-level-bar">
                                <div class="skill-level-fill" data-level="${skill.level}" style="width: 0%"></div>
                            </div>
                            <span class="skill-percentage">${skill.level}%</span>
                        </div>
                    </div>
                </div>
                
                <p class="skill-description">${skill.description}</p>
                
                ${technologies.length > 0 ? `
                    <div class="skill-technologies">
                        ${technologies.slice(0, 4).map(tech => `
                            <div class="tech-item">
                                <span class="tech-name">${tech.name}</span>
                                <div class="tech-level">
                                    <div class="tech-level-fill" data-level="${tech.level}" style="width: 0%"></div>
                                </div>
                            </div>
                        `).join('')}
                        ${technologies.length > 4 ? `<div class="tech-more">+${technologies.length - 4} più</div>` : ''}
                    </div>
                ` : ''}
                
                ${tags.length > 0 ? `
                    <div class="skill-tags">
                        ${tags.slice(0, 6).map(tag => `<span class="skill-tag">${tag}</span>`).join('')}
                        ${tags.length > 6 ? `<span class="skill-tag">+${tags.length - 6}</span>` : ''}
                    </div>
                ` : ''}
                
                <div class="skill-footer">
                    <div class="skill-experience">${skill.years_experience || 0} anni</div>
                    <div class="skill-projects">${(skill.projects || []).length} progetti</div>
                </div>
            </div>
        `;
    }

    /**
     * Gestisce il click sui filtri
     */
    handleFilterClick(e) {
        e.preventDefault();
        
        const button = e.target;
        const section = this.getFilterSection(button);
        
        if (!section) return;

        // Rimuovi classe active da tutti i bottoni della sezione
        const allButtons = section.querySelectorAll('.filter-btn');
        allButtons.forEach(btn => btn.classList.remove('active'));
        
        // Aggiungi classe active al bottone cliccato
        button.classList.add('active');
        
        // Determina il tipo di filtro
        const isSkillsFilter = section.closest('#skills');
        const filterType = isSkillsFilter ? 'skills' : 'projects';
        const filterValue = button.getAttribute(isSkillsFilter ? 'data-category' : 'data-filter');
        
        // Aggiorna filtro attivo
        this.activeFilters[filterType] = filterValue;
        
        // Applica il filtro
        this.applyFilter(filterType, filterValue);
        
        // Analytics (se disponibile)
        this.trackFilterUsage(filterType, filterValue);
    }

    /**
     * Applica il filtro selezionato
     */
    applyFilter(type, value) {
        const section = document.querySelector(`#${type === 'skills' ? 'skills' : 'projects'}`);
        if (!section) return;

        const grid = section.querySelector(`.${type === 'skills' ? 'skills' : 'projects'}-grid`);
        const items = grid.querySelectorAll(type === 'skills' ? '.skill-card' : '.project-card');

        // Anima l'uscita degli elementi
        this.animateFilterOut(items, () => {
            // Filtra gli elementi
            items.forEach(item => {
                const shouldShow = this.shouldShowItem(item, type, value);
                item.style.display = shouldShow ? '' : 'none';
                
                if (shouldShow) {
                    item.classList.add('filter-match');
                } else {
                    item.classList.remove('filter-match');
                }
            });

            // Anima l'entrata degli elementi visibili
            const visibleItems = Array.from(items).filter(item => item.style.display !== 'none');
            this.animateFilterIn(visibleItems);

            // Aggiorna conteggi
            this.updateResultsCount(type, visibleItems.length);
        });
    }

    /**
     * Determina se un elemento deve essere mostrato
     */
    shouldShowItem(item, type, filterValue) {
        if (filterValue === 'all') return true;

        const attribute = type === 'skills' ? 'data-category' : 'data-filter';
        const itemCategories = item.getAttribute(attribute);
        
        if (!itemCategories) return false;

        // Supporta multiple categorie separate da virgola
        const categories = itemCategories.split(',').map(cat => cat.trim());
        return categories.includes(filterValue);
    }

    /**
     * Anima l'uscita degli elementi durante il filtro
     */
    animateFilterOut(items, callback) {
        const visibleItems = Array.from(items).filter(item => 
            item.style.display !== 'none' && item.offsetParent !== null
        );

        if (visibleItems.length === 0) {
            callback();
            return;
        }

        visibleItems.forEach((item, index) => {
            setTimeout(() => {
                item.style.transition = `all ${this.animationConfig.duration}ms ${this.animationConfig.easing}`;
                item.style.transform = 'translateY(20px)';
                item.style.opacity = '0';
                
                if (index === visibleItems.length - 1) {
                    setTimeout(callback, this.animationConfig.duration);
                }
            }, index * this.animationConfig.stagger);
        });
    }

    /**
     * Anima l'entrata degli elementi durante il filtro
     */
    animateFilterIn(items) {
        items.forEach((item, index) => {
            // Reset immediato
            item.style.transform = 'translateY(20px)';
            item.style.opacity = '0';
            
            setTimeout(() => {
                item.style.transition = `all ${this.animationConfig.duration}ms ${this.animationConfig.easing}`;
                item.style.transform = 'translateY(0)';
                item.style.opacity = '1';
                
                // Anima anche le barre di progresso se presenti
                setTimeout(() => {
                    this.animateProgressBars(item);
                }, this.animationConfig.duration / 2);
                
            }, index * this.animationConfig.stagger + 100);
        });
    }

    /**
     * Anima le barre di progresso nelle skill cards
     */
    animateProgressBars(container) {
        const skillBars = container.querySelectorAll('.skill-level-fill[data-level]');
        const techBars = container.querySelectorAll('.tech-level-fill[data-level]');
        
        [...skillBars, ...techBars].forEach((bar, index) => {
            setTimeout(() => {
                const level = bar.getAttribute('data-level');
                bar.style.width = `${level}%`;
            }, index * 100);
        });
    }

    /**
     * Anima gli elementi della griglia al caricamento iniziale
     */
    animateGridItems(container) {
        const items = container.querySelectorAll('.skill-card, .project-card');
        
        items.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                item.style.transition = `all ${this.animationConfig.duration}ms ${this.animationConfig.easing}`;
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
                
                // Anima le barre di progresso
                setTimeout(() => {
                    this.animateProgressBars(item);
                }, this.animationConfig.duration);
                
            }, index * this.animationConfig.stagger);
        });
    }

    /**
     * Gestisce la navigazione da tastiera per accessibilità
     */
    handleFilterKeyboard(e) {
        const button = e.target;
        const container = this.getFilterSection(button);
        const buttons = Array.from(container.querySelectorAll('.filter-btn'));
        const currentIndex = buttons.indexOf(button);

        switch (e.key) {
            case 'ArrowLeft':
            case 'ArrowUp':
                e.preventDefault();
                const prevIndex = currentIndex > 0 ? currentIndex - 1 : buttons.length - 1;
                buttons[prevIndex].focus();
                break;
                
            case 'ArrowRight':
            case 'ArrowDown':
                e.preventDefault();
                const nextIndex = currentIndex < buttons.length - 1 ? currentIndex + 1 : 0;
                buttons[nextIndex].focus();
                break;
                
            case 'Enter':
            case ' ':
                e.preventDefault();
                button.click();
                break;
        }
    }

    /**
     * Trova la sezione contenente il filtro
     */
    getFilterSection(button) {
        return button.closest('.skills-filter') || button.closest('.projects-filter');
    }

    /**
     * Aggiorna il conteggio dei risultati
     */
    updateResultsCount(type, count) {
        const section = document.querySelector(`#${type === 'skills' ? 'skills' : 'projects'}`);
        let counter = section.querySelector('.results-counter');
        
        if (!counter) {
            counter = document.createElement('div');
            counter.className = 'results-counter';
            const header = section.querySelector('.section-header');
            if (header) {
                header.appendChild(counter);
            }
        }
        
        const totalItems = this.getTotalItemsCount(type);
        const isFiltered = this.activeFilters[type] !== 'all';
        
        if (isFiltered) {
            counter.textContent = `Mostrati ${count} di ${totalItems}`;
            counter.style.opacity = '1';
        } else {
            counter.style.opacity = '0';
        }
    }

    /**
     * Ottiene il conteggio totale degli elementi
     */
    getTotalItemsCount(type) {
        if (type === 'skills' && this.skillsData) {
            return this.skillsData.skills.length;
        }
        if (type === 'projects' && this.projectsData) {
            return this.projectsData.projects ? this.projectsData.projects.length : 0;
        }
        return 0;
    }

    /**
     * Aggiorna i conteggi sui filtri
     */
    updateFilterCounts() {
        // Aggiorna conteggi skills
        if (this.skillsData && this.skillsData.categories) {
            this.skillsData.categories.forEach(category => {
                if (category.id === 'all') {
                    category.count = this.skillsData.skills.length;
                } else {
                    category.count = this.skillsData.skills.filter(skill => 
                        skill.category === category.id
                    ).length;
                }
            });
        }

        // Aggiorna conteggi projects (se disponibili)
        if (this.projectsData && this.projectsData.categories && this.projectsData.projects) {
            this.projectsData.categories.forEach(category => {
                if (category.id === 'all') {
                    category.count = this.projectsData.projects.length;
                } else {
                    category.count = this.projectsData.projects.filter(project => 
                        project.category === category.id || 
                        (project.categories && project.categories.includes(category.id))
                    ).length;
                }
            });
        }
    }

    /**
     * Ottiene informazioni sul livello di competenza
     */
    getSkillLevelInfo(level) {
        if (!this.skillsData || !this.skillsData.skill_levels) {
            return { label: 'N/A', color: '#6b7280' };
        }

        const levels = this.skillsData.skill_levels;
        for (const [key, levelInfo] of Object.entries(levels)) {
            if (level >= levelInfo.min && level <= levelInfo.max) {
                return levelInfo;
            }
        }
        
        return { label: 'N/A', color: '#6b7280' };
    }

    /**
     * Crea fallback per dati progetti mancanti
     */
    createProjectsFallback() {
        this.projectsData = {
            categories: [
                { id: 'all', name: 'Tutti', count: 0 },
                { id: 'web', name: 'Web Development', count: 0 },
                { id: 'python', name: 'Python', count: 0 },
                { id: 'data', name: 'Data & AI', count: 0 },
                { id: 'iot', name: 'IoT', count: 0 }
            ]
        };
    }

    /**
     * Mostra placeholder per progetti
     */
    showProjectsPlaceholder(container) {
        container.innerHTML = `
            <div class="projects-loading">
                <div class="project-skeleton">
                    <div class="skeleton-image"></div>
                    <div class="skeleton-content">
                        <div class="skeleton-title"></div>
                        <div class="skeleton-description"></div>
                        <div class="skeleton-tags"></div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Crea stato vuoto
     */
    createEmptyState(type) {
        return `
            <div class="${type}-empty">
                <div class="empty-icon">
                    <i class="fas fa-${type === 'skills' ? 'tools' : 'folder-open'}"></i>
                </div>
                <h3>Nessun elemento trovato</h3>
                <p>Prova a selezionare un filtro diverso</p>
            </div>
        `;
    }

    /**
     * Gestisce errori di caricamento dati
     */
    handleDataError() {
        console.error('❌ Impossibile caricare i dati per i filtri');
        
        // Disabilita i filtri se i dati non sono disponibili
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(button => {
            if (button.getAttribute('data-category') !== 'all' && 
                button.getAttribute('data-filter') !== 'all') {
                button.disabled = true;
                button.style.opacity = '0.5';
            }
        });
    }

    /**
     * Gestisce il resize della finestra
     */
    handleResize() {
        // Riapplica animazioni se necessario
        if (window.innerWidth <= 768) {
            // Mobile: riduce durata animazioni
            this.animationConfig.duration = 200;
            this.animationConfig.stagger = 30;
        } else {
            // Desktop: ripristina durata normale
            this.animationConfig.duration = 300;
            this.animationConfig.stagger = 50;
        }
    }

    /**
     * Traccia l'utilizzo dei filtri (analytics)
     */
    trackFilterUsage(type, value) {
        // Implementa tracking analytics se necessario
        console.log(`📊 Filter used: ${type} -> ${value}`);
        
        // Esempio: Google Analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'filter_used', {
                'section': type,
                'filter_value': value
            });
        }
    }

    /**
     * Metodi pubblici per controllo esterno
     */
    setFilter(type, value) {
        const section = document.querySelector(`#${type === 'skills' ? 'skills' : 'projects'}`);
        if (!section) return;

        const button = section.querySelector(`[data-${type === 'skills' ? 'category' : 'filter'}="${value}"]`);
        if (button) {
            button.click();
        }
    }

    getActiveFilter(type) {
        return this.activeFilters[type];
    }

    resetAllFilters() {
        this.setFilter('skills', 'all');
        this.setFilter('projects', 'all');
    }

    /**
     * Cleanup
     */
    destroy() {
        // Rimuovi event listeners se necessario
        console.log('🗑️ Filters Module: Destroyed');
    }
}

// Export per uso modulare
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FiltersModule;
}

// Inizializzazione automatica quando il DOM è pronto
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.filtersModule = new FiltersModule();
        });
    } else {
        window.filtersModule = new FiltersModule();
    }
}