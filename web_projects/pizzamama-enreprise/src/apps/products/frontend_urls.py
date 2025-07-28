# apps/products/frontend_urls.py
"""
🍕 PIZZAMAMA ENTERPRISE - URL Frontend Prodotti
URLs per pagine frontend e API del catalogo prodotti
Convenzione nomi italiani per apprendimento
"""

from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'products'

urlpatterns = [
    # ========================================
    # PAGINE FRONTEND CATALOGO - ✅ FUNZIONANTI
    # ========================================
    
    # Pagina principale catalogo
    path('', views.catalogo_view, name='catalogo'),
    
    # Dettaglio singola pizza
    path('pizza/<int:pizza_id>/', views.dettaglio_pizza_view, name='dettaglio_pizza'),
    
    # ========================================
    # API FRONTEND CATALOGO - ✅ FUNZIONANTI
    # ========================================
    
    # API ricerca prodotti con filtri
    path('api/ricerca/', views.api_ricerca_prodotti, name='api_ricerca'),
    
    # API suggerimenti ricerca (autocomplete)
    path('api/suggerimenti/', views.api_suggerimenti_ricerca, name='api_suggerimenti'),
    
    # API categorie disponibili
    path('api/categorie/', views.api_categorie_prodotti, name='api_categorie'),
    
    # API ingredienti disponibili
    path('api/ingredienti/', views.api_ingredienti_disponibili, name='api_ingredienti'),
    
    # API pizze popolari/in evidenza
    path('api/popolari/', views.api_pizze_popolari, name='api_popolari'),
    
    # API valutazione prodotto
    path('api/valutazione/', views.api_valutazione_prodotto, name='api_valutazione'),
    
    # API statistiche catalogo
    path('api/statistiche/', views.api_statistiche_catalogo, name='api_statistiche'),
    
    # ========================================
    # 🚧 VIEWS DA IMPLEMENTARE PIÙ TARDI
    # ========================================
    # Decommenta queste righe quando implementi le relative views
    
    # Pagina categoria specifica
    # path('categoria/<slug:categoria_slug>/', views.categoria_view, name='categoria'),
    
    # Pagina ricerca avanzata
    # path('ricerca/', views.ricerca_avanzata_view, name='ricerca_avanzata'),
    
    # Pagina confronto pizze
    # path('confronta/', views.confronta_pizze_view, name='confronta_pizze'),
    
    # Pagina ingredienti
    # path('ingredienti/', views.ingredienti_view, name='ingredienti'),
    
    # API pizze del giorno/offerte speciali
    # path('api/del-giorno/', views.api_pizze_del_giorno, name='api_pizze_del_giorno'),
    
    # API recensioni prodotto
    # path('api/recensioni/<int:pizza_id>/', views.api_recensioni_prodotto, name='api_recensioni'),
    
    # API filtri dinamici
    # path('api/filtri/', views.api_filtri_disponibili, name='api_filtri'),
    
    # API prodotti correlati
    # path('api/correlati/<int:pizza_id>/', views.api_prodotti_correlati, name='api_correlati'),
    
    # API wishlist (richiede login)
    # path('api/wishlist/aggiungi/', views.api_aggiungi_wishlist, name='api_aggiungi_wishlist'),
    # path('api/wishlist/rimuovi/', views.api_rimuovi_wishlist, name='api_rimuovi_wishlist'),
    # path('api/wishlist/', views.api_lista_wishlist, name='api_lista_wishlist'),
    
    # Pagina novità
    # path('novita/', views.novita_view, name='novita'),
    
    # Pagina offerte
    # path('offerte/', views.offerte_catalogo_view, name='offerte_catalogo'),
    
    # Pagina pizza del mese
    # path('pizza-del-mese/', views.pizza_del_mese_view, name='pizza_del_mese'),
    
    # Pagina personalizza pizza
    # path('personalizza/', views.personalizza_pizza_view, name='personalizza_pizza'),
    
    # Pagina builder pizza personalizzata
    # path('pizza-builder/', views.pizza_builder_view, name='pizza_builder'),
    
    # API export catalogo PDF
    # path('api/export/pdf/', views.api_export_pdf_catalogo, name='api_export_pdf'),
    
    # API condividi prodotto
    # path('api/condividi/<int:pizza_id>/', views.api_condividi_prodotto, name='api_condividi'),
    
    # Pagina stampa catalogo
    # path('stampa/', views.stampa_catalogo_view, name='stampa_catalogo'),
    
    # ========================================
    # 📄 PAGINE PLACEHOLDER TEMPORANEE (opzionali)
    # ========================================
    # Puoi usare queste per testare gli URL senza implementare le views
    
    # Pagina categoria specifica (placeholder)
    path('categoria/<slug:categoria_slug>/', TemplateView.as_view(
        template_name='prodotti/categoria.html',
        extra_context={'titolo_pagina': 'Categoria - PizzaMama'}
    ), name='categoria'),
    
    # Pagina ricerca avanzata (placeholder)
    path('ricerca/', TemplateView.as_view(
        template_name='prodotti/ricerca.html',
        extra_context={'titolo_pagina': 'Ricerca - PizzaMama'}
    ), name='ricerca_avanzata'),
    
    # Pagina confronto pizze (placeholder)
    path('confronta/', TemplateView.as_view(
        template_name='prodotti/confronta.html',
        extra_context={'titolo_pagina': 'Confronta Pizze - PizzaMama'}
    ), name='confronta_pizze'),
    
    # Pagina ingredienti (placeholder)
    path('ingredienti/', TemplateView.as_view(
        template_name='prodotti/ingredienti.html',
        extra_context={'titolo_pagina': 'Ingredienti - PizzaMama'}
    ), name='ingredienti'),
    
    # Pagina novità (placeholder)
    path('novita/', TemplateView.as_view(
        template_name='prodotti/novita.html',
        extra_context={'titolo_pagina': 'Novità - PizzaMama'}
    ), name='novita'),
    
    # Pagina offerte (placeholder)
    path('offerte/', TemplateView.as_view(
        template_name='prodotti/offerte.html',
        extra_context={'titolo_pagina': 'Offerte - PizzaMama'}
    ), name='offerte_catalogo'),
    
    # Pagina pizza del mese (placeholder)
    path('pizza-del-mese/', TemplateView.as_view(
        template_name='prodotti/pizza_del_mese.html',
        extra_context={'titolo_pagina': 'Pizza del Mese - PizzaMama'}
    ), name='pizza_del_mese'),
    
    # Pagina personalizza pizza (placeholder)
    path('personalizza/', TemplateView.as_view(
        template_name='prodotti/personalizza.html',
        extra_context={'titolo_pagina': 'Personalizza Pizza - PizzaMama'}
    ), name='personalizza_pizza'),
    
    # Pagina builder pizza personalizzata (placeholder)
    path('pizza-builder/', TemplateView.as_view(
        template_name='prodotti/pizza_builder.html',
        extra_context={'titolo_pagina': 'Pizza Builder - PizzaMama'}
    ), name='pizza_builder'),
    
    # Pagina stampa catalogo (placeholder)
    path('stampa/', TemplateView.as_view(
        template_name='prodotti/stampa.html',
        extra_context={'titolo_pagina': 'Stampa Catalogo - PizzaMama'}
    ), name='stampa_catalogo'),
]

