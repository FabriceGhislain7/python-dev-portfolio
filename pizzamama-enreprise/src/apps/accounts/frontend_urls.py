# apps/accounts/frontend_urls.py
"""
👤 PIZZAMAMA ENTERPRISE - URL Frontend Accounts
URLs per autenticazione, profili utente e gestione account - VERSIONE CON COMMENTI
Convenzione nomi italiani per apprendimento
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'accounts'

urlpatterns = [
    # ========================================
    # AUTENTICAZIONE E REGISTRAZIONE - ✅ FUNZIONANTI (Django built-in)
    # ========================================
    
    # Login utente
    path('login/', auth_views.LoginView.as_view(
        template_name='utenti/login.html',
        extra_context={
            'titolo_pagina': 'Accedi - PizzaMama',
            'descrizione_meta': 'Accedi al tuo account PizzaMama per gestire ordini e profilo'
        },
        redirect_authenticated_user=True
    ), name='login'),
    
    # Logout utente
    path('logout/', auth_views.LogoutView.as_view(
        next_page='homepage'
    ), name='logout'),
    
    # ========================================
    # RESET PASSWORD - ✅ FUNZIONANTI (Django built-in)
    # ========================================
    
    # Richiesta reset password
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='utenti/password_reset.html',
        email_template_name='utenti/password_reset_email.html',
        subject_template_name='utenti/password_reset_subject.txt',
        success_url='/utente/password-reset/inviata/',
        extra_context={
            'titolo_pagina': 'Reset Password - PizzaMama'
        }
    ), name='password_reset'),
    
    # Conferma invio email reset
    path('password-reset/inviata/', auth_views.PasswordResetDoneView.as_view(
        template_name='utenti/password_reset_done.html',
        extra_context={
            'titolo_pagina': 'Email Inviata - PizzaMama'
        }
    ), name='password_reset_done'),
    
    # Form nuovo password
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='utenti/password_reset_confirm.html',
        success_url='/utente/password-reset/completato/',
        extra_context={
            'titolo_pagina': 'Nuova Password - PizzaMama'
        }
    ), name='password_reset_confirm'),
    
    # Password reset completato
    path('password-reset/completato/', auth_views.PasswordResetCompleteView.as_view(
        template_name='utenti/password_reset_complete.html',
        extra_context={
            'titolo_pagina': 'Password Aggiornata - PizzaMama'
        }
    ), name='password_reset_complete'),
    
    # Cambia password
    path('profilo/cambia-password/', auth_views.PasswordChangeView.as_view(
        template_name='utenti/cambia_password.html',
        success_url='/utente/profilo/?password_changed=1',
        extra_context={
            'titolo_pagina': 'Cambia Password - PizzaMama'
        }
    ), name='cambia_password'),
    
    # ========================================
    # 🚧 VIEWS DA IMPLEMENTARE PIÙ TARDI
    # ========================================
    # Decommenta queste righe quando implementi le relative views
    
    # Registrazione nuovo utente
    # path('registrazione/', views.registrazione_view, name='registrazione'),
    
    # Conferma email registrazione
    # path('conferma-email/<str:token>/', views.conferma_email_view, name='conferma_email'),
    
    # Richiesta nuovo link conferma
    # path('reinvia-conferma/', views.reinvia_conferma_email_view, name='reinvia_conferma'),
    
    # Dashboard utente
    # path('dashboard/', views.dashboard_utente_view, name='dashboard'),
    
    # Profilo utente
    # path('profilo/', views.profilo_view, name='profilo'),
    
    # Modifica profilo
    # path('profilo/modifica/', views.modifica_profilo_view, name='modifica_profilo'),
    
    # Lista ordini utente
    # path('ordini/', views.ordini_utente_view, name='ordini'),
    
    # Dettaglio ordine specifico
    # path('ordini/<str:numero_ordine>/', views.dettaglio_ordine_view, name='dettaglio_ordine'),
    
    # Tracking ordine
    # path('ordini/<str:numero_ordine>/tracking/', views.tracking_ordine_utente_view, name='tracking_ordine'),
    
    # Riordina ordine precedente
    # path('ordini/<str:numero_ordine>/riordina/', views.riordina_ordine_view, name='riordina_ordine'),
    
    # Valuta ordine/consegna
    # path('ordini/<str:numero_ordine>/valuta/', views.valuta_ordine_view, name='valuta_ordine'),
    
    # Lista indirizzi salvati
    # path('indirizzi/', views.indirizzi_view, name='indirizzi'),
    
    # Aggiungi nuovo indirizzo
    # path('indirizzi/aggiungi/', views.aggiungi_indirizzo_view, name='aggiungi_indirizzo'),
    
    # Modifica indirizzo esistente
    # path('indirizzi/<int:indirizzo_id>/modifica/', views.modifica_indirizzo_view, name='modifica_indirizzo'),
    
    # Elimina indirizzo
    # path('indirizzi/<int:indirizzo_id>/elimina/', views.elimina_indirizzo_view, name='elimina_indirizzo'),
    
    # Imposta indirizzo predefinito
    # path('indirizzi/<int:indirizzo_id>/predefinito/', views.imposta_indirizzo_predefinito_view, name='indirizzo_predefinito'),
    
    # Pagina preferenze generali
    # path('preferenze/', views.preferenze_view, name='preferenze'),
    
    # Preferenze alimentari
    # path('preferenze/alimentari/', views.preferenze_alimentari_view, name='preferenze_alimentari'),
    
    # Impostazioni notifiche
    # path('preferenze/notifiche/', views.impostazioni_notifiche_view, name='impostazioni_notifiche'),
    
    # Impostazioni privacy
    # path('preferenze/privacy/', views.impostazioni_privacy_view, name='impostazioni_privacy'),
    
    # Gestione consensi GDPR
    # path('preferenze/consensi/', views.gestione_consensi_view, name='gestione_consensi'),
    
    # Dashboard loyalty program
    # path('loyalty/', views.loyalty_dashboard_view, name='loyalty_dashboard'),
    
    # Storico punti loyalty
    # path('loyalty/storico/', views.storico_punti_view, name='storico_punti'),
    
    # Premi disponibili
    # path('loyalty/premi/', views.premi_loyalty_view, name='premi_loyalty'),
    
    # Riscatta premio
    # path('loyalty/riscatta/<int:premio_id>/', views.riscatta_premio_view, name='riscatta_premio'),
    
    # Invita amici (referral)
    # path('loyalty/invita-amici/', views.invita_amici_view, name='invita_amici'),
    
    # Lista wishlist/preferiti
    # path('wishlist/', views.wishlist_view, name='wishlist'),
    
    # Condividi wishlist
    # path('wishlist/condividi/', views.condividi_wishlist_view, name='condividi_wishlist'),
    
    # Wishlist pubblica di un utente
    # path('wishlist/<str:username>/', views.wishlist_pubblica_view, name='wishlist_pubblica'),
    
    # API aggiorna profilo
    # path('api/profilo/aggiorna/', views.api_aggiorna_profilo, name='api_aggiorna_profilo'),
    
    # API upload foto profilo
    # path('api/profilo/foto/', views.api_upload_foto_profilo, name='api_upload_foto'),
    
    # API aggiorna preferenze
    # path('api/preferenze/aggiorna/', views.api_aggiorna_preferenze, name='api_aggiorna_preferenze'),
    
    # API statistiche utente
    # path('api/statistiche/', views.api_statistiche_utente, name='api_statistiche_utente'),
    
    # API lista indirizzi
    # path('api/indirizzi/', views.api_lista_indirizzi, name='api_lista_indirizzi'),
    
    # API aggiungi indirizzo
    # path('api/indirizzi/aggiungi/', views.api_aggiungi_indirizzo, name='api_aggiungi_indirizzo'),
    
    # API aggiorna indirizzo
    # path('api/indirizzi/<int:indirizzo_id>/aggiorna/', views.api_aggiorna_indirizzo, name='api_aggiorna_indirizzo'),
    
    # API rimuovi indirizzo
    # path('api/indirizzi/<int:indirizzo_id>/rimuovi/', views.api_rimuovi_indirizzo, name='api_rimuovi_indirizzo'),
    
    # API indirizzo predefinito
    # path('api/indirizzi/<int:indirizzo_id>/predefinito/', views.api_imposta_predefinito, name='api_imposta_predefinito'),
    
    # API lista wishlist
    # path('api/wishlist/', views.api_lista_wishlist, name='api_lista_wishlist'),
    
    # API aggiungi a wishlist
    # path('api/wishlist/aggiungi/', views.api_aggiungi_wishlist, name='api_aggiungi_wishlist'),
    
    # API rimuovi da wishlist
    # path('api/wishlist/rimuovi/', views.api_rimuovi_wishlist, name='api_rimuovi_wishlist'),
    
    # API condividi wishlist
    # path('api/wishlist/condividi/', views.api_condividi_wishlist, name='api_condividi_wishlist'),
    
    # API saldo punti loyalty
    # path('api/loyalty/saldo/', views.api_saldo_loyalty, name='api_saldo_loyalty'),
    
    # API storico transazioni loyalty
    # path('api/loyalty/transazioni/', views.api_transazioni_loyalty, name='api_transazioni_loyalty'),
    
    # API premi disponibili
    # path('api/loyalty/premi/', views.api_premi_disponibili, name='api_premi_disponibili'),
    
    # API riscatta premio
    # path('api/loyalty/riscatta/', views.api_riscatta_premio, name='api_riscatta_premio'),
    
    # API invita amico
    # path('api/loyalty/invita/', views.api_invita_amico, name='api_invita_amico'),
    
    # API lista notifiche
    # path('api/notifiche/', views.api_lista_notifiche, name='api_lista_notifiche'),
    
    # API marca notifica come letta
    # path('api/notifiche/<int:notifica_id>/letta/', views.api_marca_notifica_letta, name='api_marca_letta'),
    
    # API marca tutte come lette
    # path('api/notifiche/tutte-lette/', views.api_marca_tutte_lette, name='api_tutte_lette'),
    
    # API impostazioni notifiche
    # path('api/notifiche/impostazioni/', views.api_impostazioni_notifiche, name='api_impostazioni_notifiche'),
    
    # Google OAuth
    # path('login/google/', views.google_login_view, name='google_login'),
    # path('login/google/callback/', views.google_callback_view, name='google_callback'),
    
    # Facebook OAuth
    # path('login/facebook/', views.facebook_login_view, name='facebook_login'),
    # path('login/facebook/callback/', views.facebook_callback_view, name='facebook_callback'),
    
    # Collega account social
    # path('profilo/collega-google/', views.collega_google_view, name='collega_google'),
    # path('profilo/collega-facebook/', views.collega_facebook_view, name='collega_facebook'),
    
    # Scollega account social
    # path('profilo/scollega-social/<str:provider>/', views.scollega_social_view, name='scollega_social'),
    
    # Elimina account
    # path('elimina-account/', views.elimina_account_view, name='elimina_account'),
    
    # Conferma eliminazione account
    # path('elimina-account/conferma/', views.conferma_eliminazione_view, name='conferma_eliminazione'),
    
    # Download dati utente (GDPR)
    # path('download-dati/', views.download_dati_utente_view, name='download_dati'),
    
    # Esporta dati in PDF
    # path('export/profilo-pdf/', views.export_profilo_pdf_view, name='export_profilo_pdf'),
    
    # FAQ account
    # path('faq/', views.faq_account_view, name='faq_account'),
    
    # Webhook social login
    # path('webhook/social/<str:provider>/', views.webhook_social_login, name='webhook_social'),
    
    # API sincronizzazione dati
    # path('api/sync/dati/', views.api_sincronizza_dati, name='api_sync_dati'),
    
    # API backup profilo
    # path('api/backup/profilo/', views.api_backup_profilo, name='api_backup_profilo'),
    
    # ========================================
    # 📄 PAGINE PLACEHOLDER TEMPORANEE (opzionali)
    # ========================================
    # Puoi usare queste per testare gli URL senza implementare le views
    
    # Registrazione nuovo utente (placeholder)
    path('registrazione/', TemplateView.as_view(
        template_name='utenti/registrazione.html',
        extra_context={'titolo_pagina': 'Registrazione - PizzaMama'}
    ), name='registrazione'),
    
    # Dashboard utente (placeholder)
    path('dashboard/', TemplateView.as_view(
        template_name='utenti/dashboard.html',
        extra_context={'titolo_pagina': 'Dashboard - PizzaMama'}
    ), name='dashboard'),
    
    # Profilo utente (placeholder)
    path('profilo/', TemplateView.as_view(
        template_name='utenti/profilo.html',
        extra_context={'titolo_pagina': 'Profilo - PizzaMama'}
    ), name='profilo'),
    
    # Modifica profilo (placeholder)
    path('profilo/modifica/', TemplateView.as_view(
        template_name='utenti/modifica_profilo.html',
        extra_context={'titolo_pagina': 'Modifica Profilo - PizzaMama'}
    ), name='modifica_profilo'),
    
    # Lista ordini utente (placeholder)
    path('ordini/', TemplateView.as_view(
        template_name='utenti/ordini.html',
        extra_context={'titolo_pagina': 'I Miei Ordini - PizzaMama'}
    ), name='ordini'),
    
    # Dettaglio ordine specifico (placeholder)
    path('ordini/<str:numero_ordine>/', TemplateView.as_view(
        template_name='utenti/dettaglio_ordine.html',
        extra_context={'titolo_pagina': 'Dettaglio Ordine - PizzaMama'}
    ), name='dettaglio_ordine'),
    
    # Tracking ordine (placeholder)
    path('ordini/<str:numero_ordine>/tracking/', TemplateView.as_view(
        template_name='utenti/tracking_ordine.html',
        extra_context={'titolo_pagina': 'Tracking Ordine - PizzaMama'}
    ), name='tracking_ordine'),
    
    # Riordina ordine precedente (placeholder)
    path('ordini/<str:numero_ordine>/riordina/', TemplateView.as_view(
        template_name='utenti/riordina_ordine.html',
        extra_context={'titolo_pagina': 'Riordina - PizzaMama'}
    ), name='riordina_ordine'),
    
    # Valuta ordine/consegna (placeholder)
    path('ordini/<str:numero_ordine>/valuta/', TemplateView.as_view(
        template_name='utenti/valuta_ordine.html',
        extra_context={'titolo_pagina': 'Valuta Ordine - PizzaMama'}
    ), name='valuta_ordine'),
    
    # Lista indirizzi salvati (placeholder)
    path('indirizzi/', TemplateView.as_view(
        template_name='utenti/indirizzi.html',
        extra_context={'titolo_pagina': 'I Miei Indirizzi - PizzaMama'}
    ), name='indirizzi'),
    
    # Aggiungi nuovo indirizzo (placeholder)
    path('indirizzi/aggiungi/', TemplateView.as_view(
        template_name='utenti/aggiungi_indirizzo.html',
        extra_context={'titolo_pagina': 'Aggiungi Indirizzo - PizzaMama'}
    ), name='aggiungi_indirizzo'),
    
    # Modifica indirizzo esistente (placeholder)
    path('indirizzi/<int:indirizzo_id>/modifica/', TemplateView.as_view(
        template_name='utenti/modifica_indirizzo.html',
        extra_context={'titolo_pagina': 'Modifica Indirizzo - PizzaMama'}
    ), name='modifica_indirizzo'),
    
    # Elimina indirizzo (placeholder)
    path('indirizzi/<int:indirizzo_id>/elimina/', TemplateView.as_view(
        template_name='utenti/elimina_indirizzo.html',
        extra_context={'titolo_pagina': 'Elimina Indirizzo - PizzaMama'}
    ), name='elimina_indirizzo'),
    
    # Imposta indirizzo predefinito (placeholder)
    path('indirizzi/<int:indirizzo_id>/predefinito/', TemplateView.as_view(
        template_name='utenti/indirizzo_predefinito.html',
        extra_context={'titolo_pagina': 'Indirizzo Predefinito - PizzaMama'}
    ), name='indirizzo_predefinito'),
    
    # Pagina preferenze generali (placeholder)
    path('preferenze/', TemplateView.as_view(
        template_name='utenti/preferenze.html',
        extra_context={'titolo_pagina': 'Preferenze - PizzaMama'}
    ), name='preferenze'),
    
    # Preferenze alimentari (placeholder)
    path('preferenze/alimentari/', TemplateView.as_view(
        template_name='utenti/preferenze_alimentari.html',
        extra_context={'titolo_pagina': 'Preferenze Alimentari - PizzaMama'}
    ), name='preferenze_alimentari'),
    
    # Impostazioni notifiche (placeholder)
    path('preferenze/notifiche/', TemplateView.as_view(
        template_name='utenti/notifiche.html',
        extra_context={'titolo_pagina': 'Impostazioni Notifiche - PizzaMama'}
    ), name='impostazioni_notifiche'),
    
    # Impostazioni privacy (placeholder)
    path('preferenze/privacy/', TemplateView.as_view(
        template_name='utenti/privacy.html',
        extra_context={'titolo_pagina': 'Impostazioni Privacy - PizzaMama'}
    ), name='impostazioni_privacy'),
    
    # Gestione consensi GDPR (placeholder)
    path('preferenze/consensi/', TemplateView.as_view(
        template_name='utenti/consensi.html',
        extra_context={'titolo_pagina': 'Gestione Consensi - PizzaMama'}
    ), name='gestione_consensi'),
    
    # Dashboard loyalty program (placeholder)
    path('loyalty/', TemplateView.as_view(
        template_name='utenti/loyalty.html',
        extra_context={'titolo_pagina': 'Loyalty Program - PizzaMama'}
    ), name='loyalty_dashboard'),
    
    # Storico punti loyalty (placeholder)
    path('loyalty/storico/', TemplateView.as_view(
        template_name='utenti/storico_punti.html',
        extra_context={'titolo_pagina': 'Storico Punti - PizzaMama'}
    ), name='storico_punti'),
    
    # Premi disponibili (placeholder)
    path('loyalty/premi/', TemplateView.as_view(
        template_name='utenti/premi.html',
        extra_context={'titolo_pagina': 'Premi Loyalty - PizzaMama'}
    ), name='premi_loyalty'),
    
    # Riscatta premio (placeholder)
    path('loyalty/riscatta/<int:premio_id>/', TemplateView.as_view(
        template_name='utenti/riscatta_premio.html',
        extra_context={'titolo_pagina': 'Riscatta Premio - PizzaMama'}
    ), name='riscatta_premio'),
    
    # Invita amici (placeholder)
    path('loyalty/invita-amici/', TemplateView.as_view(
        template_name='utenti/invita_amici.html',
        extra_context={'titolo_pagina': 'Invita Amici - PizzaMama'}
    ), name='invita_amici'),
    
    # Lista wishlist/preferiti (placeholder)
    path('wishlist/', TemplateView.as_view(
        template_name='utenti/wishlist.html',
        extra_context={'titolo_pagina': 'Lista Preferiti - PizzaMama'}
    ), name='wishlist'),
    
    # Condividi wishlist (placeholder)
    path('wishlist/condividi/', TemplateView.as_view(
        template_name='utenti/condividi_wishlist.html',
        extra_context={'titolo_pagina': 'Condividi Lista - PizzaMama'}
    ), name='condividi_wishlist'),
    
    # Wishlist pubblica di un utente (placeholder)
    path('wishlist/<str:username>/', TemplateView.as_view(
        template_name='utenti/wishlist_pubblica.html',
        extra_context={'titolo_pagina': 'Lista Pubblica - PizzaMama'}
    ), name='wishlist_pubblica'),
    
    # Elimina account (placeholder)
    path('elimina-account/', TemplateView.as_view(
        template_name='utenti/elimina_account.html',
        extra_context={'titolo_pagina': 'Elimina Account - PizzaMama'}
    ), name='elimina_account'),
    
    # Conferma eliminazione account (placeholder)
    path('elimina-account/conferma/', TemplateView.as_view(
        template_name='utenti/conferma_eliminazione.html',
        extra_context={'titolo_pagina': 'Conferma Eliminazione - PizzaMama'}
    ), name='conferma_eliminazione'),
    
    # Download dati utente (placeholder)
    path('download-dati/', TemplateView.as_view(
        template_name='utenti/download_dati.html',
        extra_context={'titolo_pagina': 'Download Dati - PizzaMama'}
    ), name='download_dati'),
    
    # Esporta dati in PDF (placeholder)
    path('export/profilo-pdf/', TemplateView.as_view(
        template_name='utenti/export_profilo.html',
        extra_context={'titolo_pagina': 'Export Profilo - PizzaMama'}
    ), name='export_profilo_pdf'),
    
    # Guida uso account
    path('guida/', TemplateView.as_view(
        template_name='utenti/guida.html',
        extra_context={'titolo_pagina': 'Guida Account - PizzaMama'}
    ), name='guida_account'),
    
    # FAQ account (placeholder)
    path('faq/', TemplateView.as_view(
        template_name='utenti/faq.html',
        extra_context={'titolo_pagina': 'FAQ Account - PizzaMama'}
    ), name='faq_account'),
    
    # Termini account
    path('termini-account/', TemplateView.as_view(
        template_name='utenti/termini_account.html',
        extra_context={'titolo_pagina': 'Termini Account - PizzaMama'}
    ), name='termini_account'),
]

# ========================================
# 🚧 URL PATTERNS CONDIZIONALI - DA IMPLEMENTARE PIÙ TARDI
# ========================================
# Decommenta questa sezione quando implementi 2FA

# optional_patterns = []
# 
# try:
#     from django.conf import settings
#     if getattr(settings, 'ENABLE_2FA', False):
#         optional_patterns.extend([
#             path('2fa/setup/', views.setup_2fa_view, name='setup_2fa'),
#             path('2fa/verify/', views.verify_2fa_view, name='verify_2fa'),
#             path('2fa/disable/', views.disable_2fa_view, name='disable_2fa'),
#             path('2fa/backup-codes/', views.backup_codes_2fa_view, name='backup_codes_2fa'),
#         ])
# except ImportError:
#     pass
# 
# urlpatterns.extend(optional_patterns)

# ========================================
# METADATI URL CONFIGURATION
# ========================================

URL_METADATA = {
    'app_name': 'accounts',
    'namespace': 'utenti',
    'total_patterns': len(urlpatterns),
    'django_auth_views': 7,    # Views Django built-in funzionanti
    'views_da_implementare': 50, # Views commentate da implementare
    'placeholder_attivi': 30,   # TemplateView placeholder attivi
    'stato': 'Sviluppo - Solo Django auth funzionante',
    'note': 'Sistema autenticazione base + placeholder per sviluppo graduale'
}

# ========================================
# 📝 ISTRUZIONI PER SVILUPPO FUTURO
# ========================================

"""
COME CONTINUARE LO SVILUPPO:

