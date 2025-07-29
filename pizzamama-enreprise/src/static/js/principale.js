/**
 * 🍕 PIZZAMAMA ENTERPRISE - Framework JavaScript Principale
 * Convenzione nomi italiani per apprendimento
 */

// 🌐 Configurazione globale
const CONFIGURAZIONE_APP = {
    URL_BASE_API: '/api/',
    TIMEOUT_RICHIESTE: 10000,
    ELEMENTI_PER_PAGINA: 12,
    VERSIONE: '1.0.0'
};

// 🛡️ Gestione CSRF Token
const CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                   document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

// 🚀 Classe principale per gestione API
class GestoreAPI {
    constructor() {
        this.intestazioniBase = {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        };
    }

    async effettuaRichiesta(url, opzioni = {}) {
        const impostazioniDefault = {
            headers: this.intestazioniBase,
            credentials: 'same-origin'
        };

        try {
            const risposta = await fetch(url, { ...impostazioniDefault, ...opzioni });
            
            if (!risposta.ok) {
                throw new Error(`Errore HTTP: ${risposta.status}`);
            }
            
            return await risposta.json();
        } catch (errore) {
            console.error('Errore nella richiesta API:', errore);
            this.mostraMessaggioErrore('Errore di connessione. Riprova più tardi.');
            throw errore;
        }
    }

