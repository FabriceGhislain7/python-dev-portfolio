/*
===========================================
CONTACT MODULE
===========================================
Gestisce il form di contatto con validazione e invio
*/

(function() {
    'use strict';

    // Variabili del modulo
    let contactForm = null;
    let formInputs = {};
    let formErrors = {};
    let isSubmitting = false;
    let validationRules = {};

    /* ================================ */
    /* INIZIALIZZAZIONE                 */
    /* ================================ */
    function init() {
        // Ottieni riferimenti elementi DOM
        contactForm = document.getElementById('contact-form');

        if (!contactForm) {
            console.warn('Contact form not found');
            return;
        }

        // Ottieni tutti gli input del form
        getFormElements();

        // Setup regole di validazione
        setupValidationRules();

        // Setup event listeners
        setupFormListeners();

        // Setup animazioni label floating
        setupFloatingLabels();

        window.PortfolioConfig.utils.log('debug', 'Contact module initialized');
    }

    /* ================================ */
    /* ELEMENTI FORM                    */
    /* ================================ */
    function getFormElements() {
        formInputs = {
            name: contactForm.querySelector('#name'),
            email: contactForm.querySelector('#email'),
            subject: contactForm.querySelector('#subject'),
            message: contactForm.querySelector('#message')
        };

        formErrors = {
            name: contactForm.querySelector('#name').parentNode.querySelector('.form-error'),
            email: contactForm.querySelector('#email').parentNode.querySelector('.form-error'),
            subject: contactForm.querySelector('#subject').parentNode.querySelector('.form-error'),
            message: contactForm.querySelector('#message').parentNode.querySelector('.form-error')
        };

        // Verifica che tutti gli elementi esistano
        Object.keys(formInputs).forEach(key => {
            if (!formInputs[key]) {
                console.warn(`Form input '${key}' not found`);
            }
        });
    }

    /* ================================ */
    /* REGOLE DI VALIDAZIONE            */
    /* ================================ */
    function setupValidationRules() {
        validationRules = {
            name: {
                required: true,
                minLength: 2,
                maxLength: 50,
                pattern: /^[a-zA-ZÀ-ÿ\s'-]+$/,
                messages: {
                    required: 'Il nome è richiesto',
                    minLength: 'Il nome deve avere almeno 2 caratteri',
                    maxLength: 'Il nome non può superare 50 caratteri',
                    pattern: 'Il nome può contenere solo lettere, spazi, apostrofi e trattini'
                }
            },
            email: {
                required: true,
                pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                maxLength: 100,
                messages: {
                    required: 'L\'email è richiesta',
                    pattern: 'Inserisci un indirizzo email valido',
                    maxLength: 'L\'email non può superare 100 caratteri'
                }
            },
            subject: {
                required: true,
                minLength: 5,
                maxLength: 100,
                messages: {
                    required: 'L\'oggetto è richiesto',
                    minLength: 'L\'oggetto deve avere almeno 5 caratteri',
                    maxLength: 'L\'oggetto non può superare 100 caratteri'
                }
            },
            message: {
                required: true,
                minLength: 10,
                maxLength: 1000,
                messages: {
                    required: 'Il messaggio è richiesto',
                    minLength: 'Il messaggio deve avere almeno 10 caratteri',
                    maxLength: 'Il messaggio non può superare 1000 caratteri'
                }
            }
        };
    }

    /* ================================ */
    /* EVENT LISTENERS                  */
    /* ================================ */
    function setupFormListeners() {
        // Submit form
        contactForm.addEventListener('submit', handleFormSubmit);

        // Validazione in tempo reale per ogni input
        Object.keys(formInputs).forEach(fieldName => {
            const input = formInputs[fieldName];
            
            if (input) {
                // Validazione on blur
                if (window.PortfolioConfig.components.contact.validateOnBlur) {
                    input.addEventListener('blur', () => validateField(fieldName));
                }

                // Validazione on input (mentre digita)
                if (window.PortfolioConfig.components.contact.validateOnType) {
                    input.addEventListener('input', window.PortfolioConfig.utils.debounce(() => {
                        if (input.value.length > 0) {
                            validateField(fieldName);
                        }
                    }, 300));
                }

                // Rimuovi errore quando inizia a digitare
                input.addEventListener('input', () => {
                    if (formErrors[fieldName]) {
                        clearFieldError(fieldName);
                    }
                });

                // Character counter per textarea
                if (fieldName === 'message') {
                    setupCharacterCounter(input);
                }
            }
        });

        // Previeni invio accidentale con Enter
        Object.values(formInputs).forEach(input => {
            if (input && input.type !== 'textarea') {
                input.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        const nextInput = getNextFormInput(input);
                        if (nextInput) {
                            nextInput.focus();
                        }
                    }
                });
            }
        });
    }

    /* ================================ */
    /* FLOATING LABELS                  */
    /* ================================ */
    function setupFloatingLabels() {
        Object.values(formInputs).forEach(input => {
            if (!input) return;

            const updateLabel = () => {
                const formGroup = input.parentNode;
                const label = formGroup.querySelector('.form-label');
                
                if (input.value.length > 0 || input === document.activeElement) {
                    formGroup.classList.add('form-group-focused');
                    if (label) label.classList.add('form-label-focused');
                } else {
                    formGroup.classList.remove('form-group-focused');
                    if (label) label.classList.remove('form-label-focused');
                }
            };

            input.addEventListener('focus', updateLabel);
            input.addEventListener('blur', updateLabel);
            input.addEventListener('input', updateLabel);

            // Inizializza stato
            updateLabel();
        });
    }

    /* ================================ */
    /* CHARACTER COUNTER                */
    /* ================================ */
    function setupCharacterCounter(textarea) {
        const maxLength = validationRules.message.maxLength;
        
        // Crea counter element
        const counter = document.createElement('div');
        counter.className = 'character-counter';
        counter.innerHTML = `<span class="counter-current">0</span>/<span class="counter-max">${maxLength}</span>`;
        
        // Inserisci dopo il textarea
        textarea.parentNode.appendChild(counter);

        // Update counter
        const updateCounter = () => {
            const currentLength = textarea.value.length;
            const currentSpan = counter.querySelector('.counter-current');
            
            currentSpan.textContent = currentLength;
            
            // Cambia colore in base alla lunghezza
            counter.classList.remove('counter-warning', 'counter-danger');
            
            if (currentLength > maxLength * 0.9) {
                counter.classList.add('counter-warning');
            }
            if (currentLength > maxLength) {
                counter.classList.add('counter-danger');
            }
        };

        textarea.addEventListener('input', updateCounter);
        updateCounter();
    }

    /* ================================ */
    /* VALIDAZIONE                      */
    /* ================================ */
    function validateField(fieldName) {
        const input = formInputs[fieldName];
        const rules = validationRules[fieldName];
        
        if (!input || !rules) return true;

        const value = input.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Required validation
        if (rules.required && value.length === 0) {
            isValid = false;
            errorMessage = rules.messages.required;
        }

        // Length validations
        if (isValid && rules.minLength && value.length < rules.minLength) {
            isValid = false;
            errorMessage = rules.messages.minLength;
        }

        if (isValid && rules.maxLength && value.length > rules.maxLength) {
            isValid = false;
            errorMessage = rules.messages.maxLength;
        }

        // Pattern validation
        if (isValid && rules.pattern && !rules.pattern.test(value)) {
            isValid = false;
            errorMessage = rules.messages.pattern;
        }

        // Mostra/nascondi errore
        if (isValid) {
            clearFieldError(fieldName);
        } else {
            showFieldError(fieldName, errorMessage);
        }

        return isValid;
    }

    function validateForm() {
        let isValid = true;
        
        Object.keys(formInputs).forEach(fieldName => {
            if (!validateField(fieldName)) {
                isValid = false;
            }
        });

        return isValid;
    }

    function showFieldError(fieldName, message) {
        const input = formInputs[fieldName];
        const errorElement = formErrors[fieldName];
        
        if (input && errorElement) {
            input.classList.add('form-input-error');
            errorElement.textContent = message;
            errorElement.classList.add('form-error-visible');
        }
    }

    function clearFieldError(fieldName) {
        const input = formInputs[fieldName];
        const errorElement = formErrors[fieldName];
        
        if (input && errorElement) {
            input.classList.remove('form-input-error');
            errorElement.textContent = '';
            errorElement.classList.remove('form-error-visible');
        }
    }

    function clearAllErrors() {
        Object.keys(formInputs).forEach(fieldName => {
            clearFieldError(fieldName);
        });
    }

    /* ================================ */
    /* INVIO FORM                       */
    /* ================================ */
    function handleFormSubmit(e) {
        e.preventDefault();
        
        if (isSubmitting) return;

        // Valida form
        if (!validateForm()) {
            showFormMessage('Correggi gli errori evidenziati', 'error');
            return;
        }

        // Simula invio (in un'app reale, qui invieresti i dati)
        submitForm();
    }

    async function submitForm() {
        isSubmitting = true;
        
        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        
        try {
            // Mostra loading state
            setSubmitButtonLoading(submitButton, true);
            
            // Raccoglie dati form
            const formData = collectFormData();
            
            // Simula invio (sostituisci con vera API call)
            await simulateFormSubmission(formData);
            
            // Successo
            showFormMessage(window.PortfolioConfig.components.contact.successMessage, 'success');
            resetForm();
            
            window.PortfolioConfig.utils.log('info', 'Contact form submitted successfully');
            
        } catch (error) {
            // Errore
            showFormMessage(window.PortfolioConfig.components.contact.errorMessage, 'error');
            console.error('Form submission error:', error);
            
        } finally {
            isSubmitting = false;
            setSubmitButtonLoading(submitButton, false, originalText);
        }
    }

    function collectFormData() {
        const data = {};
        
        Object.keys(formInputs).forEach(fieldName => {
            const input = formInputs[fieldName];
            if (input) {
                data[fieldName] = input.value.trim();
            }
        });

        // Aggiungi timestamp e metadata
        data.timestamp = new Date().toISOString();
        data.userAgent = navigator.userAgent;
        data.referrer = document.referrer;
        
        return data;
    }

    async function simulateFormSubmission(formData) {
        // Simula una chiamata API
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // Simula successo al 90%
                if (Math.random() > 0.1) {
                    resolve({ success: true, data: formData });
                } else {
                    reject(new Error('Simulated network error'));
                }
            }, 2000);
        });
    }

    /* ================================ */
    /* UI HELPERS                       */
    /* ================================ */
    function setSubmitButtonLoading(button, loading, originalText = '') {
        if (loading) {
            button.classList.add('loading');
            button.disabled = true;
            button.innerHTML = `
                <span>Invio in corso...</span>
                <i class="fas fa-spinner fa-spin"></i>
            `;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
            button.innerHTML = originalText || `
                <span>Invia Messaggio</span>
                <i class="fas fa-paper-plane"></i>
            `;
        }
    }

    function showFormMessage(message, type = 'info') {
        // Rimuovi messaggi esistenti
        const existingMessage = contactForm.querySelector('.form-message');
        if (existingMessage) {
            existingMessage.remove();
        }

        // Crea nuovo messaggio
        const messageElement = document.createElement('div');
        messageElement.className = `form-message form-message-${type}`;
        messageElement.innerHTML = `
            <div class="message-content">
                <i class="fas fa-${getMessageIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;

        // Inserisci prima del bottone submit
        const submitButton = contactForm.querySelector('button[type="submit"]');
        contactForm.insertBefore(messageElement, submitButton);

        // Anima entrata
        setTimeout(() => {
            messageElement.classList.add('form-message-visible');
        }, 10);

        // Rimuovi automaticamente dopo 5 secondi
        setTimeout(() => {
            messageElement.classList.remove('form-message-visible');
            setTimeout(() => {
                if (messageElement.parentNode) {
                    messageElement.remove();
                }
            }, 300);
        }, 5000);
    }

    function getMessageIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    function resetForm() {
        contactForm.reset();
        clearAllErrors();
        
        // Reset floating labels
        Object.values(formInputs).forEach(input => {
            if (input) {
                const formGroup = input.parentNode;
                const label = formGroup.querySelector('.form-label');
                
                formGroup.classList.remove('form-group-focused');
                if (label) label.classList.remove('form-label-focused');
            }
        });

        // Reset character counter
        const counter = contactForm.querySelector('.character-counter .counter-current');
        if (counter) {
            counter.textContent = '0';
            counter.parentNode.classList.remove('counter-warning', 'counter-danger');
        }
    }

    /* ================================ */
    /* UTILITIES                        */
    /* ================================ */
    function getNextFormInput(currentInput) {
        const inputs = Object.values(formInputs).filter(input => input);
        const currentIndex = inputs.indexOf(currentInput);
        return inputs[currentIndex + 1] || null;
    }

    function focusFirstErrorField() {
        const firstErrorField = Object.keys(formInputs).find(fieldName => {
            const input = formInputs[fieldName];
            return input && input.classList.contains('form-input-error');
        });

        if (firstErrorField && formInputs[firstErrorField]) {
            formInputs[firstErrorField].focus();
        }
    }

    /* ================================ */
    /* API PUBBLICA                     */
    /* ================================ */
    window.ContactModule = {
        init,
        validate: validateForm,
        reset: resetForm,
        showMessage: showFormMessage,
        setFieldValue: (fieldName, value) => {
            if (formInputs[fieldName]) {
                formInputs[fieldName].value = value;
            }
        },
        getFormData: collectFormData
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