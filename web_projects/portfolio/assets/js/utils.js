/*
===========================================
UTILS MODULE - Portfolio
===========================================
Funzioni utility riutilizzabili per tutto il portfolio
*/

// ================================
// DOM UTILITIES
// ================================

/**
 * Selettore DOM migliorato con error handling
 */
const $ = (selector, context = document) => {
    try {
        return context.querySelector(selector);
    } catch (error) {
        console.error(`❌ Invalid selector: ${selector}`, error);
        return null;
    }
};

/**
 * Selettore multiplo DOM
 */
const $$ = (selector, context = document) => {
    try {
        return Array.from(context.querySelectorAll(selector));
    } catch (error) {
        console.error(`❌ Invalid selector: ${selector}`, error);
        return [];
    }
};

/**
 * Crea un elemento DOM con attributi e contenuto
 */
const createElement = (tag, attributes = {}, content = '') => {
    const element = document.createElement(tag);
    
    Object.entries(attributes).forEach(([key, value]) => {
        if (key === 'className') {
            element.className = value;
        } else if (key === 'innerHTML') {
            element.innerHTML = value;
        } else if (key === 'textContent') {
            element.textContent = value;
        } else if (key.startsWith('data-')) {
            element.setAttribute(key, value);
        } else {
            element[key] = value;
        }
    });
    
    if (content) {
        element.innerHTML = content;
    }
    
    return element;
};

/**
 * Verifica se un elemento è visibile nel viewport
 */
const isElementInViewport = (element, threshold = 0) => {
    if (!element) return false;
    
    const rect = element.getBoundingClientRect();
    const windowHeight = window.innerHeight || document.documentElement.clientHeight;
    const windowWidth = window.innerWidth || document.documentElement.clientWidth;
    
    const verticalVisible = rect.top + (rect.height * threshold) < windowHeight && 
                           rect.bottom - (rect.height * threshold) > 0;
    const horizontalVisible = rect.left < windowWidth && rect.right > 0;
    
    return verticalVisible && horizontalVisible;
};

/**
 * Ottiene la posizione di un elemento rispetto al documento
 */
const getElementPosition = (element) => {
    if (!element) return { top: 0, left: 0 };
    
    const rect = element.getBoundingClientRect();
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
    
    return {
        top: rect.top + scrollTop,
        left: rect.left + scrollLeft,
        width: rect.width,
        height: rect.height
    };
};

// ================================
// ANIMATION UTILITIES
// ================================

/**
 * Easing functions per animazioni
 */
const Easing = {
    linear: t => t,
    easeInQuad: t => t * t,
    easeOutQuad: t => t * (2 - t),
    easeInOutQuad: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
    easeInCubic: t => t * t * t,
    easeOutCubic: t => (--t) * t * t + 1,
    easeInOutCubic: t => t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
    easeInQuart: t => t * t * t * t,
    easeOutQuart: t => 1 - (--t) * t * t * t,
    easeInOutQuart: t => t < 0.5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t,
    easeInBack: t => 2.7 * t * t * t - 1.7 * t * t,
    easeOutBack: t => 1 + (--t) * t * (2.7 * t + 1.7),
    easeInOutBack: t => t < 0.5 
        ? (t * t * (7 * t - 2.5) * 2)
        : (1 + (--t) * t * 2 * (7 * t + 2.5))
};

/**
 * Animazione personalizzata con requestAnimationFrame
 */
const animate = (options) => {
    const {
        duration = 1000,
        easing = Easing.easeOutQuad,
        from = 0,
        to = 1,
        onUpdate = () => {},
        onComplete = () => {}
    } = options;
    
    const startTime = performance.now();
    const difference = to - from;
    
    const step = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = easing(progress);
        const currentValue = from + (difference * easedProgress);
        
        onUpdate(currentValue, progress);
        
        if (progress < 1) {
            requestAnimationFrame(step);
        } else {
            onComplete();
        }
    };
    
    requestAnimationFrame(step);
};

/**
 * Fade in di un elemento
 */
