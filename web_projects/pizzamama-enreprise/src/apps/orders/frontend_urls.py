# apps/orders/frontend_urls.py
"""
🛒 PIZZAMAMA ENTERPRISE - URL Frontend Ordini
URLs per carrello, checkout, ordini e pagamenti - VERSIONE CON COMMENTI
Convenzione nomi italiani per apprendimento
"""

from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'orders'

urlpatterns = [
    # ========================================
    # PAGINE FRONTEND CARRELLO - ✅ FUNZIONANTI
    # ========================================
    
    # Pagina principale carrello
    path('', views.carrello_view, name='carrello'),
    
    # ========================================
    # API GESTIONE CARRELLO - ✅ FUNZIONANTI
    # ========================================
    
    # API aggiungi al carrello
    path('api/aggiungi/', views.api_aggiungi_al_carrello, name='api_aggiungi'),
    
    # API contenuto carrello
    path('api/contenuto/', views.api_contenuto_carrello, name='api_contenuto'),
    
    # API aggiorna quantità
    path('api/aggiorna-quantita/', views.api_aggiorna_quantita, name='api_aggiorna_quantita'),
    
    # API rimuovi dal carrello
    path('api/rimuovi/', views.api_rimuovi_dal_carrello, name='api_rimuovi'),
    
    # API svuota carrello
    path('api/svuota/', views.api_svuota_carrello, name='api_svuota'),
    
    # API applica codice sconto
    path('api/sconto/', views.api_applica_codice_sconto, name='api_sconto'),
    
    # API crea nuovo ordine
    path('api/crea-ordine/', views.api_crea_ordine, name='api_crea_ordine'),
    
    # API stato ordine specifico
    path('api/stato/<str:numero_ordine>/', views.api_stato_ordine, name='api_stato_ordine'),
    
    # API storico ordini utente
    path('api/storico/', views.api_storico_ordini, name='api_storico'),
    
    # API metodi pagamento disponibili
    path('api/metodi-pagamento/', views.api_metodi_pagamento, name='api_metodi_pagamento'),
    
    # API zone consegna
    path('api/zone-consegna/', views.api_zone_consegna, name='api_zone_consegna'),
    
    # API statistiche ordini
    path('api/statistiche/', views.api_statistiche_ordini, name='api_statistiche'),
    
    # ========================================
    # 🚧 VIEWS DA IMPLEMENTARE PIÙ TARDI
    # ========================================
    # Decommenta queste righe quando implementi le relative views
    
    # Pagina checkout
    # path('checkout/', views.checkout_view, name='checkout'),
    
    # Pagina conferma ordine
    # path('conferma/', views.conferma_ordine_view, name='conferma_ordine'),
    
    # Pagina ordine completato
    # path('completato/<str:numero_ordine>/', views.ordine_completato_view, name='ordine_completato'),
    
    # Pagina tracking ordine
    # path('tracking/<str:numero_ordine>/', views.tracking_ordine_view, name='tracking_ordine'),
    
    # Pagina stampa ricevuta
    # path('ricevuta/<str:numero_ordine>/', views.ricevuta_ordine_view, name='ricevuta_ordine'),
    
    # API salva carrello (per utenti registrati)
    # path('api/carrello/salva/', views.api_salva_carrello, name='api_salva_carrello'),
    
    # API ripristina carrello salvato
    # path('api/carrello/ripristina/', views.api_ripristina_carrello, name='api_ripristina_carrello'),
    
    # API rimuovi sconto
    # path('api/sconto/rimuovi/', views.api_rimuovi_sconto, name='api_rimuovi_sconto'),
    
    # API verifica validità sconto
    # path('api/sconto/verifica/', views.api_verifica_sconto, name='api_verifica_sconto'),
    
    # API sconti disponibili per utente
    # path('api/sconti-disponibili/', views.api_sconti_disponibili, name='api_sconti_disponibili'),
    
    # API tracking ordine in tempo reale
    # path('api/ordini/tracking/<str:numero_ordine>/', views.api_tracking_ordine, name='api_tracking_ordine'),
    
    # API dettagli ordine
    # path('api/ordini/dettagli/<str:numero_ordine>/', views.api_dettagli_ordine, name='api_dettagli_ordine'),
    
    # API annulla ordine
    # path('api/ordini/annulla/<str:numero_ordine>/', views.api_annulla_ordine, name='api_annulla_ordine'),
    
    # API riordina (duplicate ordine precedente)
    # path('api/ordini/riordina/<str:numero_ordine>/', views.api_riordina, name='api_riordina'),
    
    # API valutazione ordine/consegna
    # path('api/ordini/valuta/<str:numero_ordine>/', views.api_valuta_ordine, name='api_valuta_ordine'),
    
    # API avvia pagamento
    # path('api/pagamenti/avvia/', views.api_avvia_pagamento, name='api_avvia_pagamento'),
    
    # API conferma pagamento
    # path('api/pagamenti/conferma/', views.api_conferma_pagamento, name='api_conferma_pagamento'),
    
    # API stato pagamento
    # path('api/pagamenti/stato/<str:id_transazione>/', views.api_stato_pagamento, name='api_stato_pagamento'),
    
    # API rimborso
    # path('api/pagamenti/rimborso/<str:numero_ordine>/', views.api_rimborso, name='api_rimborso'),
    
    # API verifica zona per CAP
    # path('api/consegna/verifica-zona/', views.api_verifica_zona_consegna, name='api_verifica_zona'),
    
    # API calcola costi consegna
    # path('api/consegna/calcola-costi/', views.api_calcola_costi_consegna, name='api_calcola_costi'),
    
    # API slot consegna disponibili
    # path('api/consegna/slot-disponibili/', views.api_slot_consegna, name='api_slot_consegna'),
    
    # API tracking consegnatore in tempo reale
    # path('api/consegna/tracking-live/<str:numero_ordine>/', views.api_tracking_consegnatore, name='api_tracking_consegnatore'),
    
    # API statistiche utente
    # path('api/statistiche/utente/', views.api_statistiche_utente, name='api_statistiche_utente'),
    
    # API tempi di consegna medi
    # path('api/statistiche/tempi-consegna/', views.api_tempi_consegna, name='api_tempi_consegna'),
    
    # API prodotti più ordinati
    # path('api/statistiche/prodotti-popolari/', views.api_prodotti_popolari_ordini, name='api_prodotti_popolari'),
    
    # Lista ordini utente
    # path('i-miei-ordini/', views.lista_ordini_utente_view, name='lista_ordini_utente'),
    
    # Dettaglio ordine utente
    # path('ordine/<str:numero_ordine>/', views.dettaglio_ordine_utente_view, name='dettaglio_ordine_utente'),
    
    # Pagina riordina
    # path('riordina/<str:numero_ordine>/', views.riordina_view, name='riordina'),
    
    # Pagina tracking live
    # path('live/<str:numero_ordine>/', views.tracking_live_view, name='tracking_live'),
    
    # Pagina carrello salvato
    # path('carrelli-salvati/', views.carrelli_salvati_view, name='carrelli_salvati'),
    
    # Pagina ordini frequenti
    # path('ordini-frequenti/', views.ordini_frequenti_view, name='ordini_frequenti'),
    
    # Pagina calcola consegna
    # path('calcola-consegna/', views.calcola_consegna_view, name='calcola_consegna'),
    
    # Pagina gruppi ordine (ordini condivisi)
    # path('gruppo-ordine/', views.gruppo_ordine_view, name='gruppo_ordine'),
    # path('gruppo-ordine/<str:codice_gruppo>/', views.gestisci_gruppo_ordine_view, name='gestisci_gruppo_ordine'),
    
    # Webhook pagamenti (PayPal, Stripe, etc.)
    # path('webhook/pagamento/<str:provider>/', views.webhook_pagamento, name='webhook_pagamento'),
    
    # Webhook tracking consegna
    # path('webhook/tracking/', views.webhook_tracking, name='webhook_tracking'),
    
    # API notifiche push
    # path('api/notifiche/registra-device/', views.api_registra_device_notifiche, name='api_registra_device'),
    # path('api/notifiche/aggiorna-stato/', views.api_aggiorna_stato_notifiche, name='api_aggiorna_notifiche'),
    
    # Export storico ordini PDF
    # path('export/storico-pdf/', views.export_storico_ordini_pdf, name='export_storico_pdf'),
    
    # Export ricevuta fiscale
    # path('export/ricevuta/<str:numero_ordine>/', views.export_ricevuta_fiscale, name='export_ricevuta'),
    
    # API dati per report utente
    # path('api/report/dati-utente/', views.api_dati_report_utente, name='api_report_utente'),
    
    # ========================================
    # 📄 PAGINE PLACEHOLDER TEMPORANEE (opzionali)
    # ========================================
    # Puoi usare queste per testare gli URL senza implementare le views
    
    # Pagina checkout (placeholder)
    path('checkout/', TemplateView.as_view(
        template_name='carrello/checkout.html',
        extra_context={'titolo_pagina': 'Checkout - PizzaMama'}
    ), name='checkout'),
    
    # Pagina conferma ordine (placeholder)
    path('conferma/', TemplateView.as_view(
        template_name='carrello/conferma.html',
        extra_context={'titolo_pagina': 'Conferma Ordine - PizzaMama'}
    ), name='conferma_ordine'),
    
    # Pagina ordine completato (placeholder)
    path('completato/<str:numero_ordine>/', TemplateView.as_view(
        template_name='carrello/completato.html',
        extra_context={'titolo_pagina': 'Ordine Completato - PizzaMama'}
    ), name='ordine_completato'),
    
    # Pagina tracking ordine (placeholder)
    path('tracking/<str:numero_ordine>/', TemplateView.as_view(
        template_name='carrello/tracking.html',
        extra_context={'titolo_pagina': 'Tracking Ordine - PizzaMama'}
    ), name='tracking_ordine'),
    
    # Pagina stampa ricevuta (placeholder)
    path('ricevuta/<str:numero_ordine>/', TemplateView.as_view(
        template_name='carrello/ricevuta.html',
        extra_context={'titolo_pagina': 'Ricevuta - PizzaMama'}
    ), name='ricevuta_ordine'),
    
    # Lista ordini utente (placeholder)
    path('i-miei-ordini/', TemplateView.as_view(
        template_name='carrello/lista_ordini.html',
        extra_context={'titolo_pagina': 'I Miei Ordini - PizzaMama'}
    ), name='lista_ordini_utente'),
    
    # Dettaglio ordine utente (placeholder)
    path('ordine/<str:numero_ordine>/', TemplateView.as_view(
        template_name='carrello/dettaglio_ordine.html',
        extra_context={'titolo_pagina': 'Dettaglio Ordine - PizzaMama'}
    ), name='dettaglio_ordine_utente'),
    
    # Pagina riordina (placeholder)
    path('riordina/<str:numero_ordine>/', TemplateView.as_view(
        template_name='carrello/riordina.html',
        extra_context={'titolo_pagina': 'Riordina - PizzaMama'}
    ), name='riordina'),
    
    # Pagina tracking live (placeholder)
    path('live/<str:numero_ordine>/', TemplateView.as_view(
        template_name='carrello/tracking_live.html',
        extra_context={'titolo_pagina': 'Tracking Live - PizzaMama'}
    ), name='tracking_live'),
    
    # Pagina carrello salvato (placeholder)
    path('carrelli-salvati/', TemplateView.as_view(
        template_name='carrello/carrelli_salvati.html',
        extra_context={'titolo_pagina': 'Carrelli Salvati - PizzaMama'}
    ), name='carrelli_salvati'),
    
    # Pagina ordini frequenti (placeholder)
    path('ordini-frequenti/', TemplateView.as_view(
        template_name='carrello/ordini_frequenti.html',
        extra_context={'titolo_pagina': 'Ordini Frequenti - PizzaMama'}
    ), name='ordini_frequenti'),
    
    # Pagina calcola consegna (placeholder)
    path('calcola-consegna/', TemplateView.as_view(
        template_name='carrello/calcola_consegna.html',
        extra_context={'titolo_pagina': 'Calcola Consegna - PizzaMama'}
    ), name='calcola_consegna'),
    
    # Pagina gruppi ordine (placeholder)
    path('gruppo-ordine/', TemplateView.as_view(
        template_name='carrello/gruppo_ordine.html',
        extra_context={'titolo_pagina': 'Gruppo Ordine - PizzaMama'}
    ), name='gruppo_ordine'),
    
    path('gruppo-ordine/<str:codice_gruppo>/', TemplateView.as_view(
        template_name='carrello/gestisci_gruppo.html',
        extra_context={'titolo_pagina': 'Gestisci Gruppo - PizzaMama'}
    ), name='gestisci_gruppo_ordine'),
]