    mostraMessaggioErrore(messaggio) {
        // Integrazione con sistema messaggi Django
        const containerMessaggi = document.getElementById('messaggi-sistema');
        if (containerMessaggi) {
            containerMessaggi.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${messaggio}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    }

    mostraMessaggioSuccesso(messaggio) {
        const containerMessaggi = document.getElementById('messaggi-sistema');
        if (containerMessaggi) {
            containerMessaggi.innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <i class="fas fa-check-circle me-2"></i>
                    ${messaggio}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    }
}

// 🛒 Gestione Carrello (State Management Italiano)
class GestoreCarrello {
    constructor() {
        this.elementi = JSON.parse(localStorage.getItem('carrello_pizzamama') || '[]');
        this.listenerCambiamenti = [];
        this.aggiornaContatoreBadge();
    }

    aggiungiProdotto(prodotto, quantita = 1) {
        const elementoEsistente = this.elementi.find(item => item.id === prodotto.id);
        
        if (elementoEsistente) {
            elementoEsistente.quantita += quantita;
        } else {
            this.elementi.push({
                id: prodotto.id,
                nome: prodotto.nome,
                prezzo: prodotto.prezzo,
                quantita: quantita,
                immagine: prodotto.immagine
            });
        }
        
        this.salvaCarrello();
        this.notificaCambiamenti();
        this.mostraNotificaAggiunta(prodotto.nome);
    }

    rimuoviProdotto(idProdotto) {
        this.elementi = this.elementi.filter(item => item.id !== idProdotto);
        this.salvaCarrello();
        this.notificaCambiamenti();
    }

    aggiornaQuantita(idProdotto, nuovaQuantita) {
        const elemento = this.elementi.find(item => item.id === idProdotto);
        if (elemento) {
            if (nuovaQuantita <= 0) {
                this.rimuoviProdotto(idProdotto);
            } else {
                elemento.quantita = nuovaQuantita;
                this.salvaCarrello();
                this.notificaCambiamenti();
            }
        }
    }

    ottieniTotale() {
        return this.elementi.reduce((totale, item) => totale + (item.prezzo * item.quantita), 0);
    }

    ottieniQuantitaTotale() {
        return this.elementi.reduce((totale, item) => totale + item.quantita, 0);
    }

    svuotaCarrello() {
        this.elementi = [];
        this.salvaCarrello();
        this.notificaCambiamenti();
    }

    salvaCarrello() {
        localStorage.setItem('carrello_pizzamama', JSON.stringify(this.elementi));
    }

    aggiornaContatoreBadge() {
        const badge = document.getElementById('contatore-carrello');
        if (badge) {
            const quantitaTotale = this.ottieniQuantitaTotale();
            badge.textContent = quantitaTotale;
            badge.style.display = quantitaTotale > 0 ? 'inline' : 'none';
        }
    }

    notificaCambiamenti() {
        this.aggiornaContatoreBadge();
        this.listenerCambiamenti.forEach(callback => callback(this.elementi));
    }

    aggiungiListenerCambiamenti(callback) {
        this.listenerCambiamenti.push(callback);
    }

    mostraNotificaAggiunta(nomeProdotto) {
        // Toast notification italiana
        const toastHtml = `
            <div class="toast align-items-center text-white bg-success border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas fa-pizza-slice me-2"></i>
                        <strong>${nomeProdotto}</strong> aggiunta al carrello!
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;
        
        const containerToast = document.getElementById('container-toast') || this.creaContainerToast();
        containerToast.insertAdjacentHTML('beforeend', toastHtml);
        
        const toast = new bootstrap.Toast(containerToast.lastElementChild);
        toast.show();
    }

    creaContainerToast() {
        const container = document.createElement('div');
        container.id = 'container-toast';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
        return container;
    }
}

// 🍕 Gestione Catalogo Prodotti
class GestoreCatalogo {
    constructor(gestoreAPI, gestoreCarrello) {
        this.api = gestoreAPI;
        this.carrello = gestoreCarrello;
        this.prodotti = [];
        this.filtriAttivi = {
            categoria: null,
            prezzoMin: null,
            prezzoMax: null,
            ricerca: ''
        };
    }

    async caricaProdotti() {
        try {
            this.mostraSpinnerCaricamento();
            const dati = await this.api.effettuaRichiesta('/api/prodotti/');
            this.prodotti = dati.results || dati;
            this.renderizzaCatalogo();
        } catch (errore) {
            console.error('Errore caricamento prodotti:', errore);
        } finally {
            this.nascondiSpinnerCaricamento();
        }
    }

    renderizzaCatalogo(prodottiFiltrati = null) {
        const container = document.getElementById('container-prodotti');
        if (!container) return;

        const prodotti = prodottiFiltrati || this.prodotti;
        
        if (prodotti.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">Nessun prodotto trovato</h4>
                    <p class="text-muted">Prova a modificare i filtri di ricerca</p>
                </div>
            `;
            return;
        }

        container.innerHTML = prodotti.map(prodotto => this.creaCardProdotto(prodotto)).join('');
        this.associaEventiCardsPerFormance();
    }

    creaCardProdotto(prodotto) {
        const prezzoFormattato = new Intl.NumberFormat('it-IT', {
            style: 'currency',
            currency: 'EUR'
        }).format(prodotto.prezzo);

        return `
            <div class="col-lg-4 col-md-6 col-sm-12 mb-4">
                <div class="card prodotto-card h-100 shadow-sm">
                    <div class="posizione-relativa">
                        <img src="${prodotto.immagine || '/static/images/pizza-default.jpg'}" 
                             class="card-img-top" 
                             alt="${prodotto.nome}"
                             style="height: 200px; object-fit: cover;">
                        ${prodotto.popolare ? '<span class="badge bg-warning posizione-assoluta top-0 start-0 m-2">🔥 Popolare</span>' : ''}
                    </div>
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${prodotto.nome}</h5>
                        <p class="card-text text-muted piccolo mb-2">${prodotto.descrizione}</p>
                        <div class="ingredienti mb-2">
                            <small class="text-muted">
                                <i class="fas fa-leaf me-1"></i>
                                ${prodotto.ingredienti?.slice(0, 3).join(', ') || 'Ingredienti vari'}
                            </small>
                        </div>
                        <div class="mt-auto">
                            <div class="d-flex justify-content-between align-items-center">
                                <h4 class="prezzo mb-0 text-primary">${prezzoFormattato}</h4>
                                <button class="btn btn-primary btn-aggiungi-carrello" 
                                        data-prodotto-id="${prodotto.id}">
                                    <i class="fas fa-cart-plus me-1"></i>
                                    Aggiungi
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    associaEventiCardsPerFormance() {
        // Event delegation per performance migliori
        const container = document.getElementById('container-prodotti');
        if (!container) return;

        container.addEventListener('click', (evento) => {
            const bottone = evento.target.closest('.btn-aggiungi-carrello');
            if (bottone) {
                const idProdotto = parseInt(bottone.dataset.prodottoId);
                const prodotto = this.prodotti.find(p => p.id === idProdotto);
                if (prodotto) {
                    this.carrello.aggiungiProdotto(prodotto);
                }
            }
        });
    }

    applicaFiltri() {
        let prodottiFiltrati = this.prodotti;

        // Filtro per categoria
        if (this.filtriAttivi.categoria) {
            prodottiFiltrati = prodottiFiltrati.filter(p => 
                p.categoria === this.filtriAttivi.categoria
            );
        }

        // Filtro per prezzo
        if (this.filtriAttivi.prezzoMin !== null) {
            prodottiFiltrati = prodottiFiltrati.filter(p => 
                p.prezzo >= this.filtriAttivi.prezzoMin
            );
        }

        if (this.filtriAttivi.prezzoMax !== null) {
            prodottiFiltrati = prodottiFiltrati.filter(p => 
                p.prezzo <= this.filtriAttivi.prezzoMax
            );
        }

        // Filtro per ricerca testuale
        if (this.filtriAttivi.ricerca) {
            const termineRicerca = this.filtriAttivi.ricerca.toLowerCase();
            prodottiFiltrati = prodottiFiltrati.filter(p => 
                p.nome.toLowerCase().includes(termineRicerca) ||
                p.descrizione.toLowerCase().includes(termineRicerca)
            );
        }

        this.renderizzaCatalogo(prodottiFiltrati);
    }

    mostraSpinnerCaricamento() {
        const container = document.getElementById('container-prodotti');
        if (container) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Caricamento...</span>
                    </div>
                    <p class="mt-3 text-muted">Caricamento prodotti...</p>
                </div>
            `;
        }
    }