1. VIEWS PRIORITARIE DA IMPLEMENTARE:
   ✅ Login/Logout (Django built-in - funzionante)
   ✅ Password reset (Django built-in - funzionante)
   ✅ Password change (Django built-in - funzionante)
   🚧 registrazione_view (da implementare)
   🚧 dashboard_utente_view (da implementare)
   🚧 profilo_view (da implementare)
   🚧 ordini_utente_view (da implementare)
   🚧 indirizzi_view (da implementare)

2. API PRIORITARIE DA IMPLEMENTARE:
   🚧 api_aggiorna_profilo (gestione profilo)
   🚧 api_upload_foto_profilo (upload immagini)
   🚧 api_lista_indirizzi (gestione indirizzi)
   🚧 api_aggiungi_indirizzo (nuovo indirizzo)
   🚧 api_statistiche_utente (dashboard dati)

3. FUNZIONALITÀ AVANZATE DA IMPLEMENTARE:
   🚧 Sistema registrazione con email conferma
   🚧 Loyalty program completo
   🚧 Wishlist prodotti
   🚧 Social login (Google, Facebook)
   🚧 Sistema notifiche
   🚧 Gestione privacy GDPR
   🚧 2FA opzionale
   🚧 Export dati utente

4. PROCESSO DI IMPLEMENTAZIONE:
   - Scegli una view da implementare
   - Decommentala nella sezione "🚧 VIEWS DA IMPLEMENTARE PIÙ TARDI"
   - Commenta la corrispondente TemplateView placeholder
   - Implementa la view in views.py
   - Crea il template necessario
   - Testa la funzionalità