# ========================================
# 🚧 URL PATTERNS CHECKOUT MULTISTEP - DA IMPLEMENTARE PIÙ TARDI
# ========================================
# Decommenta questa sezione quando implementi le relative views

# checkout_patterns = [
#     path('checkout/step-1/', views.checkout_step1_view, name='checkout_step1'),  # Carrello review
#     path('checkout/step-2/', views.checkout_step2_view, name='checkout_step2'),  # Dati consegna  
#     path('checkout/step-3/', views.checkout_step3_view, name='checkout_step3'),  # Pagamento
#     path('checkout/step-4/', views.checkout_step4_view, name='checkout_step4'),  # Conferma
# ]

# 📄 Pattern checkout multistep con placeholder temporanei
checkout_patterns_placeholder = [
    path('checkout/step-1/', TemplateView.as_view(
        template_name='carrello/checkout_step1.html',
        extra_context={'titolo_pagina': 'Checkout Step 1 - PizzaMama'}
    ), name='checkout_step1'),
    
    path('checkout/step-2/', TemplateView.as_view(
        template_name='carrello/checkout_step2.html',
        extra_context={'titolo_pagina': 'Checkout Step 2 - PizzaMama'}
    ), name='checkout_step2'),
    
    path('checkout/step-3/', TemplateView.as_view(
        template_name='carrello/checkout_step3.html',
        extra_context={'titolo_pagina': 'Checkout Step 3 - PizzaMama'}
    ), name='checkout_step3'),
    
    path('checkout/step-4/', TemplateView.as_view(
        template_name='carrello/checkout_step4.html',
        extra_context={'titolo_pagina': 'Checkout Step 4 - PizzaMama'}
    ), name='checkout_step4'),
]

