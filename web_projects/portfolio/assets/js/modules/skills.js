/*
===========================================
SKILLS MODULE
===========================================
Carica e gestisce la sezione competenze
*/

(function() {
    'use strict';

    // Variabili del modulo
    let skillsData = null;
    let skillsGrid = null;
    let filterButtons = null;
    let currentFilter = 'all';
    let skillsLoaded = false;

    /* ================================ */
    /* INIZIALIZZAZIONE                 */
    /* ================================ */
    function init() {
        // Ottieni riferimenti elementi DOM
        skillsGrid = document.getElementById('skills-grid');
        filterButtons = document.querySelectorAll('.skills-filter .filter-btn');

        if (!skillsGrid) {
            console.warn('Skills grid not found');
            return;
        }

        // Setup filtri
        setupFilters();

        // Carica dati skills
        loadSkillsData();

        window.PortfolioConfig.utils.log('debug', 'Skills module initialized');
    }

    /* ================================ */
    /* CARICAMENTO DATI                 */
    /* ================================ */
    async function loadSkillsData() {
        try {
            const response = await fetch(window.PortfolioConfig.paths.data.skills);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            skillsData = await response.json();
            
            // Valida dati
            if (!skillsData || !skillsData.skills || !Array.isArray(skillsData.skills)) {
                throw new Error('Invalid skills data format');
            }

            // Renderizza skills
            renderSkills();
            setupSkillsAnimations();
            
            skillsLoaded = true;
            window.PortfolioConfig.utils.log('info', `Loaded ${skillsData.skills.length} skills`);

        } catch (error) {
            console.error('Error loading skills data:', error);
            showErrorMessage();
        }
    }

    /* ================================ */
    /* RENDERING SKILLS                 */
    /* ================================ */
    function renderSkills() {
        if (!skillsData || !skillsGrid) return;

        // Filtra skills in base al filtro corrente
        const filteredSkills = filterSkills(skillsData.skills, currentFilter);

        // Genera HTML
        const skillsHTML = filteredSkills.map(skill => createSkillCard(skill)).join('');

        // Aggiorna grid
        skillsGrid.innerHTML = skillsHTML;

        // Avvia animazioni
        animateSkillCards();
    }

    function createSkillCard(skill) {
        const levelColor = getSkillLevelColor(skill.level);
        const technologies = skill.technologies.slice(0, 3); // Mostra prime 3 tecnologie

        return `
            <div class="skill-card" data-category="${skill.category}" data-level="${skill.level}">
                <div class="skill-header">
                    <div class="skill-icon">
                        <i class="${skill.icon}"></i>
                    </div>
                    <div class="skill-info">
                        <h3 class="skill-name">${skill.name}</h3>
                        <div class="skill-level">
                            <div class="skill-level-bar">
                                <div class="skill-level-fill" 
                                     style="width: 0%; background-color: ${levelColor};"
                                     data-level="${skill.level}">
                                </div>
                            </div>
                            <span class="skill-percentage">0%</span>
                        </div>
                    </div>
                </div>
                
                <p class="skill-description">${skill.description}</p>
                
                <div class="skill-technologies">
                    ${technologies.map(tech => `
                        <div class="tech-item">
                            <span class="tech-name">${tech.name}</span>
                            <div class="tech-level">
                                <div class="tech-level-fill" 
                                     style="width: 0%;" 
                                     data-level="${tech.level}">
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <div class="skill-tags">
                    ${skill.tags.slice(0, 4).map(tag => `
                        <span class="skill-tag">${tag}</span>
                    `).join('')}
                </div>
                
                <div class="skill-footer">
                    <span class="skill-experience">${skill.years_experience} ${skill.years_experience === 1 ? 'anno' : 'anni'} di esperienza</span>
                    <span class="skill-projects">${skill.projects.length} progetti</span>
                </div>
            </div>
        `;
    }

    /* ================================ */
    /* FILTRI SKILLS                    */
    /* ================================ */
    function setupFilters() {
        if (!filterButtons.length) return;

        filterButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                
                const category = button.getAttribute('data-category');
                if (category && category !== currentFilter) {
                    updateFilter(category);
                }
            });
        });
    }

    function updateFilter(newFilter) {
        currentFilter = newFilter;

        // Aggiorna UI filtri
        filterButtons.forEach(button => {
            const category = button.getAttribute('data-category');
            button.classList.toggle('active', category === currentFilter);
        });

        // Re-renderizza skills
        if (skillsLoaded) {
            renderSkills();
        }

        window.PortfolioConfig.utils.log('debug', `Skills filtered by: ${currentFilter}`);
    }

    function filterSkills(skills, category) {
        if (category === 'all') {
            return skills;
        }
        return skills.filter(skill => skill.category === category);
    }

    /* ================================ */
    /* ANIMAZIONI                       */
    /* ================================ */
    function setupSkillsAnimations() {
        const observer = window.PortfolioConfig.utils.createObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateSkillBars(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        });

        // Osserva la sezione skills
        const skillsSection = document.getElementById('skills');
        if (skillsSection) {
            observer.observe(skillsSection);
        }
    }

    function animateSkillCards() {
        const skillCards = skillsGrid.querySelectorAll('.skill-card');
        
        skillCards.forEach((card, index) => {
            // Animazione di entrata scaglionata
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    function animateSkillBars(container) {
        // Anima barre principali delle skills
        const skillBars = container.querySelectorAll('.skill-level-fill');
        const percentageElements = container.querySelectorAll('.skill-percentage');
        
        skillBars.forEach((bar, index) => {
            const targetLevel = parseInt(bar.getAttribute('data-level'));
            const percentageEl = percentageElements[index];
            
            animateProgressBar(bar, targetLevel, (progress) => {
                if (percentageEl) {
                    percentageEl.textContent = `${progress}%`;
                }
            });
        });

        // Anima barre tecnologie
        const techBars = container.querySelectorAll('.tech-level-fill');
        techBars.forEach(bar => {
            const targetLevel = parseInt(bar.getAttribute('data-level'));
            setTimeout(() => {
                animateProgressBar(bar, targetLevel);
            }, 300);
        });
    }

    function animateProgressBar(element, targetWidth, callback = null) {
        let currentWidth = 0;
        const increment = targetWidth / 60; // 60 frame per animazione smooth
        
        const animate = () => {
            currentWidth += increment;
            
            if (currentWidth >= targetWidth) {
                currentWidth = targetWidth;
                element.style.width = `${currentWidth}%`;
                if (callback) callback(Math.round(currentWidth));
                return;
            }
            
            element.style.width = `${currentWidth}%`;
            if (callback) callback(Math.round(currentWidth));
            
            requestAnimationFrame(animate);
        };
        
        requestAnimationFrame(animate);
    }

    /* ================================ */
    /* UTILITIES                        */
    /* ================================ */
    function getSkillLevelColor(level) {
        if (!skillsData || !skillsData.skill_levels) {
            return '#3b82f6'; // Default blue
        }

        const levels = skillsData.skill_levels;
        
        if (level >= levels.expert.min) return levels.expert.color;
        if (level >= levels.advanced.min) return levels.advanced.color;
        if (level >= levels.intermediate.min) return levels.intermediate.color;
        return levels.beginner.color;
    }

    function getSkillLevelLabel(level) {
        if (!skillsData || !skillsData.skill_levels) {
            return 'N/A';
        }

        const levels = skillsData.skill_levels;
        
        if (level >= levels.expert.min) return levels.expert.label;
        if (level >= levels.advanced.min) return levels.advanced.label;
        if (level >= levels.intermediate.min) return levels.intermediate.label;
        return levels.beginner.label;
    }

    function showErrorMessage() {
        if (!skillsGrid) return;
        
        skillsGrid.innerHTML = `
            <div class="skills-error">
                <div class="error-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3>Errore nel caricamento delle competenze</h3>
                <p>Non è stato possibile caricare i dati delle competenze. Riprova più tardi.</p>
                <button class="btn btn-primary" onclick="window.SkillsModule.reload()">
                    <i class="fas fa-redo"></i>
                    Riprova
                </button>
            </div>
        `;
    }

    /* ================================ */
    /* SEARCH & SORTING                 */
    /* ================================ */
    function searchSkills(query) {
        if (!skillsData || !query.trim()) {
            renderSkills();
            return;
        }

        const searchTerm = query.toLowerCase();
        const filteredSkills = skillsData.skills.filter(skill => 
            skill.name.toLowerCase().includes(searchTerm) ||
            skill.description.toLowerCase().includes(searchTerm) ||
            skill.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
            skill.technologies.some(tech => tech.name.toLowerCase().includes(searchTerm))
        );

        const skillsHTML = filteredSkills.map(skill => createSkillCard(skill)).join('');
        skillsGrid.innerHTML = skillsHTML;
        animateSkillCards();

        window.PortfolioConfig.utils.log('debug', `Found ${filteredSkills.length} skills for query: ${query}`);
    }

    function sortSkills(sortBy = 'level') {
        if (!skillsData) return;

        const sortedSkills = [...skillsData.skills].sort((a, b) => {
            switch (sortBy) {
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'level':
                    return b.level - a.level;
                case 'experience':
                    return b.years_experience - a.years_experience;
                default:
                    return 0;
            }
        });

        const skillsHTML = sortedSkills.map(skill => createSkillCard(skill)).join('');
        skillsGrid.innerHTML = skillsHTML;
        animateSkillCards();
    }

    /* ================================ */
    /* API PUBBLICA                     */
    /* ================================ */
    window.SkillsModule = {
        init,
        reload: () => {
            skillsLoaded = false;
            loadSkillsData();
        },
        filter: updateFilter,
        search: searchSkills,
        sort: sortSkills,
        getData: () => skillsData,
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

})();