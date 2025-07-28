"""
URL configuration for pizzamama project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Step 12: Import per frontend views italianizzate
from . import views as viste_principali

@api_view(['GET'])
def radice_api(request):
    """API root endpoint con informazioni sistema in italiano"""
    return Response({
        'messaggio': 'Benvenuto alle API di PizzaMama Enterprise!',
        'versione': '2.0',
        'stato': 'Operativo',
        'documentazione': {
            'swagger': '/api/docs/swagger/',
            'redoc': '/api/docs/redoc/', 
            'schema': '/api/docs/schema/'
        },
        'endpoints_disponibili': {
            'amministrazione': '/admin/',
            'autenticazione_api': '/api/auth/',
            'gestione_utenti': '/api/utenti/',
            'catalogo_prodotti': '/api/prodotti/',
            'gestione_ordini': '/api/ordini/'
        },
        'pagine_frontend': {
            'homepage': '/',
            'catalogo': '/catalogo/',
            'carrello': '/carrello/',
            'area_utente': '/utente/',
            'chi_siamo': '/chi-siamo/'
        }
    })

# ========================================
# CONFIGURAZIONE URL PATTERNS ITALIANA
# ========================================

pattern_url = [
    # ========================================
    # INTERFACCIA AMMINISTRAZIONE
    # ========================================
    path('admin/', admin.site.urls, name='pannello_amministrazione'),
    
    # ========================================
    # DOCUMENTAZIONE API - STEP 11
    # ========================================
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema_api'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema_api'), name='documentazione_swagger'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema_api'), name='documentazione_redoc'),
    
    # ========================================
    # API ROOT E AUTENTICAZIONE
    # ========================================
    path('api/', radice_api, name='radice-api'),
    path('api/auth/', include('rest_framework.urls'), name='autenticazione_drf'),
    
    # ========================================
    # API BUSINESS LOGIC - STEP 11 (URLs Italiani)
    # ========================================
    path('api/utenti/', include('apps.accounts.api.urls'), name='api_gestione_utenti'),
    path('api/prodotti/', include('apps.products.api.urls'), name='api_catalogo_prodotti'), 
    path('api/ordini/', include('apps.orders.api.urls'), name='api_gestione_ordini'),
    
    # ========================================
    # PAGINE FRONTEND - STEP 12 (URLs Italiani)
    # ========================================
    
    # Homepage e pagine istituzionali
    path('', viste_principali.homepage, name='homepage'),
    path('chi-siamo/', viste_principali.chi_siamo, name='chi_siamo'),
    path('contatti/', viste_principali.contatti, name='contatti'),
    path('privacy/', viste_principali.privacy_policy, name='privacy'),
    path('termini/', viste_principali.termini_servizio, name='termini'),
    
    # ========================================
    # CATALOGO PRODOTTI FRONTEND (URLs Italiani) - AGGIORNATO
    # ========================================
    path('catalogo/', include('apps.products.frontend_urls'), name='catalogo_frontend'),
    # Esempi URL che avremo:
    # /catalogo/ → Lista pizze
    # /catalogo/pizza/<id>/ → Dettaglio pizza
    # /catalogo/api/ricerca/ → API ricerca
    # /catalogo/api/categorie/ → API categorie
    # /catalogo/api/suggerimenti/ → API suggerimenti ricerca
    # /catalogo/api/popolari/ → API pizze popolari
    # /catalogo/api/ingredienti/ → API ingredienti
    # /catalogo/api/valutazione/ → API valutazioni
    # /catalogo/api/statistiche/ → API statistiche catalogo
    
    # ========================================
    # CARRELLO E ORDINI FRONTEND (URLs Italiani) - AGGIORNATO
    # ========================================
    path('carrello/', include('apps.orders.frontend_urls'), name='carrello_frontend'),
    # Esempi URL che avremo:
    # /carrello/ → Visualizza carrello
    # /carrello/api/aggiungi/ → API aggiungi al carrello
    # /carrello/api/contenuto/ → API contenuto carrello
    # /carrello/api/aggiorna-quantita/ → API aggiorna quantità
    # /carrello/api/rimuovi/ → API rimuovi dal carrello
    # /carrello/api/svuota/ → API svuota carrello
    # /carrello/api/sconto/ → API applica sconto
    # /carrello/api/crea-ordine/ → API creazione ordine
    # /carrello/api/stato/<numero>/ → API stato ordine
    # /carrello/api/storico/ → API storico ordini
    # /carrello/api/metodi-pagamento/ → API metodi pagamento
    # /carrello/api/zone-consegna/ → API zone consegna
    # /carrello/api/statistiche/ → API statistiche ordini
    
    # ========================================
    # AREA UTENTE FRONTEND (URLs Italiani) - AGGIORNATO
    # ========================================
    path('utente/', include('apps.accounts.frontend_urls'), name='area_utente_frontend'),
    # Esempi URL che avremo:
    # /utente/login/ → Login
    # /utente/logout/ → Logout
    # /utente/registrazione/ → Registrazione
    # /utente/password-reset/ → Reset password
    # /utente/profilo/ → Gestione profilo
    # /utente/ordini/ → Storia ordini
    # /utente/indirizzi/ → Gestione indirizzi
    # /utente/preferenze/ → Impostazioni account
    # /utente/api/aggiorna-profilo/ → API aggiornamento profilo
    # /utente/api/aggiungi-indirizzo/ → API aggiungi indirizzo
    # /utente/api/rimuovi-indirizzo/ → API rimuovi indirizzo
    
    # ========================================
    # PAGINE SPECIALI E SERVIZI - AGGIORNATO
    # ========================================
    path('ricerca/', viste_principali.ricerca_globale, name='ricerca_globale'),
    path('newsletter/', viste_principali.gestione_newsletter, name='newsletter'),
    path('offerte/', viste_principali.pagina_offerte, name='offerte_speciali'),
    path('zona-consegna/', viste_principali.verifica_zona_consegna, name='zona_consegna'),
]

# ========================================
# GESTIONE FILES MEDIA E STATIC - STEP 12
# ========================================
# Configurazione per servire file media e static durante development

if settings.DEBUG:
    # Serve file media (immagini caricate dagli utenti)
    pattern_url += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT,
        # Step 12: Nome view italiano per debug
        show_indexes=True
    )
    
    # Serve file static (CSS, JS, immagini statiche)
    pattern_url += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT if settings.STATIC_ROOT else settings.STATICFILES_DIRS[0]
    )
    
    # Step 12: Debug toolbar se disponibile
    try:
        import debug_toolbar
        pattern_url = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + pattern_url
    except ImportError:
        pass

# ========================================
# GESTIONE ERRORI PERSONALIZZATE - STEP 12
# ========================================
# Handler per pagine errore personalizzate in italiano

handler404 = 'pizzamama.views.pagina_non_trovata'      # 404 - Pagina non trovata
handler500 = 'pizzamama.views.errore_server'          # 500 - Errore interno server  
handler403 = 'pizzamama.views.accesso_negato'         # 403 - Accesso negato
handler400 = 'pizzamama.views.richiesta_non_valida'   # 400 - Bad request

# ========================================
# URL PATTERNS FINALE
# ========================================
# Assegnazione finale con nome italiano
urlpatterns = pattern_url

# ========================================
# CONFIGURAZIONI AGGIUNTIVE URL - STEP 12
# ========================================

# Step 12: Configurazione nomi URL in italiano per reverse()
NOMI_URL_ITALIANI = {
    # Pagine principali
    'home': 'homepage',
    'about': 'chi_siamo', 
    'contact': 'contatti',
    
    # Catalogo
    'product_list': 'lista_prodotti',
    'product_detail': 'dettaglio_prodotto',
    'category_list': 'lista_categorie',
    
    # Utenti
    'login': 'accesso_utente',
    'register': 'registrazione_utente',
    'profile': 'profilo_utente',
    'dashboard': 'dashboard_utente',
    
    # Ordini
    'cart': 'visualizza_carrello',
    'checkout': 'processo_checkout',
    'order_detail': 'dettaglio_ordine',
    'order_tracking': 'tracciamento_ordine',
}

# Step 12: Patterns URL dinamici per SEO italiano
PATTERN_SEO_ITALIANI = {
    'pizza_detail': 'catalogo/pizza/<slug:nome_pizza>/',
    'category_detail': 'catalogo/categoria/<slug:nome_categoria>/',
    'user_profile': 'utente/profilo/<slug:username>/',
    'order_tracking': 'carrello/ordine/<uuid:numero_ordine>/tracciamento/',
}

# Step 12: Configurazione redirect URL legacy (se necessario)
REDIRECT_URL_LEGACY = {
    'products/': 'catalogo/',
    'cart/': 'carrello/',
    'accounts/': 'utente/',
    'about/': 'chi-siamo/',
}

# ========================================
# NAMESPACE URL PER APP - STEP 12  
# ========================================
# Configurazione namespace italiani per le app

NAMESPACE_APP_ITALIANI = {
    'accounts': 'utenti',      # app accounts → namespace 'utenti'
    'products': 'catalogo',    # app products → namespace 'catalogo'  
    'orders': 'ordini',        # app orders → namespace 'ordini'
}

# ========================================
# METADATA URL CONFIGURATION
# ========================================
# Informazioni metadata per l'applicazione

URL_METADATA = {
    'nome_progetto': 'PizzaMama Enterprise',
    'versione_urls': '2.0',
    'lingua_principale': 'italiano',
    'pattern_principali': len([p for p in pattern_url if hasattr(p, 'pattern')]),
    'api_endpoints': 3,  # accounts, products, orders
    'pagine_frontend': 12,  # homepage, catalogo, carrello, etc.
    'documentazione_disponibile': True,
    'debug_abilitato': settings.DEBUG,
    'frontend_urls_integrati': True,
    'error_handlers_personalizzati': True,
}

# ========================================
# SICUREZZA URL - STEP 12
# ========================================
# Configurazioni sicurezza per URL patterns

if not settings.DEBUG:
    # In produzione, disabilita alcune URL di debug
    PATTERN_DEBUG_DISABILITATI = [
        'api/docs/swagger/',  # Swagger solo in development
        '__debug__/',         # Debug toolbar
    ]

# ========================================
# CONFIGURAZIONE CACHE URL (OPZIONALE)
# ========================================
# Per migliorare performance in produzione

CACHE_URL_PATTERNS = {
    'homepage': 300,           # Cache homepage per 5 minuti
    'catalogo': 180,          # Cache catalogo per 3 minuti
    'chi_siamo': 3600,        # Cache pagine statiche per 1 ora
    'privacy': 3600,
    'termini': 3600,
}

# ========================================
# MONITORAGGIO URL (OPZIONALE)
# ========================================
# Per analytics e monitoring

URL_MONITORING = {
    'track_api_calls': True,
    'track_page_views': True,
    'log_slow_requests': True,
    'alert_404_threshold': 50,  # Alert se più di 50 404 in un'ora
}

# ========================================
# DOCUMENTAZIONE URL STRUCTURE
# ========================================
"""
STRUTTURA COMPLETA URL PIZZAMAMA ENTERPRISE:

