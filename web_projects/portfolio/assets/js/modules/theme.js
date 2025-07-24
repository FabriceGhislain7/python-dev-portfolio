/*
===========================================
THEME MODULE
===========================================
Gestisce il sistema di tema scuro/chiaro
*/

(function() {
    'use strict';

    // Variabili del modulo
    let themeToggleBtn = null;
    let currentTheme = 'light';
    let isTransitioning = false;

    /* ================================ */
    /* INIZIALIZZAZIONE                 */
    /* ================================ */
    function init() {
        // Ottieni riferimenti elementi DOM
        themeToggleBtn = document.getElementById('theme-toggle');

        if (!themeToggleBtn) {
            console.warn('Theme toggle button not found');
            return;
        }

        // Carica tema salvato o rileva preferenza sistema
        loadTheme();

        // Setup event listeners
        setupThemeToggle();
        setupSystemThemeDetection();

        window.PortfolioConfig.utils.log('debug', 'Theme module initialized');
    }

    /* ================================ */
    /* CARICAMENTO TEMA                 */
    /* ================================ */
    function loadTheme() {
        // Ottieni tema salvato
        const savedTheme = window.PortfolioConfig.utils.storage.get(
            window.PortfolioConfig.ui.theme.storageKey
        );

        // Se non c'è tema salvato, rileva preferenza sistema
        if (!savedTheme) {
            currentTheme = detectSystemTheme();
        } else {
            currentTheme = savedTheme;
        }

        // Applica tema
        applyTheme(currentTheme, false);

        window.PortfolioConfig.utils.log('debug', `Theme loaded: ${currentTheme}`);
    }

    function detectSystemTheme() {
        // Verifica se il browser supporta prefers-color-scheme
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    /* ================================ */
    /* APPLICAZIONE TEMA                */
    /* ================================ */
    function applyTheme(theme, withAnimation = true) {
        if (isTransitioning) return;
        
        isTransitioning = true;
        currentTheme = theme;

        // Aggiungi classe di transizione se richiesta
        if (withAnimation && window.PortfolioConfig.ui.theme.transitions) {
            document.documentElement.classList.add('theme-transitioning');
        }

        // Applica attributo data-theme
        document.documentElement.setAttribute('data-theme', theme);

        // Aggiorna icona del bottone
        updateThemeToggleIcon(theme);

        // Salva tema nel localStorage
        window.PortfolioConfig.utils.storage.set(
            window.PortfolioConfig.ui.theme.storageKey,
            theme
        );

        // Rimuovi classe di transizione dopo animazione
        if (withAnimation) {
            setTimeout(() => {
                document.documentElement.classList.remove('theme-transitioning');
                isTransitioning = false;
            }, 300);
        } else {
            isTransitioning = false;
        }

        // Dispatch evento custom per altri moduli
        dispatchThemeChangeEvent(theme);

        window.PortfolioConfig.utils.log('debug', `Theme applied: ${theme}`);
    }

    function updateThemeToggleIcon(theme) {
        if (!themeToggleBtn) return;

        const icon = themeToggleBtn.querySelector('i');
        if (!icon) return;

        // Rimuovi classi esistenti
        icon.classList.remove('fa-moon', 'fa-sun');

        // Aggiungi icona appropriata
        if (theme === 'dark') {
            icon.classList.add('fa-sun');
            themeToggleBtn.setAttribute('aria-label', 'Passa al tema chiaro');
            themeToggleBtn.title = 'Passa al tema chiaro';
        } else {
            icon.classList.add('fa-moon');
            themeToggleBtn.setAttribute('aria-label', 'Passa al tema scuro');
            themeToggleBtn.title = 'Passa al tema scuro';
        }
    }

    /* ================================ */
    /* TOGGLE TEMA                      */
    /* ================================ */
    function setupThemeToggle() {
        if (!themeToggleBtn) return;

        themeToggleBtn.addEventListener('click', toggleTheme);

        // Supporto keyboard
        themeToggleBtn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleTheme();
            }
        });
    }

    function toggleTheme() {
        if (isTransitioning) return;

        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        // Aggiungi effetto visual al bottone
        addToggleEffect();
        
        // Applica nuovo tema
        setTimeout(() => {
            applyTheme(newTheme, true);
        }, 150);

        window.PortfolioConfig.utils.log('debug', `Theme toggled from ${currentTheme} to ${newTheme}`);
    }

    function addToggleEffect() {
        if (!themeToggleBtn) return;

        // Aggiungi classe per animazione
        themeToggleBtn.classList.add('theme-toggle-active');

        // Rimuovi dopo animazione
        setTimeout(() => {
            themeToggleBtn.classList.remove('theme-toggle-active');
        }, 300);
    }

    /* ================================ */
    /* RILEVAMENTO SISTEMA              */
    /* ================================ */
    function setupSystemThemeDetection() {
        // Ascolta cambiamenti preferenze sistema
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            mediaQuery.addEventListener('change', (e) => {
                // Solo se non c'è tema salvato esplicitamente
                const savedTheme = window.PortfolioConfig.utils.storage.get(
                    window.PortfolioConfig.ui.theme.storageKey
                );
                
                if (!savedTheme) {
                    const systemTheme = e.matches ? 'dark' : 'light';
                    applyTheme(systemTheme, true);
                    
                    window.PortfolioConfig.utils.log('debug', `System theme changed to: ${systemTheme}`);
                }
            });
        }
    }

    /* ================================ */
    /* EVENTI CUSTOM                    */
    /* ================================ */
    function dispatchThemeChangeEvent(theme) {
        const event = new CustomEvent('themeChanged', {
            detail: {
                theme: theme,
                previousTheme: currentTheme === 'light' ? 'dark' : 'light'
            }
        });
        
        document.dispatchEvent(event);
    }

    /* ================================ */
    /* ANIMAZIONI SPECIALI              */
    /* ================================ */
    function createThemeTransitionEffect() {
        // Crea overlay per transizione smooth
        const overlay = document.createElement('div');
        overlay.className = 'theme-transition-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: ${currentTheme === 'light' ? '#000' : '#fff'};
            z-index: 99999;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        `;
        
        document.body.appendChild(overlay);
        
        // Anima overlay
        requestAnimationFrame(() => {
            overlay.style.opacity = '0.1';
            
            setTimeout(() => {
                overlay.style.opacity = '0';
                
                setTimeout(() => {
                    document.body.removeChild(overlay);
                }, 300);
            }, 150);
        });
    }

    /* ================================ */
    /* UTILITIES                        */
    /* ================================ */
    function getThemeColors(theme) {
        const colors = {
            light: {
                primary: '#ffffff',
                secondary: '#f9fafb',
                text: '#111827',
                border: '#e5e7eb'
            },
            dark: {
                primary: '#111827',
                secondary: '#1f2937',
                text: '#f9fafb',
                border: '#374151'
            }
        };
        
        return colors[theme] || colors.light;
    }

    function updateMetaThemeColor(theme) {
        // Aggiorna meta theme-color per mobile
        let metaThemeColor = document.querySelector('meta[name="theme-color"]');
        
        if (!metaThemeColor) {
            metaThemeColor = document.createElement('meta');
            metaThemeColor.name = 'theme-color';
            document.head.appendChild(metaThemeColor);
        }
        
        const colors = getThemeColors(theme);
        metaThemeColor.content = colors.primary;
    }

    /* ================================ */
    /* PERSISTENZA AVANZATA             */
    /* ================================ */
    function syncThemeAcrossTabs() {
        // Ascolta cambiamenti localStorage da altre tab
        window.addEventListener('storage', (e) => {
            if (e.key === window.PortfolioConfig.ui.theme.storageKey && e.newValue) {
                const newTheme = e.newValue.replace(/"/g, ''); // Rimuovi quotes JSON
                if (newTheme !== currentTheme) {
                    applyTheme(newTheme, true);
                    window.PortfolioConfig.utils.log('debug', `Theme synced from other tab: ${newTheme}`);
                }
            }
        });
    }

    /* ================================ */
    /* ACCESSIBILITY                    */
    /* ================================ */
    function setupAccessibility() {
        // Rispetta prefers-reduced-motion
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        if (prefersReducedMotion) {
            window.PortfolioConfig.ui.theme.transitions = false;
            document.documentElement.style.setProperty('--transition-normal', '0ms');
            document.documentElement.style.setProperty('--transition-fast', '0ms');
            document.documentElement.style.setProperty('--transition-slow', '0ms');
        }

        // Shortcut keyboard per toggle tema
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Shift + T per toggle tema
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
                e.preventDefault();
                toggleTheme();
            }
        });
    }

    /* ================================ */
    /* API PUBBLICA                     */
    /* ================================ */
    window.ThemeModule = {
        init,
        toggle: toggleTheme,
        setTheme: (theme) => applyTheme(theme, true),
        getCurrentTheme: () => currentTheme,
        getThemeColors: () => getThemeColors(currentTheme),
        resetToSystem: () => {
            window.PortfolioConfig.utils.storage.remove(window.PortfolioConfig.ui.theme.storageKey);
            const systemTheme = detectSystemTheme();
            applyTheme(systemTheme, true);
        }
    };

    /* ================================ */
    /* AUTO-INIZIALIZZAZIONE            */
    /* ================================ */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            init();
            setupAccessibility();
            syncThemeAcrossTabs();
            updateMetaThemeColor(currentTheme);
        });
    } else {
        init();
        setupAccessibility();
        syncThemeAcrossTabs();
        updateMetaThemeColor(currentTheme);
    }

})();