# Aggiungi pattern checkout placeholder agli urlpatterns principali
urlpatterns.extend(checkout_patterns_placeholder)

# ========================================
# 🚧 URL PATTERNS GUEST CHECKOUT - DA IMPLEMENTARE PIÙ TARDI
# ========================================
# Decommenta questa sezione quando implementi le relative views

# guest_patterns = [
#     path('guest/checkout/', views.guest_checkout_view, name='guest_checkout'),
#     path('guest/tracking/<str:tracking_code>/', views.guest_tracking_view, name='guest_tracking'),
#     path('guest/ricevuta/<str:tracking_code>/', views.guest_ricevuta_view, name='guest_ricevuta'),
# ]

# 📄 Pattern guest checkout con placeholder temporanei
guest_patterns_placeholder = [
    path('guest/checkout/', TemplateView.as_view(
        template_name='carrello/guest_checkout.html',
        extra_context={'titolo_pagina': 'Guest Checkout - PizzaMama'}
    ), name='guest_checkout'),
    
    path('guest/tracking/<str:tracking_code>/', TemplateView.as_view(
        template_name='carrello/guest_tracking.html',
        extra_context={'titolo_pagina': 'Guest Tracking - PizzaMama'}
    ), name='guest_tracking'),
    
    path('guest/ricevuta/<str:tracking_code>/', TemplateView.as_view(
        template_name='carrello/guest_ricevuta.html',
        extra_context={'titolo_pagina': 'Guest Ricevuta - PizzaMama'}
    ), name='guest_ricevuta'),
]