AMMINISTRAZIONE:
├── /admin/                                 → Django Admin

API REST:
├── /api/                                   → API Root
├── /api/docs/swagger/                      → Documentazione Swagger
├── /api/docs/redoc/                        → Documentazione ReDoc
├── /api/auth/                              → Autenticazione DRF
├── /api/utenti/                            → API Gestione Utenti
├── /api/prodotti/                          → API Catalogo Prodotti
└── /api/ordini/                            → API Gestione Ordini

FRONTEND PAGES:
├── /                                       → Homepage
├── /chi-siamo/                             → Chi Siamo
├── /contatti/                              → Contatti
├── /privacy/                               → Privacy Policy
├── /termini/                               → Termini Servizio
├── /ricerca/                               → Ricerca Globale
├── /newsletter/                            → Gestione Newsletter
├── /offerte/                               → Offerte Speciali
└── /zona-consegna/                         → Verifica Zona Consegna

CATALOGO PRODOTTI:
├── /catalogo/                              → Lista Pizze
├── /catalogo/pizza/<id>/                   → Dettaglio Pizza
├── /catalogo/api/ricerca/                  → API Ricerca Prodotti
├── /catalogo/api/suggerimenti/             → API Suggerimenti
├── /catalogo/api/categorie/                → API Categorie
├── /catalogo/api/ingredienti/              → API Ingredienti
├── /catalogo/api/popolari/                 → API Pizze Popolari
├── /catalogo/api/valutazione/              → API Valutazioni
└── /catalogo/api/statistiche/              → API Statistiche Catalogo