    nascondiSpinnerCaricamento() {
        // Lo spinner viene nascosto automaticamente quando si renderizza il catalogo
    }
}

// 🎛️ Inizializzazione globale dell'applicazione
class AppPizzaMama {
    constructor() {
        this.api = new GestoreAPI();
        this.carrello = new GestoreCarrello();
        this.catalogo = new GestoreCatalogo(this.api, this.carrello);
        
        this.inizializzaApp();
    }

    inizializzaApp() {
        // Aspetta che il DOM sia caricato
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.configuraManaagers());
        } else {
            this.configuraManaagers();
        }
    }

    configuraManaagers() {
        // Configura navigation responsiva
        this.configuraBarra();
        
        // Carica prodotti se siamo nella pagina catalogo
        if (document.getElementById('container-prodotti')) {
            this.catalogo.caricaProdotti();
            this.configuraFiltriCatalogo();
        }

        // Configura pagina carrello se presente
        if (document.getElementById('pagina-carrello')) {
            this.configuraCarrello();
        }

        // Listeners globali
        this.configuraListenersGlobali();
    }

    configuraBarra() {
        // Gestione menu mobile
        const toggleMenu = document.getElementById('toggle-menu-mobile');
        const menuMobile = document.getElementById('menu-navigazione-mobile');
        
        if (toggleMenu && menuMobile) {
            toggleMenu.addEventListener('click', () => {
                menuMobile.classList.toggle('show');
            });
        }
    }

    configuraFiltriCatalogo() {
        // Gestione filtri ricerca
        const inputRicerca = document.getElementById('input-ricerca-prodotti');
        if (inputRicerca) {
            let timeoutRicerca;
            inputRicerca.addEventListener('input', (evento) => {
                clearTimeout(timeoutRicerca);
                timeoutRicerca = setTimeout(() => {
                    this.catalogo.filtriAttivi.ricerca = evento.target.value;
                    this.catalogo.applicaFiltri();
                }, 300); // Debounce di 300ms
            });
        }

        // Gestione filtri categoria
        const selectCategoria = document.getElementById('filtro-categoria');
        if (selectCategoria) {
            selectCategoria.addEventListener('change', (evento) => {
                this.catalogo.filtriAttivi.categoria = evento.target.value || null;
                this.catalogo.applicaFiltri();
            });
        }
    }

    configuraCarrello() {
        // Renderizza contenuto carrello
        this.renderizzaCarrello();
        
        // Listener per cambiamenti carrello
        this.carrello.aggiungiListenerCambiamenti((elementi) => {
            this.renderizzaCarrello();
        });
    }

    renderizzaCarrello() {
        const containerCarrello = document.getElementById('elementi-carrello');
        const containerTotalE = document.getElementById('totale-carrello');
        
        if (!containerCarrello) return;

        if (this.carrello.elementi.length === 0) {
            containerCarrello.innerHTML = `
                <div class="text-center py-5">
                    <i class="fas fa-shopping-cart fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">Il tuo carrello è vuoto</h4>
                    <p class="text-muted">Aggiungi qualche deliziosa pizza!</p>
                    <a href="/catalogo/" class="btn btn-primary">
                        <i class="fas fa-pizza-slice me-2"></i>
                        Esplora il catalogo
                    </a>
                </div>
            `;
            return;
        }

        // Renderizza elementi carrello
        containerCarrello.innerHTML = this.carrello.elementi.map(elemento => `
            <div class="row elemento-carrello py-3 border-bottom" data-id="${elemento.id}">
                <div class="col-md-2">
                    <img src="${elemento.immagine || '/static/images/pizza-default.jpg'}" 
                         class="img-fluid rounded" alt="${elemento.nome}">
                </div>
                <div class="col-md-4">
                    <h6 class="mb-1">${elemento.nome}</h6>
                    <small class="text-muted">Pizza artigianale</small>
                </div>
                <div class="col-md-2">
                    <div class="input-group input-group-sm">
                        <button class="btn btn-outline-secondary btn-diminuisci" data-id="${elemento.id}">-</button>
                        <input type="number" class="form-control text-center input-quantita" 
                               value="${elemento.quantita}" min="1" data-id="${elemento.id}">
                        <button class="btn btn-outline-secondary btn-aumenta" data-id="${elemento.id}">+</button>
                    </div>
                </div>
                <div class="col-md-2 text-end">
                    <strong>${(elemento.prezzo * elemento.quantita).toFixed(2)}€</strong>
                </div>
                <div class="col-md-2 text-end">
                    <button class="btn btn-sm btn-outline-danger btn-rimuovi" data-id="${elemento.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');

        // Aggiorna totale
        if (containerTotalE) {
            containerTotalE.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Riepilogo Ordine</h5>
                        <div class="d-flex justify-content-between">
                            <span>Subtotale:</span>
                            <span>${this.carrello.ottieniTotale().toFixed(2)}€</span>
                        </div>
                        <div class="d-flex justify-content-between">
                            <span>Consegna:</span>
                            <span>3.50€</span>
                        </div>
                        <hr>
                        <div class="d-flex justify-content-between">
                            <strong>Totale:</strong>
                            <strong>${(this.carrello.ottieniTotale() + 3.50).toFixed(2)}€</strong>
                        </div>
                        <button class="btn btn-success w-100 mt-3" id="btn-procedi-checkout">
                            <i class="fas fa-credit-card me-2"></i>
                            Procedi al pagamento
                        </button>
                    </div>
                </div>
            `;
        }

        // Associa eventi per gestione quantità
        this.associaEventiCarrello();
    }

    associaEventiCarrello() {
        const containerCarrello = document.getElementById('elementi-carrello');
        if (!containerCarrello) return;

        containerCarrello.addEventListener('click', (evento) => {
            const elemento = evento.target;
            const id = parseInt(elemento.dataset.id);

            if (elemento.classList.contains('btn-aumenta')) {
                const inputQuantita = containerCarrello.querySelector(`input[data-id="${id}"]`);
                const nuovaQuantita = parseInt(inputQuantita.value) + 1;
                this.carrello.aggiornaQuantita(id, nuovaQuantita);
            }

            if (elemento.classList.contains('btn-diminuisci')) {
                const inputQuantita = containerCarrello.querySelector(`input[data-id="${id}"]`);
                const nuovaQuantita = Math.max(1, parseInt(inputQuantita.value) - 1);
                this.carrello.aggiornaQuantita(id, nuovaQuantita);
            }

            if (elemento.classList.contains('btn-rimuovi')) {
                this.carrello.rimuoviProdotto(id);
            }
        });

        // Gestione input quantità diretta
        containerCarrello.addEventListener('change', (evento) => {
            if (evento.target.classList.contains('input-quantita')) {
                const id = parseInt(evento.target.dataset.id);
                const nuovaQuantita = parseInt(evento.target.value) || 1;
                this.carrello.aggiornaQuantita(id, nuovaQuantita);
            }
        });
    }

    configuraListenersGlobali() {
        // Gestione forme di contatto
        const formContatto = document.getElementById('form-contatto');
        if (formContatto) {
            formContatto.addEventListener('submit', (evento) => this.gestisciInvioContatto(evento));
        }

        // Gestione scroll per navbar
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (navbar) {
                if (window.scrollY > 100) {
                    navbar.classList.add('navbar-scrolled');
                } else {
                    navbar.classList.remove('navbar-scrolled');
                }
            }
        });
    }

    async gestisciInvioContatto(evento) {
        evento.preventDefault();
        
        const formData = new FormData(evento.target);
        const datiContatto = Object.fromEntries(formData.entries());

        try {
            const risposta = await this.api.effettuaRichiesta('/api/contatti/', {
                method: 'POST',
                body: JSON.stringify(datiContatto)
            });

            this.api.mostraMessaggioSuccesso('Messaggio inviato con successo! Ti risponderemo presto.');
            evento.target.reset();
        } catch (errore) {
            this.api.mostraMessaggioErrore('Errore nell\'invio del messaggio. Riprova più tardi.');
        }
    }
}

// 🚀 Avvio automatico applicazione
window.pizzaMamaApp = new AppPizzaMama();

// 💡 Utilities globali italiane
window.utilita = {
    formattaPrezzo: (prezzo) => new Intl.NumberFormat('it-IT', {
        style: 'currency',
        currency: 'EUR'
    }).format(prezzo),
    
    formattaData: (data) => new Intl.DateTimeFormat('it-IT').format(new Date(data)),
    
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
    }
};

console.log('🍕 PizzaMama Enterprise - JavaScript Framework caricato con successo!');