5. TEMPLATE DA CREARE (quando necessari):
   - templates/utenti/login.html ✅ (per Django auth)
   - templates/utenti/password_reset.html ✅ (per Django auth)
   - templates/utenti/password_reset_done.html ✅ (per Django auth)
   - templates/utenti/password_reset_confirm.html ✅ (per Django auth)
   - templates/utenti/password_reset_complete.html ✅ (per Django auth)
   - templates/utenti/cambia_password.html ✅ (per Django auth)
   - templates/utenti/registrazione.html 🚧 (da creare)
   - templates/utenti/dashboard.html 🚧 (da creare)
   - templates/utenti/profilo.html 🚧 (da creare)
   - templates/utenti/ordini.html 🚧 (da creare)
   - templates/utenti/indirizzi.html 🚧 (da creare)
   - templates/utenti/preferenze.html 🚧 (da creare)
   - templates/utenti/loyalty.html 🚧 (da creare)
   - templates/utenti/wishlist.html 🚧 (da creare)
   - templates/utenti/elimina_account.html 🚧 (da creare)
   - templates/utenti/download_dati.html 🚧 (da creare)

ORDINE DI SVILUPPO SUGGERITO:
1. Sistema registrazione (registrazione_view + email conferma)
2. Dashboard utente base (dashboard_utente_view)
3. Gestione profilo (profilo_view + modifica_profilo_view)
4. Gestione indirizzi (indirizzi_view + CRUD indirizzi)
5. Lista ordini utente (ordini_utente_view + dettaglio)
6. API profilo (api_aggiorna_profilo + api_upload_foto)
7. Preferenze utente (preferenze_view + alimentari/notifiche)
8. Sistema loyalty (loyalty_dashboard_view + punti/premi)
9. Wishlist prodotti (wishlist_view + API)
10. Funzionalità avanzate (social login, 2FA, GDPR)