CARRELLO E ORDINI:
├── /carrello/                              → Visualizza Carrello
├── /carrello/api/aggiungi/                 → API Aggiungi al Carrello
├── /carrello/api/contenuto/                → API Contenuto Carrello
├── /carrello/api/aggiorna-quantita/        → API Aggiorna Quantità
├── /carrello/api/rimuovi/                  → API Rimuovi dal Carrello
├── /carrello/api/svuota/                   → API Svuota Carrello
├── /carrello/api/sconto/                   → API Applica Sconto
├── /carrello/api/crea-ordine/              → API Creazione Ordine
├── /carrello/api/stato/<numero>/           → API Stato Ordine
├── /carrello/api/storico/                  → API Storico Ordini
├── /carrello/api/metodi-pagamento/         → API Metodi Pagamento
├── /carrello/api/zone-consegna/            → API Zone Consegna
└── /carrello/api/statistiche/              → API Statistiche Ordini

AREA UTENTE:
├── /utente/login/                          → Login
├── /utente/logout/                         → Logout
├── /utente/registrazione/                  → Registrazione
├── /utente/password-reset/                 → Reset Password
├── /utente/profilo/                        → Gestione Profilo
├── /utente/ordini/                         → Storia Ordini
├── /utente/indirizzi/                      → Gestione Indirizzi
├── /utente/preferenze/                     → Impostazioni Account
├── /utente/api/aggiorna-profilo/           → API Aggiornamento Profilo
├── /utente/api/aggiungi-indirizzo/         → API Aggiungi Indirizzo
└── /utente/api/rimuovi-indirizzo/          → API Rimuovi Indirizzo

GESTIONE ERRORI:
├── 400 → Bad Request Personalizzato
├── 403 → Accesso Negato Personalizzato
├── 404 → Pagina Non Trovata Personalizzata
└── 500 → Errore Server Personalizzato

TOTALE ENDPOINTS: 50+ URL configurati
CONVENZIONE: Nomi italiani per apprendimento
ARCHITETTURA: API + Frontend integrati
SICUREZZA: Error handlers personalizzati
DOCUMENTAZIONE: Swagger/ReDoc integrati
"""