# ========================================
# 🚧 URL PATTERNS SEO - DA IMPLEMENTARE PIÙ TARDI
# ========================================
# Decommenta questa sezione quando implementi le relative views

seo_patterns = [
    # URLs con slug per SEO migliore
    # path('pizza/<slug:pizza_slug>/', views.dettaglio_pizza_slug_view, name='dettaglio_pizza_slug'),
    # path('categoria/<slug:categoria_slug>/pizza/<slug:pizza_slug>/', views.pizza_in_categoria_view, name='pizza_in_categoria'),
    
    # URLs per filtri comuni
    # path('vegetariane/', views.pizze_vegetariane_view, name='pizze_vegetariane'),
    # path('vegane/', views.pizze_vegane_view, name='pizze_vegane'),
    # path('senza-glutine/', views.pizze_senza_glutine_view, name='pizze_senza_glutine'),
    # path('classiche/', views.pizze_classiche_view, name='pizze_classiche'),
    # path('gourmet/', views.pizze_gourmet_view, name='pizze_gourmet'),
]

# 📄 Pattern SEO con placeholder temporanei
seo_patterns_placeholder = [
    # URLs con slug per SEO migliore (placeholder)
    path('pizza/<slug:pizza_slug>/', TemplateView.as_view(
        template_name='prodotti/dettaglio_slug.html',
        extra_context={'titolo_pagina': 'Pizza - PizzaMama'}
    ), name='dettaglio_pizza_slug'),
    
    # URLs per filtri comuni (placeholder)
    path('vegetariane/', TemplateView.as_view(
        template_name='prodotti/vegetariane.html',
        extra_context={'titolo_pagina': 'Pizze Vegetariane - PizzaMama'}
    ), name='pizze_vegetariane'),
    
    path('vegane/', TemplateView.as_view(
        template_name='prodotti/vegane.html',
        extra_context={'titolo_pagina': 'Pizze Vegane - PizzaMama'}
    ), name='pizze_vegane'),
    
    path('senza-glutine/', TemplateView.as_view(
        template_name='prodotti/senza_glutine.html',
        extra_context={'titolo_pagina': 'Pizze Senza Glutine - PizzaMama'}
    ), name='pizze_senza_glutine'),
    
    path('classiche/', TemplateView.as_view(
        template_name='prodotti/classiche.html',
        extra_context={'titolo_pagina': 'Pizze Classiche - PizzaMama'}
    ), name='pizze_classiche'),
    
    path('gourmet/', TemplateView.as_view(
        template_name='prodotti/gourmet.html',
        extra_context={'titolo_pagina': 'Pizze Gourmet - PizzaMama'}
    ), name='pizze_gourmet'),
]