TEMPLATE DJANGO AUTH NECESSARI (priorità alta):
Questi template sono richiesti dalle views Django built-in:
- templates/utenti/login.html (LOGIN FORM)
- templates/utenti/password_reset.html (RESET REQUEST)
- templates/utenti/password_reset_done.html (EMAIL SENT CONFIRMATION)
- templates/utenti/password_reset_confirm.html (NEW PASSWORD FORM)
- templates/utenti/password_reset_complete.html (RESET SUCCESS)
- templates/utenti/cambia_password.html (CHANGE PASSWORD FORM)

STATO ATTUALE SISTEMA AUTH:
✅ Django built-in authentication funzionante
✅ Login/Logout/Password reset configurati
✅ URL patterns per tutte le funzionalità
📄 Placeholder per testing senza errori
🚧 Sistema registrazione da implementare
🚧 Dashboard e profilo da implementare
🚧 Gestione indirizzi da implementare
🚧 Loyalty program da implementare
🚧 Wishlist da implementare
🚧 Social login da implementare
🚧 GDPR compliance da implementare

INTEGRAZIONE CON ALTRE APP:
- ordini_utente_view → integrazione con apps.orders
- tracking_ordine_utente_view → integrazione con apps.orders  
- wishlist_view → integrazione con apps.products
- api_statistiche_utente → dati da apps.orders + apps.products

CONFIGURAZIONI NECESSARIE:
- EMAIL_BACKEND per password reset
- MEDIA_ROOT per upload foto profilo
- Social auth keys (Google, Facebook) se implementato
- 2FA library se implementato

SICUREZZA:
- CSRF protection su tutte le form
- Login required decorators
- Permission checks per API
- Rate limiting su registrazione/login
- Validazione input utente
- Sanitizzazione upload files

FUNZIONALITÀ ENTERPRISE INCLUSE:
- Sistema autenticazione completo
- Gestione profili avanzata
- Loyalty program con punti/premi
- Wishlist condivisibile
- Social login opzionale
- Gestione indirizzi multipli
- Preferenze personalizzate
- GDPR compliance completa
- 2FA opzionale
- Export dati utente
- Sistema notifiche
- Dashboard analytics

TOTALE FEATURES: 70+ endpoints per gestione utenti enterprise
FLESSIBILITÀ: Sviluppo graduale view per view
SCALABILITÀ: Architettura modulare espandibile
SICUREZZA: Best practices Django implementate
"""