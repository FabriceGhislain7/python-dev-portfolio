// Contact Form Management Module

const ContactManager = {
    // Initialize contact form management
    init() {
        this.contactForm = Utils.dom.get('#contact-form');
        this.formFields = {};
        this.validationRules = {};
        this.isSubmitting = false;
        
        if (!this.contactForm) {
            console.warn('Contact form not found');
            return;
        }
        
        this.setupFormFields();
        this.setupValidation();
        this.setupEventListeners();
        this.setupAutoSave();
        
        console.log('Contact Manager initialized');
    },
    
    // Setup form fields references
    setupFormFields() {
        this.formFields = {
            name: Utils.dom.get('#name'),
            email: Utils.dom.get('#email'),
            subject: Utils.dom.get('#subject'),
            message: Utils.dom.get('#message')
        };
        
        this.validationRules = {
            name: {
                required: true,
                minLength: 2,
                maxLength: 50,
                pattern: /^[a-zA-ZÀ-ÿ\s'-]+$/,
                message: 'Il nome deve contenere solo lettere e essere di 2-50 caratteri'
            },
            email: {
                required: true,
                pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Inserisci un indirizzo email valido'
            },
            subject: {
                required: true,
                minLength: 5,
                maxLength: 100,
                message: 'L\'oggetto deve essere di 5-100 caratteri'
            },
            message: {
                required: true,
                minLength: 10,
                maxLength: 1000,
                message: 'Il messaggio deve essere di 10-1000 caratteri'
            }
        };
    },
    
    // Setup event listeners
    setupEventListeners() {
        // Form submission
        this.contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });
        
        // Real-time validation
        Object.keys(this.formFields).forEach(fieldName => {
            const field = this.formFields[fieldName];
            if (field) {
                // Validate on blur
                field.addEventListener('blur', () => {
                    this.validateField(fieldName);
                });
                
                // Clear errors on input
                field.addEventListener('input', () => {
                    this.clearFieldError(fieldName);
                    this.updateCharacterCount(fieldName);
                });
                
                // Handle floating labels
                field.addEventListener('focus', () => {
                    this.handleFloatingLabel(field, true);
                });
                
                field.addEventListener('blur', () => {
                    this.handleFloatingLabel(field, false);
                });
            }
        });
        
        // Keyboard shortcuts
        this.contactForm.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                this.handleSubmit();
            }
        });
        
        // Prevent form submission on Enter in text inputs
        Object.values(this.formFields).forEach(field => {
            if (field && field.type !== 'textarea') {
                field.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        this.focusNextField(field);
                    }
                });
            }
        });
    },
    
    // Handle form submission
    async handleSubmit() {
        if (this.isSubmitting) return;
        
        // Validate all fields
        const isValid = this.validateForm();
        if (!isValid) {
            this.showNotification('Correggi gli errori nel form prima di inviare', 'error');
            return;
        }
        
        this.isSubmitting = true;
        const submitButton = this.contactForm.querySelector('button[type="submit"]');
        const originalButtonContent = submitButton.innerHTML;
        
        try {
            // Show loading state
            this.showLoadingState(submitButton);
            
            // Get form data
            const formData = this.getFormData();
            
            // Send form data
            await this.sendFormData(formData);
            
            // Success handling
            this.handleSuccess();
            
        } catch (error) {
            console.error('Form submission error:', error);
            this.handleError(error);
        } finally {
            // Reset button state
            this.resetLoadingState(submitButton, originalButtonContent);
            this.isSubmitting = false;
        }
    },
    
    // Validate entire form
    validateForm() {
        let isValid = true;
        
        Object.keys(this.formFields).forEach(fieldName => {
            if (!this.validateField(fieldName)) {
                isValid = false;
            }
        });
        
        return isValid;
    },
    
    // Validate individual field
    validateField(fieldName) {
        const field = this.formFields[fieldName];
        const rules = this.validationRules[fieldName];
        
        if (!field || !rules) return true;
        
        const value = field.value.trim();
        
        // Clear previous errors
        this.clearFieldError(fieldName);
        
        // Required validation
        if (rules.required && !value) {
            this.showFieldError(fieldName, `${this.getFieldLabel(fieldName)} è obbligatorio`);
            return false;
        }
        
        // Skip other validations if field is empty and not required
        if (!value && !rules.required) return true;
        
        // Length validation
        if (rules.minLength && value.length < rules.minLength) {
            this.showFieldError(fieldName, `Minimo ${rules.minLength} caratteri`);
            return false;
        }
        
        if (rules.maxLength && value.length > rules.maxLength) {
            this.showFieldError(fieldName, `Massimo ${rules.maxLength} caratteri`);
            return false;
        }
        
        // Pattern validation
        if (rules.pattern && !rules.pattern.test(value)) {
            this.showFieldError(fieldName, rules.message);
            return false;
        }
        
        // Field-specific validations
        if (fieldName === 'email' && value) {
            if (!this.isValidEmail(value)) {
                this.showFieldError(fieldName, 'Formato email non valido');
                return false;
            }
        }
        
        // Show success state
        this.showFieldSuccess(fieldName);
        return true;
    },
    
    // Validate email format
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },
    
    // Show field error
    showFieldError(fieldName, message) {
        const field = this.formFields[fieldName];
        if (!field) return;
        
        // Add error class to field
        Utils.dom.addClass(field, 'error');
        Utils.dom.removeClass(field, 'success');
        
        // Remove existing error message
        this.clearFieldError(fieldName, false);
        
        // Create error message
        const errorElement = Utils.dom.create('div', 'error-message', message);
        field.parentNode.appendChild(errorElement);
        
        // Add error icon
        this.updateFieldIcon(field, 'error');
    },
    
    // Show field success
    showFieldSuccess(fieldName) {
        const field = this.formFields[fieldName];
        if (!field) return;
        
        Utils.dom.addClass(field, 'success');
        Utils.dom.removeClass(field, 'error');
        this.updateFieldIcon(field, 'success');
    },
    
    // Clear field error
    clearFieldError(fieldName, removeClass = true) {
        const field = this.formFields[fieldName];
        if (!field) return;
        
        if (removeClass) {
            Utils.dom.removeClass(field, 'error');
            Utils.dom.removeClass(field, 'success');
        }
        
        // Remove error message
        const errorMessage = field.parentNode.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
        
        // Remove field icon
        this.updateFieldIcon(field, 'none');
    },
    
    // Update field icon
    updateFieldIcon(field, state) {
        // Remove existing icon
        const existingIcon = field.parentNode.querySelector('.field-icon');
        if (existingIcon) {
            existingIcon.remove();
        }
        
        if (state === 'none') return;
        
        // Create new icon
        const icon = Utils.dom.create('div', 'field-icon');
        if (state === 'error') {
            icon.innerHTML = '<i class="fas fa-exclamation-circle"></i>';
        } else if (state === 'success') {
            icon.innerHTML = '<i class="fas fa-check-circle"></i>';
        }
        
        field.parentNode.appendChild(icon);
    },
    
    // Get field label
    getFieldLabel(fieldName) {
        const field = this.formFields[fieldName];
        if (!field) return fieldName;
        
        const label = field.parentNode.querySelector('label');
        return label ? label.textContent : fieldName;
    },
    
    // Update character count
    updateCharacterCount(fieldName) {
        const field = this.formFields[fieldName];
        const rules = this.validationRules[fieldName];
        
        if (!field || !rules.maxLength) return;
        
        const currentLength = field.value.length;
        const maxLength = rules.maxLength;
        
        // Find or create character count element
        let countElement = field.parentNode.querySelector('.char-count');
        if (!countElement) {
            countElement = Utils.dom.create('div', 'char-count');
            field.parentNode.appendChild(countElement);
        }
        
        countElement.textContent = `${currentLength}/${maxLength}`;
        
        // Add warning class if near limit
        if (currentLength > maxLength * 0.9) {
            Utils.dom.addClass(countElement, 'warning');
        } else {
            Utils.dom.removeClass(countElement, 'warning');
        }
        
        // Add error class if over limit
        if (currentLength > maxLength) {
            Utils.dom.addClass(countElement, 'error');
        } else {
            Utils.dom.removeClass(countElement, 'error');
        }
    },
    
    // Handle floating labels
    handleFloatingLabel(field, isFocused) {
        const label = field.parentNode.querySelector('label');
        if (!label) return;
        
        if (isFocused || field.value.length > 0) {
            Utils.dom.addClass(label, 'floating');
        } else {
            Utils.dom.removeClass(label, 'floating');
        }
    },
    
    // Focus next field
    focusNextField(currentField) {
        const fieldNames = Object.keys(this.formFields);
        const currentFieldName = Object.keys(this.formFields).find(
            name => this.formFields[name] === currentField
        );
        
        if (currentFieldName) {
            const currentIndex = fieldNames.indexOf(currentFieldName);
            const nextIndex = currentIndex + 1;
            
            if (nextIndex < fieldNames.length) {
                const nextField = this.formFields[fieldNames[nextIndex]];
                if (nextField) {
                    nextField.focus();
                }
            }
        }
    },
    
    // Get form data
    getFormData() {
        const data = {};
        
        Object.keys(this.formFields).forEach(fieldName => {
            const field = this.formFields[fieldName];
            if (field) {
                data[fieldName] = field.value.trim();
            }
        });
        
        // Add metadata
        data.timestamp = new Date().toISOString();
        data.userAgent = navigator.userAgent;
        data.referrer = document.referrer;
        
        return data;
    },
    
    // Send form data
    async sendFormData(formData) {
        // Simulate API call - replace with actual endpoint
        if (CONFIG.contact.endpoint) {
            const response = await fetch(CONFIG.contact.endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } else {
            // Simulate delay for demo
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Simulate random success/failure for demo
            if (Math.random() > 0.1) { // 90% success rate
                return { success: true, message: 'Message sent successfully' };
            } else {
                throw new Error('Simulated server error');
            }
        }
    },
    
    // Show loading state
    showLoadingState(button) {
        button.disabled = true;
        Utils.dom.addClass(button, 'loading');
        button.innerHTML = `
            <div class="loading-spinner"></div>
            <span>Invio in corso...</span>
        `;
    },
    
    // Reset loading state
    resetLoadingState(button, originalContent) {
        button.disabled = false;
        Utils.dom.removeClass(button, 'loading');
        button.innerHTML = originalContent;
    },
    
    // Handle successful submission
    handleSuccess() {
        // Show success message
        this.showNotification(CONFIG.contact.successMessage || 'Messaggio inviato con successo!', 'success');
        
        // Reset form
        this.resetForm();
        
        // Clear auto-saved data
        this.clearAutoSave();
        
        // Trigger success event
        Utils.events.trigger(this.contactForm, 'formSuccess', {
            timestamp: new Date().toISOString()
        });
        
        // Optional: scroll to success message or top of form
        Utils.animation.scrollTo(this.contactForm, 800, 100);
    },
    
    // Handle submission error
    handleError(error) {
        let errorMessage = CONFIG.contact.errorMessage || 'Errore nell\'invio del messaggio. Riprova più tardi.';
        
        // Customize error message based on error type
        if (error.message.includes('network') || error.message.includes('fetch')) {
            errorMessage = 'Errore di connessione. Controlla la tua connessione internet.';
        } else if (error.message.includes('timeout')) {
            errorMessage = 'Timeout della richiesta. Riprova più tardi.';
        }
        
        this.showNotification(errorMessage, 'error');
        
        // Trigger error event
        Utils.events.trigger(this.contactForm, 'formError', {
            error: error.message,
            timestamp: new Date().toISOString()
        });
    },
    
    // Reset form
    resetForm() {
        this.contactForm.reset();
        
        // Clear all field states
        Object.keys(this.formFields).forEach(fieldName => {
            this.clearFieldError(fieldName);
            this.updateCharacterCount(fieldName);
            
            const field = this.formFields[fieldName];
            if (field) {
                this.handleFloatingLabel(field, false);
            }
        });
        
        // Focus first field
        const firstField = this.formFields.name;
        if (firstField) {
            setTimeout(() => firstField.focus(), 100);
        }
    },
    
    // Show notification
    showNotification(message, type = 'info') {
        // Create notification
        const notification = Utils.dom.create('div', `notification notification-${type}`);
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${this.getNotificationIcon(type)}"></i>
                <span class="notification-message">${message}</span>
                <button class="notification-close" aria-label="Chiudi notifica">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Show with animation
        setTimeout(() => Utils.dom.addClass(notification, 'show'), 100);
        
        // Auto-hide after delay
        const autoHideDelay = type === 'error' ? 8000 : 5000;
        setTimeout(() => this.hideNotification(notification), autoHideDelay);
        
        // Close button
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => this.hideNotification(notification));
        
        return notification;
    },
    
    // Hide notification
    hideNotification(notification) {
        Utils.dom.removeClass(notification, 'show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    },
    
    // Get notification icon
    getNotificationIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        return icons[type] || icons.info;
    },
    
    // Setup auto-save functionality
    setupAutoSave() {
        const autoSaveKey = 'contact-form-autosave';
        
        // Load saved data
        this.loadAutoSave();
        
        // Save data on input
        const debouncedSave = Utils.events.debounce(() => {
            this.saveFormData(autoSaveKey);
        }, 1000);
        
        Object.values(this.formFields).forEach(field => {
            if (field) {
                field.addEventListener('input', debouncedSave);
            }
        });
        
        // Clear auto-save on successful submission
        this.contactForm.addEventListener('formSuccess', () => {
            this.clearAutoSave();
        });
    },
    
    // Save form data to localStorage
    saveFormData(key) {
        const formData = this.getFormData();
        Utils.storage.set(key, {
            data: formData,
            timestamp: Date.now()
        });
    },
    
    // Load auto-saved data
    loadAutoSave() {
        const autoSaveKey = 'contact-form-autosave';
        const saved = Utils.storage.get(autoSaveKey);
        
        if (!saved) return;
        
        // Check if data is not too old (24 hours)
        const maxAge = 24 * 60 * 60 * 1000;
        if (Date.now() - saved.timestamp > maxAge) {
            this.clearAutoSave();
            return;
        }
        
        // Restore form data
        Object.keys(saved.data).forEach(fieldName => {
            const field = this.formFields[fieldName];
            if (field && saved.data[fieldName]) {
                field.value = saved.data[fieldName];
                this.handleFloatingLabel(field, false);
                this.updateCharacterCount(fieldName);
            }
        });
        
        // Show restore notification
        if (Object.values(saved.data).some(value => value.length > 0)) {
            this.showNotification('Dati del form ripristinati', 'info');
        }
    },
    
    // Clear auto-save data
    clearAutoSave() {
        const autoSaveKey = 'contact-form-autosave';
        Utils.storage.remove(autoSaveKey);
    },
    
    // Get form validation state
    getValidationState() {
        const state = {};
        
        Object.keys(this.formFields).forEach(fieldName => {
            state[fieldName] = {
                isValid: this.validateField(fieldName),
                value: this.formFields[fieldName]?.value || '',
                hasError: Utils.dom.hasClass(this.formFields[fieldName], 'error'),
                hasSuccess: Utils.dom.hasClass(this.formFields[fieldName], 'success')
            };
        });
        
        return state;
    },
    
    // Enable/disable form
    setFormEnabled(enabled) {
        Object.values(this.formFields).forEach(field => {
            if (field) {
                field.disabled = !enabled;
            }
        });
        
        const submitButton = this.contactForm.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = !enabled;
        }
    }
};

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    ContactManager.init();
});

// Export for other modules
window.ContactManager = ContactManager;