# Aggiungi pattern SEO placeholder (rimuovi quando implementi le views reali)
urlpatterns.extend(seo_patterns_placeholder)

# ========================================
# METADATI URL CONFIGURATION
# ========================================

URL_METADATA = {
    'app_name': 'products',
    'namespace': 'catalogo',
    'total_patterns': len(urlpatterns),
    'views_implementate': 8,     # Views che esistono e funzionano
    'views_da_implementare': 18, # Views commentate da implementare
    'placeholder_attivi': 12,    # TemplateView placeholder attivi
    'stato': 'Sviluppo - Solo views base implementate',
    'note': 'La maggior parte delle views sono commentate o placeholder'
}

# ========================================
# 📝 ISTRUZIONI PER SVILUPPO FUTURO
# ========================================

"""
COME CONTINUARE LO SVILUPPO:

1. VIEWS PRIORITARIE DA IMPLEMENTARE:
   ✅ catalogo_view (già fatto)
   ✅ dettaglio_pizza_view (già fatto)
   ✅ api_ricerca_prodotti (già fatto)
   ✅ api_categorie_prodotti (già fatto)
   🚧 categoria_view (da implementare)
   🚧 ricerca_avanzata_view (da implementare)
   🚧 confronta_pizze_view (da implementare)

2. API PRIORITARIE DA IMPLEMENTARE:
   ✅ api_ricerca_prodotti (già fatto)
   ✅ api_suggerimenti_ricerca (già fatto)
   ✅ api_popolari (già fatto)
   🚧 api_pizze_del_giorno (da implementare)
   🚧 api_recensioni_prodotto (da implementare)
   🚧 api_wishlist_* (da implementare)

3. FUNZIONALITÀ AVANZATE DA IMPLEMENTARE:
   🚧 pizza_builder_view
   🚧 personalizza_pizza_view
   🚧 api_export_pdf_catalogo
   🚧 Sistema wishlist completo
   🚧 Sistema recensioni

4. PROCESSO DI IMPLEMENTAZIONE:
   - Scegli una view da implementare
   - Decommentala nella sezione "🚧 VIEWS DA IMPLEMENTARE PIÙ TARDI"
   - Commenta la corrispondente TemplateView placeholder
   - Implementa la view in views.py
   - Crea il template necessario
   - Testa la funzionalità

5. TEMPLATE DA CREARE (quando necessari):
   - templates/prodotti/categoria.html
   - templates/prodotti/ricerca.html
   - templates/prodotti/confronta.html
   - templates/prodotti/ingredienti.html
   - templates/prodotti/novita.html
   - templates/prodotti/offerte.html
   - templates/prodotti/pizza_del_mese.html
   - templates/prodotti/personalizza.html
   - templates/prodotti/pizza_builder.html
   - templates/prodotti/stampa.html

STATO ATTUALE:
✅ Server funzionante con views base
📄 Placeholder per tutte le pagine
🚧 Sviluppo graduale possibile
"""