const fadeIn = (element, duration = 300, callback = () => {}) => {
    if (!element) return;
    
    element.style.opacity = '0';
    element.style.display = 'block';
    
    animate({
        duration,
        from: 0,
        to: 1,
        onUpdate: (value) => {
            element.style.opacity = value;
        },
        onComplete: callback
    });
};

/**
 * Fade out di un elemento
 */
const fadeOut = (element, duration = 300, callback = () => {}) => {
    if (!element) return;
    
    animate({
        duration,
        from: 1,
        to: 0,
        onUpdate: (value) => {
            element.style.opacity = value;
        },
        onComplete: () => {
            element.style.display = 'none';
            callback();
        }
    });
};

/**
 * Slide up di un elemento
 */
const slideUp = (element, duration = 300, callback = () => {}) => {
    if (!element) return;
    
    const height = element.offsetHeight;
    element.style.overflow = 'hidden';
    
    animate({
        duration,
        from: height,
        to: 0,
        onUpdate: (value) => {
            element.style.height = `${value}px`;
        },
        onComplete: () => {
            element.style.display = 'none';
            element.style.height = '';
            element.style.overflow = '';
            callback();
        }
    });
};

/**
 * Slide down di un elemento
 */
const slideDown = (element, duration = 300, callback = () => {}) => {
    if (!element) return;
    
    element.style.display = 'block';
    element.style.overflow = 'hidden';
    element.style.height = '0px';
    
    const height = element.scrollHeight;
    
    animate({
        duration,
        from: 0,
        to: height,
        onUpdate: (value) => {
            element.style.height = `${value}px`;
        },
        onComplete: () => {
            element.style.height = '';
            element.style.overflow = '';
            callback();
        }
    });
};

// ================================
// UTILITY FUNCTIONS
// ================================

/**
 * Debounce function per limitare chiamate frequenti
 */
const debounce = (func, wait, immediate = false) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
};

/**
 * Throttle function per limitare chiamate frequenti
 */
const throttle = (func, limit) => {
    let inThrottle;
    return function executedFunction(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};

/**
 * Genera un ID univoco
 */
const generateUniqueId = (prefix = 'id') => {
    return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * Formatta un numero con separatori delle migliaia
 */
const formatNumber = (number, locale = 'it-IT') => {
    return new Intl.NumberFormat(locale).format(number);
};

/**
 * Formatta una data
 */
const formatDate = (date, locale = 'it-IT', options = {}) => {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    return new Intl.DateTimeFormat(locale, { ...defaultOptions, ...options }).format(new Date(date));
};

/**
 * Capitalizza la prima lettera di una stringa
 */
const capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

/**
 * Rimuove caratteri speciali da una stringa per creare slug
 */
const slugify = (str) => {
    return str
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')
        .replace(/[\s_-]+/g, '-')
        .replace(/^-+|-+$/g, '');
};

/**
 * Verifica se una stringa è un email valido
 */
const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

/**
 * Verifica se una stringa è un URL valido
 */
const isValidUrl = (url) => {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
};

// ================================
// STORAGE UTILITIES
// ================================

/**
 * Gestione sicura del localStorage
 */
const storage = {
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.warn(`❌ Error reading from localStorage: ${key}`, error);
            return defaultValue;
        }
    },
    
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.warn(`❌ Error writing to localStorage: ${key}`, error);
            return false;
        }
    },
    
    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.warn(`❌ Error removing from localStorage: ${key}`, error);
            return false;
        }
    },
    
    clear() {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.warn('❌ Error clearing localStorage', error);
            return false;
        }
    }
};

// ================================
// DEVICE DETECTION
// ================================

/**
 * Rileva il tipo di dispositivo
 */
const device = {
    isMobile() {
        return window.innerWidth <= 768;
    },
    
    isTablet() {
        return window.innerWidth > 768 && window.innerWidth <= 1024;
    },
    
    isDesktop() {
        return window.innerWidth > 1024;
    },
    
    isTouchDevice() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    },
    
    isIOS() {
        return /iPad|iPhone|iPod/.test(navigator.userAgent);
    },
    
    isAndroid() {
        return /Android/.test(navigator.userAgent);
    },
    
    supportsWebP() {
        const canvas = document.createElement('canvas');
        return canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    }
};

