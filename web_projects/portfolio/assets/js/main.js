/*
===========================================
MAIN APPLICATION SCRIPT
===========================================
Coordinatore principale di tutti i moduli del portfolio
*/

// Hide loading screen when page is fully loaded
window.addEventListener('load', () => {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.classList.add('fade-out');
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
            }, 1000);
        }, 500); // Minimum loading time
    }
});

(function() {
    'use strict';

    // Stato globale dell'applicazione
    const AppState = {
        isLoaded: false,
        modules: [],
        performance: {
            startTime: performance.now(),
            loadTime: null,
            domReadyTime: null
        },
        errors: []
    };

    /* ================================ */
    /* INIZIALIZZAZIONE PRINCIPALE      */
    /* ================================ */
    function initializeApp() {
        AppState.performance.domReadyTime = performance.now();
        
        window.PortfolioConfig.utils.log('info', 'Initializing Portfolio Application');

        try {
            // Inizializza moduli in ordine di priorità
            initializeModules();

            // Setup global event listeners
            setupGlobalEventListeners();

            // Setup performance monitoring
            setupPerformanceMonitoring();

            // Setup error handling
            setupGlobalErrorHandling();

            // Setup accessibility features
            setupAccessibilityFeatures();

            // Finalize initialization
            finalizeInitialization();

        } catch (error) {
            handleInitializationError(error);
        }
    }

    /* ================================ */
    /* INIZIALIZZAZIONE MODULI          */
    /* ================================ */
    function initializeModules() {
        const modules = [
            // Moduli core (sempre necessari)
            {
                name: 'Theme',
                instance: window.ThemeModule,
                required: true,
                priority: 1
            },
            {
                name: 'Navigation',
                instance: window.NavigationModule,
                required: true,
                priority: 2
            },
            // Moduli di contenuto
            {
                name: 'Skills',
                instance: window.SkillsModule,
                required: false,
                priority: 3
            },
            {
                name: 'Projects',
                instance: window.ProjectsModule,
                required: false,
                priority: 4
            },
            {
                name: 'Contact',
                instance: window.ContactModule,
                required: false,
                priority: 5
            },
            {
                name: 'Animations',
                instance: window.AnimationsModule,
                required: false,
                priority: 6
            }
        ];

        // Ordina per priorità
        modules.sort((a, b) => a.priority - b.priority);

        // Inizializza ogni modulo
        modules.forEach(module => {
            try {
                if (module.instance && typeof module.instance.init === 'function') {
                    module.instance.init();
                    AppState.modules.push(module.name);
                    window.PortfolioConfig.utils.log('debug', `Module ${module.name} initialized`);
                } else if (module.required) {
                    throw new Error(`Required module ${module.name} not found or missing init method`);
                } else {
                    window.PortfolioConfig.utils.log('warn', `Optional module ${module.name} not available`);
                }
            } catch (error) {
                const errorMsg = `Failed to initialize module ${module.name}: ${error.message}`;
                AppState.errors.push(errorMsg);
                
                if (module.required) {
                    throw new Error(errorMsg);
                } else {
                    console.warn(errorMsg);
                }
            }
        });

        window.PortfolioConfig.utils.log('info', `Initialized ${AppState.modules.length} modules`);
    }

    /* ================================ */
    /* EVENT LISTENERS GLOBALI          */
    /* ================================ */
    function setupGlobalEventListeners() {
        // Window resize handler
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                handleWindowResize();
            }, 250);
        });

        // Window focus/blur handlers
        window.addEventListener('focus', handleWindowFocus);
        window.addEventListener('blur', handleWindowBlur);

        // Page visibility API
        if (typeof document.visibilityState !== 'undefined') {
            document.addEventListener('visibilitychange', handleVisibilityChange);
        }

        // Online/offline handlers
        window.addEventListener('online', handleOnlineStatus);
        window.addEventListener('offline', handleOfflineStatus);

        // Before unload (per cleanup)
        window.addEventListener('beforeunload', handleBeforeUnload);

        // Global keyboard shortcuts
        document.addEventListener('keydown', handleGlobalKeyboard);

        // Global click handler (per analytics futuri)
        document.addEventListener('click', handleGlobalClick);

        window.PortfolioConfig.utils.log('debug', 'Global event listeners setup completed');
    }

    /* ================================ */
    /* GESTIONE EVENTI                  */
    /* ================================ */
    function handleWindowResize() {
        const newWidth = window.innerWidth;
        const newHeight = window.innerHeight;
        
        // Notifica moduli del resize
        const event = new CustomEvent('portfolioResize', {
            detail: { width: newWidth, height: newHeight }
        });
        document.dispatchEvent(event);

        window.PortfolioConfig.utils.log('debug', `Window resized to ${newWidth}x${newHeight}`);
    }

    function handleWindowFocus() {
        document.body.classList.remove('window-blurred');
        window.PortfolioConfig.utils.log('debug', 'Window focused');
    }

    function handleWindowBlur() {
        document.body.classList.add('window-blurred');
        window.PortfolioConfig.utils.log('debug', 'Window blurred');
    }

    function handleVisibilityChange() {
        if (document.visibilityState === 'visible') {
            document.body.classList.remove('page-hidden');
            window.PortfolioConfig.utils.log('debug', 'Page visible');
        } else {
            document.body.classList.add('page-hidden');
            window.PortfolioConfig.utils.log('debug', 'Page hidden');
        }
    }

    function handleOnlineStatus() {
        document.body.classList.remove('offline');
        showConnectionStatus('online');
        window.PortfolioConfig.utils.log('info', 'Connection restored');
    }

    function handleOfflineStatus() {
        document.body.classList.add('offline');
        showConnectionStatus('offline');
        window.PortfolioConfig.utils.log('warn', 'Connection lost');
    }

    function handleBeforeUnload() {
        // Cleanup operations
        AppState.modules.forEach(moduleName => {
            const moduleInstance = window[`${moduleName}Module`];
            if (moduleInstance && typeof moduleInstance.cleanup === 'function') {
                try {
                    moduleInstance.cleanup();
                } catch (error) {
                    console.warn(`Error cleaning up module ${moduleName}:`, error);
                }
            }
        });
    }

    function handleGlobalKeyboard(e) {
        // Global keyboard shortcuts
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case '/':
                    e.preventDefault();
                    showKeyboardShortcuts();
                    break;
                case 'k':
                    e.preventDefault();
                    focusSearch();
                    break;
            }
        }

        // Escape key global handler
        if (e.key === 'Escape') {
            closeAllModals();
        }
    }

    function handleGlobalClick(e) {
        // Track clicks for future analytics
        const target = e.target;
        const tagName = target.tagName.toLowerCase();
        const className = target.className;
        
        // Log important interactions
        if (tagName === 'a' || tagName === 'button' || target.closest('.clickable')) {
            window.PortfolioConfig.utils.log('debug', 'User interaction', {
                element: tagName,
                className: className,
                text: target.textContent?.trim().substring(0, 50)
            });
        }
    }

    /* ================================ */
    /* PERFORMANCE MONITORING           */
    /* ================================ */
    function setupPerformanceMonitoring() {
        // Misura Core Web Vitals
        if ('web-vital' in window) {
            measureWebVitals();
        }

        // Monitor loading performance
        window.addEventListener('load', () => {
            AppState.performance.loadTime = performance.now();
            
            const loadDuration = AppState.performance.loadTime - AppState.performance.startTime;
            window.PortfolioConfig.utils.log('info', `Page loaded in ${loadDuration.toFixed(2)}ms`);
            
            // Report performance metrics
            if (window.PortfolioConfig.dev.showPerformanceMetrics) {
                showPerformanceMetrics();
            }
        });

        // Monitor long tasks
        if ('PerformanceObserver' in window) {
            try {
                const observer = new PerformanceObserver((list) => {
                    list.getEntries().forEach((entry) => {
                        if (entry.duration > 50) {
                            window.PortfolioConfig.utils.log('warn', `Long task detected: ${entry.duration.toFixed(2)}ms`);
                        }
                    });
                });
                observer.observe({ entryTypes: ['longtask'] });
            } catch (error) {
                // PerformanceObserver not supported or failed
                console.warn('Performance monitoring not available');
            }
        }
    }

    function measureWebVitals() {
        // Placeholder per future Web Vitals integration
        // In un'app reale, useresti una libreria come web-vitals
        window.PortfolioConfig.utils.log('debug', 'Web Vitals monitoring setup');
    }

    function showPerformanceMetrics() {
        const metrics = {
            'DOM Ready': `${(AppState.performance.domReadyTime - AppState.performance.startTime).toFixed(2)}ms`,
            'Page Load': `${(AppState.performance.loadTime - AppState.performance.startTime).toFixed(2)}ms`,
            'Modules': AppState.modules.length,
            'Errors': AppState.errors.length
        };

        console.table(metrics);
    }

    /* ================================ */
    /* ERROR HANDLING                   */
    /* ================================ */
    function setupGlobalErrorHandling() {
        // Global error handler
        window.addEventListener('error', (e) => {
            const error = {
                message: e.message,
                filename: e.filename,
                lineno: e.lineno,
                colno: e.colno,
                stack: e.error?.stack
            };
            
            AppState.errors.push(error);
            window.PortfolioConfig.utils.log('error', 'Global error caught', error);
            
            // In produzione, potresti inviare errori a un servizio di monitoring
            if (!window.PortfolioConfig.dev.debug) {
                // sendErrorToService(error);
            }
        });

        // Unhandled promise rejections
        window.addEventListener('unhandledrejection', (e) => {
            const error = {
                reason: e.reason,
                promise: e.promise
            };
            
            AppState.errors.push(error);
            window.PortfolioConfig.utils.log('error', 'Unhandled promise rejection', error);
            
            // Previeni il log di default nel browser
            e.preventDefault();
        });
    }

    function handleInitializationError(error) {
        console.error('Portfolio initialization failed:', error);
        
        // Mostra error message user-friendly
        showErrorMessage('Si è verificato un errore durante il caricamento del portfolio. Ricarica la pagina.');
        
        // Try graceful degradation
        document.body.classList.add('app-error');
        
        // Hide loading screen
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.style.display = 'none';
        }
    }

    /* ================================ */
    /* ACCESSIBILITY                    */
    /* ================================ */
    function setupAccessibilityFeatures() {
        // Skip link functionality
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) {
            skipLink.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector('#main');
                if (target) {
                    target.focus();
                    target.scrollIntoView();
                }
            });
        }

        // Keyboard navigation enhancement
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });

        // ARIA live region for announcements
        createAriaLiveRegion();

        window.PortfolioConfig.utils.log('debug', 'Accessibility features setup completed');
    }

    function createAriaLiveRegion() {
        const liveRegion = document.createElement('div');
        liveRegion.id = 'aria-live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.style.cssText = `
            position: absolute;
            left: -10000px;
            width: 1px;
            height: 1px;
            overflow: hidden;
        `;
        document.body.appendChild(liveRegion);
    }

    /* ================================ */
    /* UTILITY FUNCTIONS                */
    /* ================================ */
    function showConnectionStatus(status) {
        const message = status === 'online' ? 'Connessione ripristinata' : 'Connessione persa';
        const type = status === 'online' ? 'success' : 'warning';
        
        showToast(message, type);
    }

    function showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${getToastIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;
        
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--color-${type === 'success' ? 'success' : type === 'warning' ? 'warning' : 'info'});
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 10);
        
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, duration);
    }

    function getToastIcon(type) {
        const icons = {
            success: 'check-circle',
            warning: 'exclamation-triangle',
            error: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    function showErrorMessage(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'global-error';
        errorDiv.innerHTML = `
            <div class="error-content">
                <h2>Errore</h2>
                <p>${message}</p>
                <button onclick="window.location.reload()" class="btn btn-primary">
                    Ricarica Pagina
                </button>
            </div>
        `;
        
        errorDiv.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 99999;
        `;
        
        document.body.appendChild(errorDiv);
    }

    function showKeyboardShortcuts() {
        // Future implementation for keyboard shortcuts help
        window.PortfolioConfig.utils.log('info', 'Keyboard shortcuts: Ctrl+Shift+T (theme), Ctrl+/ (help)');
    }

    function focusSearch() {
        // Future implementation for search functionality
        window.PortfolioConfig.utils.log('info', 'Search functionality not implemented yet');
    }

    function closeAllModals() {
        // Chiudi tutti i modal aperti
        const modals = document.querySelectorAll('.project-modal.active');
        modals.forEach(modal => {
            modal.classList.remove('active');
        });
    }

    /* ================================ */
    /* FINALIZZAZIONE                   */
    /* ================================ */
    function finalizeInitialization() {
        AppState.isLoaded = true;
        
        // Nascondi loading screen
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
            }, window.PortfolioConfig.ui.loading.minDuration);
        }

        // Aggiungi classe loaded al body
        document.body.classList.add('app-loaded');
        
        // Dispatch evento di inizializzazione completata
        const event = new CustomEvent('portfolioLoaded', {
            detail: {
                modules: AppState.modules,
                loadTime: AppState.performance.loadTime - AppState.performance.startTime,
                errors: AppState.errors
            }
        });
        document.dispatchEvent(event);

        window.PortfolioConfig.utils.log('info', 'Portfolio initialization completed successfully');
        
        // Log finale stato applicazione
        if (window.PortfolioConfig.dev.debug) {
            console.log('Portfolio State:', AppState);
        }
    }

    /* ================================ */
    /* API PUBBLICA                     */
    /* ================================ */
    window.PortfolioApp = {
        getState: () => ({ ...AppState }),
        getModules: () => [...AppState.modules],
        getErrors: () => [...AppState.errors],
        showToast,
        isLoaded: () => AppState.isLoaded
    };

    /* ================================ */
    /* AUTO-INIZIALIZZAZIONE            */
    /* ================================ */
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeApp);
    } else {
        initializeApp();
    }

})();