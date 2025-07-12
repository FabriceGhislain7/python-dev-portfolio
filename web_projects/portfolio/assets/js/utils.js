// Utility Functions

const Utils = {
    // DOM manipulation utilities
    dom: {
        // Get element by selector
        get: (selector) => document.querySelector(selector),
        
        // Get all elements by selector
        getAll: (selector) => document.querySelectorAll(selector),
        
        // Create element
        create: (tag, className = '', content = '') => {
            const element = document.createElement(tag);
            if (className) element.className = className;
            if (content) element.textContent = content;
            return element;
        },
        
        // Add class to element
        addClass: (element, className) => {
            if (element) element.classList.add(className);
        },
        
        // Remove class from element
        removeClass: (element, className) => {
            if (element) element.classList.remove(className);
        },
        
        // Toggle class on element
        toggleClass: (element, className) => {
            if (element) element.classList.toggle(className);
        },
        
        // Check if element has class
        hasClass: (element, className) => {
            return element ? element.classList.contains(className) : false;
        },
        
        // Set multiple attributes
        setAttributes: (element, attributes) => {
            if (element) {
                Object.keys(attributes).forEach(key => {
                    element.setAttribute(key, attributes[key]);
                });
            }
        },
        
        // Get element position
        getPosition: (element) => {
            if (!element) return { top: 0, left: 0 };
            const rect = element.getBoundingClientRect();
            return {
                top: rect.top + window.pageYOffset,
                left: rect.left + window.pageXOffset,
                bottom: rect.bottom + window.pageYOffset,
                right: rect.right + window.pageXOffset
            };
        },
        
        // Check if element is in viewport
        isInViewport: (element, threshold = 0.1) => {
            if (!element) return false;
            const rect = element.getBoundingClientRect();
            const windowHeight = window.innerHeight || document.documentElement.clientHeight;
            const windowWidth = window.innerWidth || document.documentElement.clientWidth;
            
            const vertInView = (rect.top <= windowHeight * (1 - threshold)) && 
                              ((rect.top + rect.height) >= windowHeight * threshold);
            const horInView = (rect.left <= windowWidth * (1 - threshold)) && 
                             ((rect.left + rect.width) >= windowWidth * threshold);
            
            return vertInView && horInView;
        }
    },
    
    // Animation utilities
    animation: {
        // Smooth scroll to element
        scrollTo: (target, duration = 1000, offset = 0) => {
            const targetElement = typeof target === 'string' ? Utils.dom.get(target) : target;
            if (!targetElement) return;
            
            const targetPosition = Utils.dom.getPosition(targetElement).top - offset;
            const startPosition = window.pageYOffset;
            const distance = targetPosition - startPosition;
            let startTime = null;
            
            const easeInOutCubic = (t) => {
                return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
            };
            
            const animation = (currentTime) => {
                if (startTime === null) startTime = currentTime;
                const timeElapsed = currentTime - startTime;
                const progress = Math.min(timeElapsed / duration, 1);
                
                window.scrollTo(0, startPosition + distance * easeInOutCubic(progress));
                
                if (progress < 1) {
                    requestAnimationFrame(animation);
                }
            };
            
            requestAnimationFrame(animation);
        },
        
        // Animate number counting
        countUp: (element, target, duration = 2000, suffix = '') => {
            if (!element) return;
            
            const start = 0;
            const startTime = performance.now();
            
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                const current = Math.floor(start + (target - start) * progress);
                element.textContent = current + suffix;
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                }
            };
            
            requestAnimationFrame(animate);
        },
        
        // Stagger animation for multiple elements
        stagger: (elements, animationClass, delay = 100) => {
            elements.forEach((element, index) => {
                setTimeout(() => {
                    Utils.dom.addClass(element, animationClass);
                }, index * delay);
            });
        }
    },
    
    // Event utilities
    events: {
        // Debounce function
        debounce: (func, wait) => {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        // Throttle function
        throttle: (func, limit) => {
            let inThrottle;
            return function() {
                const args = arguments;
                const context = this;
                if (!inThrottle) {
                    func.apply(context, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },
        
        // Add event listener with automatic cleanup
        on: (element, event, handler, options = {}) => {
            if (element) {
                element.addEventListener(event, handler, options);
                return () => element.removeEventListener(event, handler, options);
            }
        },
        
        // Trigger custom event
        trigger: (element, eventName, detail = {}) => {
            if (element) {
                const event = new CustomEvent(eventName, { detail });
                element.dispatchEvent(event);
            }
        }
    },
    
    // Storage utilities
    storage: {
        // Set localStorage item
        set: (key, value) => {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.warn('LocalStorage not available:', e);
                return false;
            }
        },
        
        // Get localStorage item
        get: (key, defaultValue = null) => {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                console.warn('LocalStorage not available:', e);
                return defaultValue;
            }
        },
        
        // Remove localStorage item
        remove: (key) => {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.warn('LocalStorage not available:', e);
                return false;
            }
        }
    },
    
    // API utilities
    api: {
        // Fetch JSON data
        get: async (url) => {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                throw error;
            }
        },
        
        // Post data
        post: async (url, data) => {
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                throw error;
            }
        }
    },
    
    // Form utilities
    form: {
        // Get form data as object
        getData: (form) => {
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            return data;
        },
        
        // Validate email
        isValidEmail: (email) => {
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return regex.test(email);
        },
        
        // Reset form
        reset: (form) => {
            if (form) {
                form.reset();
                // Remove any error classes
                const inputs = form.querySelectorAll('.form-input');
                inputs.forEach(input => {
                    Utils.dom.removeClass(input, 'error');
                    Utils.dom.removeClass(input, 'success');
                });
            }
        }
    },
    
    // Device detection
    device: {
        // Check if mobile
        isMobile: () => {
            return window.innerWidth <= CONFIG.navigation.mobileBreakpoint;
        },
        
        // Check if tablet
        isTablet: () => {
            return window.innerWidth > CONFIG.navigation.mobileBreakpoint && 
                   window.innerWidth <= CONFIG.breakpoints.lg;
        },
        
        // Check if desktop
        isDesktop: () => {
            return window.innerWidth > CONFIG.breakpoints.lg;
        },
        
        // Check if touch device
        isTouchDevice: () => {
            return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
        }
    },
    
    // Performance utilities
    performance: {
        // Create intersection observer
        createObserver: (callback, options = {}) => {
            const defaultOptions = {
                threshold: CONFIG.performance.intersectionThreshold,
                rootMargin: '0px'
            };
            
            const observerOptions = { ...defaultOptions, ...options };
            
            return new IntersectionObserver(callback, observerOptions);
        },
        
        // Lazy load images
        lazyLoadImage: (img) => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                Utils.dom.addClass(img, 'loaded');
            }
        }
    },
    
    // Math utilities
    math: {
        // Clamp number between min and max
        clamp: (num, min, max) => Math.min(Math.max(num, min), max),
        
        // Linear interpolation
        lerp: (start, end, factor) => start + (end - start) * factor,
        
        // Map value from one range to another
        map: (value, inMin, inMax, outMin, outMax) => {
            return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
        },
        
        // Random number between min and max
        random: (min, max) => Math.random() * (max - min) + min
    }
};

// Initialize utilities on DOM load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Portfolio Utils loaded successfully');
});