// ================================
// FETCH UTILITIES
// ================================

/**
 * Fetch wrapper con timeout e error handling
 */
const fetchWithTimeout = async (url, options = {}, timeout = 10000) => {
    const { signal, ...otherOptions } = options;
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, {
            ...otherOptions,
            signal: signal || controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        throw error;
    }
};

/**
 * Carica JSON con gestione errori
 */
const loadJSON = async (url, timeout = 10000) => {
    try {
        const response = await fetchWithTimeout(url, {}, timeout);
        return await response.json();
    } catch (error) {
        console.error(`❌ Error loading JSON from ${url}:`, error);
        throw error;
    }
};

// ================================
// MATH UTILITIES
// ================================

/**
 * Clamp di un valore tra min e max
 */
const clamp = (value, min, max) => {
    return Math.min(Math.max(value, min), max);
};

/**
 * Mappa un valore da un range a un altro
 */
const mapRange = (value, inMin, inMax, outMin, outMax) => {
    return (value - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
};

/**
 * Interpolazione lineare
 */
const lerp = (start, end, factor) => {
    return start + (end - start) * factor;
};

/**
 * Genera un numero casuale tra min e max
 */
const random = (min, max) => {
    return Math.random() * (max - min) + min;
};

/**
 * Arrotonda un numero a un numero specifico di decimali
 */
const roundTo = (number, decimals = 2) => {
    return Math.round(number * Math.pow(10, decimals)) / Math.pow(10, decimals);
};

// ================================
// COLOR UTILITIES
// ================================

/**
 * Converte HEX a RGB
 */
const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
};

/**
 * Converte RGB a HEX
 */
const rgbToHex = (r, g, b) => {
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
};

// ================================
// EVENT UTILITIES
// ================================

/**
 * Event emitter semplice
 */
class EventEmitter {
    constructor() {
        this.events = {};
    }
    
    on(event, callback) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(callback);
    }
    
    off(event, callback) {
        if (!this.events[event]) return;
        
        this.events[event] = this.events[event].filter(cb => cb !== callback);
    }
    
    emit(event, ...args) {
        if (!this.events[event]) return;
        
        this.events[event].forEach(callback => callback(...args));
    }
}

// ================================
// PERFORMANCE UTILITIES
// ================================

/**
 * Misura le performance di una funzione
 */
const measurePerformance = (name, fn) => {
    return (...args) => {
        const start = performance.now();
        const result = fn(...args);
        const end = performance.now();
        console.log(`⏱️ ${name} took ${end - start} milliseconds`);
        return result;
    };
};

/**
 * Precarica immagini
 */
const preloadImages = (urls) => {
    return Promise.all(
        urls.map(url => {
            return new Promise((resolve, reject) => {
                const img = new Image();
                img.onload = () => resolve(img);
                img.onerror = () => reject(new Error(`Failed to load image: ${url}`));
                img.src = url;
            });
        })
    );
};

// ================================
// EXPORTS
// ================================

// Esporta tutte le utility
const Utils = {
    // DOM
    $, $$, createElement, isElementInViewport, getElementPosition,
    
    // Animations
    Easing, animate, fadeIn, fadeOut, slideUp, slideDown,
    
    // General utilities
    debounce, throttle, generateUniqueId, formatNumber, formatDate,
    capitalize, slugify, isValidEmail, isValidUrl,
    
    // Storage
    storage,
    
    // Device
    device,
    
    // Fetch
    fetchWithTimeout, loadJSON,
    
    // Math
    clamp, mapRange, lerp, random, roundTo,
    
    // Color
    hexToRgb, rgbToHex,
    
    // Events
    EventEmitter,
    
    // Performance
    measurePerformance, preloadImages
};

// Export per moduli
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Utils;
}

// Rendi disponibile globalmente
if (typeof window !== 'undefined') {
    window.Utils = Utils;
    
    // Shortcut globali per le funzioni più usate
    window.$ = $;
    window.$$ = $$;
    
    console.log('🛠️ Utils Module: Loaded');
}