# Aggiungi pattern guest placeholder
urlpatterns.extend(guest_patterns_placeholder)

# ========================================
# METADATI URL CONFIGURATION
# ========================================

URL_METADATA = {
    'app_name': 'orders',
    'namespace': 'ordini',
    'total_patterns': len(urlpatterns),
    'views_implementate': 12,    # Views che esistono e funzionano
    'views_da_implementare': 40, # Views commentate da implementare
    'placeholder_attivi': 15,    # TemplateView placeholder attivi
    'stato': 'Sviluppo - Solo views base implementate',
    'note': 'La maggior parte delle views sono commentate o placeholder'
}

# ========================================
# 📝 ISTRUZIONI PER SVILUPPO FUTURO
# ========================================

"""
COME CONTINUARE LO SVILUPPO:

1. VIEWS PRIORITARIE DA IMPLEMENTARE:
   ✅ carrello_view (già fatto)
   ✅ api_aggiungi_al_carrello (già fatto)
   ✅ api_contenuto_carrello (già fatto)
   ✅ api_aggiorna_quantita (già fatto)
   ✅ api_rimuovi_dal_carrello (già fatto)
   ✅ api_svuota_carrello (già fatto)
   ✅ api_applica_codice_sconto (già fatto)
   ✅ api_crea_ordine (già fatto)
   ✅ api_stato_ordine (già fatto)
   ✅ api_storico_ordini (già fatto)
   ✅ api_metodi_pagamento (già fatto)
   ✅ api_zone_consegna (già fatto)
   ✅ api_statistiche_ordini (già fatto)
   🚧 checkout_view (da implementare)
   🚧 conferma_ordine_view (da implementare)
   🚧 tracking_ordine_view (da implementare)

2. API PRIORITARIE DA IMPLEMENTARE:
   🚧 api_salva_carrello (per utenti registrati)
   🚧 api_ripristina_carrello (carrelli salvati)
   🚧 api_rimuovi_sconto (gestione sconti avanzata)
   🚧 api_verifica_sconto (validazione sconti)
   🚧 api_tracking_ordine (tracking tempo reale)
   🚧 api_dettagli_ordine (dettagli completi)
   🚧 api_annulla_ordine (cancellazione ordini)

3. FUNZIONALITÀ AVANZATE DA IMPLEMENTARE:
   🚧 checkout_multistep (4 step)
   🚧 guest_checkout (senza registrazione)
   🚧 sistema_pagamenti (integrazione gateway)
   🚧 tracking_gps (tempo reale)
   🚧 webhook_integrations (PayPal, Stripe)
   🚧 export_fiscali (PDF ricevute)
   🚧 notifiche_push (aggiornamenti ordini)

4. PROCESSO DI IMPLEMENTAZIONE:
   - Scegli una view da implementare
   - Decommentala nella sezione "🚧 VIEWS DA IMPLEMENTARE PIÙ TARDI"
   - Commenta la corrispondente TemplateView placeholder
   - Implementa la view in views.py
   - Crea il template necessario
   - Testa la funzionalità

5. TEMPLATE DA CREARE (quando necessari):
   - templates/carrello/checkout.html
   - templates/carrello/conferma.html
   - templates/carrello/completato.html
   - templates/carrello/tracking.html
   - templates/carrello/ricevuta.html
   - templates/carrello/lista_ordini.html
   - templates/carrello/dettaglio_ordine.html
   - templates/carrello/riordina.html
   - templates/carrello/tracking_live.html
   - templates/carrello/carrelli_salvati.html
   - templates/carrello/ordini_frequenti.html
   - templates/carrello/calcola_consegna.html
   - templates/carrello/gruppo_ordine.html
   - templates/carrello/checkout_step1.html
   - templates/carrello/checkout_step2.html
   - templates/carrello/checkout_step3.html
   - templates/carrello/checkout_step4.html
   - templates/carrello/guest_checkout.html
   - templates/carrello/guest_tracking.html
   - templates/carrello/guest_ricevuta.html

ORDINE DI SVILUPPO SUGGERITO:
1. Completare checkout base (checkout_view)
2. Implementare tracking ordini (tracking_ordine_view)
3. Aggiungere gestione avanzata sconti
4. Sviluppare sistema pagamenti
5. Implementare checkout multistep
6. Aggiungere guest checkout
7. Integrare tracking GPS
8. Sviluppare webhook e notifiche
9. Implementare export e report
10. Aggiungere funzionalità gruppi ordine

STATO ATTUALE:
✅ Server funzionante con views base carrello
✅ API core e-commerce implementate
📄 Placeholder per tutte le pagine avanzate
🚧 Sviluppo graduale possibile
🎯 Sistema e-commerce enterprise quasi completo
"""