// Theme Management Module

const ThemeManager = {
    // Initialize theme management
    init() {
        this.themeToggle = Utils.dom.get('#theme-toggle');
        this.currentTheme = this.getStoredTheme() || CONFIG.theme.default;
        
        this.setupEventListeners();
        this.applyTheme(this.currentTheme);
        this.updateToggleIcon();
        
        console.log('Theme Manager initialized');
    },
    
    // Setup event listeners
    setupEventListeners() {
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
        
        // Listen for system theme changes
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                if (!this.getStoredTheme()) {
                    this.applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    },
    
    // Toggle between light and dark theme
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    },
    
    // Set specific theme
    setTheme(theme) {
        this.currentTheme = theme;
        this.applyTheme(theme);
        this.storeTheme(theme);
        this.updateToggleIcon();
        
        // Trigger custom event
        Utils.events.trigger(document, 'themeChanged', { theme });
    },
    
    // Apply theme to document
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        
        // Add transition class for smooth theme change
        Utils.dom.addClass(document.body, 'theme-transition');
        
        // Remove transition class after animation
        setTimeout(() => {
            Utils.dom.removeClass(document.body, 'theme-transition');
        }, CONFIG.theme.transition);
        
        // Update meta theme-color for mobile browsers
        this.updateMetaThemeColor(theme);
    },
    
    // Update toggle button icon
    updateToggleIcon() {
        if (!this.themeToggle) return;
        
        const icon = this.themeToggle.querySelector('i');
        if (icon) {
            if (this.currentTheme === 'dark') {
                icon.className = 'fas fa-sun';
                this.themeToggle.setAttribute('aria-label', 'Switch to light theme');
            } else {
                icon.className = 'fas fa-moon';
                this.themeToggle.setAttribute('aria-label', 'Switch to dark theme');
            }
        }
    },
    
    // Update meta theme-color
    updateMetaThemeColor(theme) {
        let metaThemeColor = Utils.dom.get('meta[name="theme-color"]');
        
        if (!metaThemeColor) {
            metaThemeColor = Utils.dom.create('meta');
            metaThemeColor.setAttribute('name', 'theme-color');
            document.head.appendChild(metaThemeColor);
        }
        
        const color = theme === 'dark' ? '#1e293b' : '#ffffff';
        metaThemeColor.setAttribute('content', color);
    },
    
    // Store theme preference
    storeTheme(theme) {
        Utils.storage.set(CONFIG.theme.storageKey, theme);
    },
    
    // Get stored theme preference
    getStoredTheme() {
        return Utils.storage.get(CONFIG.theme.storageKey);
    },
    
    // Get system theme preference
    getSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    },
    
    // Get current theme
    getCurrentTheme() {
        return this.currentTheme;
    }
};

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
});

// Export for other modules
window.ThemeManager = ThemeManager;