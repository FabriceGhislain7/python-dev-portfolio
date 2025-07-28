# apps/products/views.py
"""
🍕 PIZZAMAMA ENTERPRISE - Views Prodotti Frontend
Views per l'integrazione frontend con API prodotti
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .models import Pizza, Category, Ingredient


def catalogo_view(request):
    """
    View principale per la pagina del catalogo prodotti
    Supporta filtri via GET parameters
    """
    contesto_pagina = {
        'titolo_pagina': 'Catalogo Pizze - PizzaMama',
        'descrizione_meta': 'Scopri il nostro catalogo di pizze artigianali',
        'canonical_url': request.build_absolute_uri(),
        
        # Dati per filtri
        'categorie_disponibili': Category.objects.filter(attiva=True),
        'ingredienti_popolari': Ingredient.objects.filter(
            disponibile=True
        ).order_by('-popolarita')[:10],
        
        # Configurazione JavaScript
        'config_js': {
            'api_endpoint': '/api/prodotti/',
            'elementi_per_pagina': 12,
            'abilita_infinite_scroll': True
        }
    }
    
    return render(request, 'prodotti/catalogo.html', contesto_pagina)


def dettaglio_pizza_view(request, pizza_id):
    """
    View per mostrare i dettagli di una pizza specifica
    """
    pizza = get_object_or_404(Pizza, id=pizza_id, disponibile=True)
    
    # Pizze correlate (stessa categoria)
    pizze_correlate = Pizza.objects.filter(
        categoria=pizza.categoria,
        disponibile=True
    ).exclude(id=pizza.id)[:4]
    
    # Ingredienti opzionali disponibili
    ingredienti_extra = Ingredient.objects.filter(
        disponibile=True,
        extra=True
    ).order_by('nome')
    
    contesto_pagina = {
        'pizza': pizza,
        'pizze_correlate': pizze_correlate,
        'ingredienti_extra': ingredienti_extra,
        'titolo_pagina': f'{pizza.nome} - PizzaMama',
        'descrizione_meta': pizza.descrizione,
        'immagine_og': pizza.immagine.url if pizza.immagine else None,
        
        # Dati strutturati per SEO
        'structured_data': {
            '@context': 'https://schema.org',
            '@type': 'Product',
            'name': pizza.nome,
            'description': pizza.descrizione,
            'image': pizza.immagine.url if pizza.immagine else '',
            'offers': {
                '@type': 'Offer',
                'price': str(pizza.prezzo),
                'priceCurrency': 'EUR',
                'availability': 'https://schema.org/InStock'
            }
        }
    }
    
    return render(request, 'prodotti/dettaglio.html', contesto_pagina)


@require_http_methods(["GET"])
def api_ricerca_prodotti(request):
    """
    API endpoint per ricerca prodotti con filtri avanzati
    Utilizzata dal frontend JavaScript per filtraggio dinamico
    """
    try:
        # Parametri di ricerca
        query_ricerca = request.GET.get('q', '').strip()
        categoria_id = request.GET.get('categoria')
        prezzo_min = request.GET.get('prezzo_min')
        prezzo_max = request.GET.get('prezzo_max')
        ingredienti = request.GET.getlist('ingredienti')
        vegetariana = request.GET.get('vegetariana')
        senza_glutine = request.GET.get('senza_glutine')
        ordinamento = request.GET.get('ordinamento', 'nome')
        pagina = int(request.GET.get('pagina', 1))
        per_pagina = int(request.GET.get('per_pagina', 12))
        
        # Query base
        pizze = Pizza.objects.filter(disponibile=True)
        
        # Applicazione filtri
        if query_ricerca:
            pizze = pizze.filter(
                Q(nome__icontains=query_ricerca) |
                Q(descrizione__icontains=query_ricerca) |
                Q(ingredienti__nome__icontains=query_ricerca)
            ).distinct()
        
        if categoria_id:
            pizze = pizze.filter(categoria_id=categoria_id)
        
        if prezzo_min:
            pizze = pizze.filter(prezzo__gte=float(prezzo_min))
        
        if prezzo_max:
            pizze = pizze.filter(prezzo__lte=float(prezzo_max))
        
        if ingredienti:
            for ingrediente_id in ingredienti:
                pizze = pizze.filter(ingredienti__id=ingrediente_id)
        
        if vegetariana == 'true':
            pizze = pizze.filter(vegetariana=True)
        
        if senza_glutine == 'true':
            pizze = pizze.filter(senza_glutine=True)
        
        # Ordinamento
        ordinamenti_validi = {
            'nome': 'nome',
            'prezzo_crescente': 'prezzo',
            'prezzo_decrescente': '-prezzo',
            'popolarita': '-popolare',
            'nuovo': '-data_creazione'
        }
        
        if ordinamento in ordinamenti_validi:
            pizze = pizze.order_by(ordinamenti_validi[ordinamento])
        
        # Paginazione
        paginator = Paginator(pizze, per_pagina)
        pagina_oggetto = paginator.get_page(pagina)
        
        # Serializzazione risultati
        risultati = []
        for pizza in pagina_oggetto:
            risultati.append({
                'id': pizza.id,
                'nome': pizza.nome,
                'descrizione': pizza.descrizione,
                'prezzo': float(pizza.prezzo),
                'immagine': pizza.immagine.url if pizza.immagine else None,
                'categoria': pizza.categoria.nome if pizza.categoria else None,
                'ingredienti': [ing.nome for ing in pizza.ingredienti.all()],
                'vegetariana': pizza.vegetariana,
                'senza_glutine': pizza.senza_glutine,
                'popolare': pizza.popolare,
                'nuovo': pizza.nuovo,
                'tempo_preparazione': pizza.tempo_preparazione,
                'calorie': pizza.calorie
            })
        
        risposta_data = {
            'risultati': risultati,
            'paginazione': {
                'pagina_corrente': pagina_oggetto.number,
                'pagine_totali': paginator.num_pages,
                'elementi_totali': paginator.count,
                'ha_precedente': pagina_oggetto.has_previous(),
                'ha_successiva': pagina_oggetto.has_next(),
                'numero_precedente': pagina_oggetto.previous_page_number() if pagina_oggetto.has_previous() else None,
                'numero_successiva': pagina_oggetto.next_page_number() if pagina_oggetto.has_next() else None
            },
            'filtri_applicati': {
                'ricerca': query_ricerca,
                'categoria': categoria_id,
                'prezzo_min': prezzo_min,
                'prezzo_max': prezzo_max,
                'ingredienti': ingredienti,
                'vegetariana': vegetariana,
                'senza_glutine': senza_glutine,
                'ordinamento': ordinamento
            }
        }
        
        return JsonResponse(risposta_data)
        
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nella ricerca prodotti',
            'dettaglio': str(errore)
        }, status=400)


@require_http_methods(["GET"])
def api_suggerimenti_ricerca(request):
    """
    API per suggerimenti di ricerca autocomplete
    """
    try:
        query = request.GET.get('q', '').strip()
        limite = int(request.GET.get('limite', 10))
        
        if len(query) < 2:
            return JsonResponse({'suggerimenti': []})
        
        # Suggerimenti da nomi pizze
        pizze_suggerimenti = Pizza.objects.filter(
            nome__icontains=query,
            disponibile=True
        ).values_list('nome', flat=True)[:limite//2]
        
        # Suggerimenti da ingredienti
        ingredienti_suggerimenti = Ingredient.objects.filter(
            nome__icontains=query,
            disponibile=True
        ).values_list('nome', flat=True)[:limite//2]
        
        # Combina e deduplica
        tutti_suggerimenti = list(set(
            list(pizze_suggerimenti) + list(ingredienti_suggerimenti)
        ))[:limite]
        
        return JsonResponse({
            'suggerimenti': tutti_suggerimenti,
            'query': query
        })
        
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento suggerimenti',
            'dettaglio': str(errore)
        }, status=400)


@require_http_methods(["GET"])
def api_categorie_prodotti(request):
    """
    API per ottenere tutte le categorie disponibili con conteggio prodotti
    """
    try:
        categorie = []
        
        for categoria in Category.objects.filter(attiva=True):
            conteggio_prodotti = Pizza.objects.filter(
                categoria=categoria,
                disponibile=True
            ).count()
            
            categorie.append({
                'id': categoria.id,
                'nome': categoria.nome,
                'descrizione': categoria.descrizione,
                'immagine': categoria.immagine.url if categoria.immagine else None,
                'conteggio_prodotti': conteggio_prodotti,
                'ordine': categoria.ordine
            })
        
        # Ordina per campo ordine
        categorie.sort(key=lambda x: x['ordine'])
        
        return JsonResponse({
            'categorie': categorie,
            'totale': len(categorie)
        })
        
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento categorie',
            'dettaglio': str(errore)
        }, status=400)


@require_http_methods(["GET"])
def api_ingredienti_disponibili(request):
    """
    API per ottenere tutti gli ingredienti disponibili
    """
    try:
        categoria_filtro = request.GET.get('categoria')
        solo_extra = request.GET.get('solo_extra') == 'true'
        
        ingredienti_query = Ingredient.objects.filter(disponibile=True)
        
        if solo_extra:
            ingredienti_query = ingredienti_query.filter(extra=True)
        
        ingredienti = []
        for ingrediente in ingredienti_query.order_by('nome'):
            # Conta pizze che contengono questo ingrediente
            pizze_con_ingrediente = Pizza.objects.filter(
                ingredienti=ingrediente,
                disponibile=True
            )
            
            if categoria_filtro:
                pizze_con_ingrediente = pizze_con_ingrediente.filter(
                    categoria_id=categoria_filtro
                )
            
            conteggio = pizze_con_ingrediente.count()
            
            if conteggio > 0:  # Solo ingredienti effettivamente utilizzati
                ingredienti.append({
                    'id': ingrediente.id,
                    'nome': ingrediente.nome,
                    'descrizione': ingrediente.descrizione,
                    'prezzo_extra': float(ingrediente.prezzo_extra) if ingrediente.prezzo_extra else 0,
                    'allergeni': ingrediente.allergeni,
                    'vegetariano': ingrediente.vegetariano,
                    'vegano': ingrediente.vegano,
                    'senza_glutine': ingrediente.senza_glutine,
                    'popolarita': ingrediente.popolarita,
                    'conteggio_utilizzo': conteggio
                })
        
        return JsonResponse({
            'ingredienti': ingredienti,
            'totale': len(ingredienti)
        })
        
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento ingredienti',
            'dettaglio': str(errore)
        }, status=400)


@require_http_methods(["GET"])
def api_pizze_popolari(request):
    """
    API per ottenere le pizze più popolari
    """
    try:
        limite = int(request.GET.get('limite', 8))
        categoria_id = request.GET.get('categoria')
        
        pizze_query = Pizza.objects.filter(
            disponibile=True,
            popolare=True
        )
        
        if categoria_id:
            pizze_query = pizze_query.filter(categoria_id=categoria_id)
        
        pizze_popolari = pizze_query.order_by('-popolarita', 'nome')[:limite]
        
        risultati = []
        for pizza in pizze_popolari:
            risultati.append({
                'id': pizza.id,
                'nome': pizza.nome,
                'descrizione': pizza.descrizione,
                'prezzo': float(pizza.prezzo),
                'immagine': pizza.immagine.url if pizza.immagine else None,
                'categoria': pizza.categoria.nome if pizza.categoria else None,
                'ingredienti': [ing.nome for ing in pizza.ingredienti.all()],
                'vegetariana': pizza.vegetariana,
                'senza_glutine': pizza.senza_glutine,
                'tempo_preparazione': pizza.tempo_preparazione,
                'calorie': pizza.calorie,
                'popolarita': pizza.popolarita
            })
        
        return JsonResponse({
            'pizze_popolari': risultati,
            'totale': len(risultati)
        })
        
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento pizze popolari',
            'dettaglio': str(errore)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_valutazione_prodotto(request):
    """
    API per aggiungere valutazione a un prodotto
    """
    try:
        dati = json.loads(request.body)
        pizza_id = dati.get('pizza_id')
        valutazione = dati.get('valutazione')  # 1-5 stelle
        commento = dati.get('commento', '')
        nome_utente = dati.get('nome_utente', 'Anonimo')
        
        # Validazione
        if not pizza_id or not valutazione:
            return JsonResponse({
                'errore': 'ID pizza e valutazione sono obbligatori'
            }, status=400)
        
        if not (1 <= int(valutazione) <= 5):
            return JsonResponse({
                'errore': 'La valutazione deve essere tra 1 e 5 stelle'
            }, status=400)
        
        pizza = get_object_or_404(Pizza, id=pizza_id, disponibile=True)
        
        # Per ora simuliamo il salvataggio (implementare model Review)
        # In una versione completa, salveresti in un model Review
        
        return JsonResponse({
            'successo': True,
            'messaggio': 'Valutazione aggiunta con successo',
            'valutazione': {
                'pizza_id': pizza_id,
                'valutazione': valutazione,
                'commento': commento,
                'nome_utente': nome_utente,
                'data': 'oggi'  # Sostituire con timestamp reale
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'errore': 'Formato dati non valido'
        }, status=400)
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel salvataggio valutazione',
            'dettaglio': str(errore)
        }, status=500)


@require_http_methods(["GET"])
def api_statistiche_catalogo(request):
    """
    API per statistiche generali del catalogo
    Utile per dashboard e analytics
    """
    try:
        # Statistiche base
        totale_pizze = Pizza.objects.filter(disponibile=True).count()
        totale_categorie = Category.objects.filter(attiva=True).count()
        totale_ingredienti = Ingredient.objects.filter(disponibile=True).count()
        
        # Pizze per categoria
        pizze_per_categoria = {}
        for categoria in Category.objects.filter(attiva=True):
            conteggio = Pizza.objects.filter(
                categoria=categoria,
                disponibile=True
            ).count()
            pizze_per_categoria[categoria.nome] = conteggio
        
        # Range prezzi
        prezzi = Pizza.objects.filter(disponibile=True).values_list('prezzo', flat=True)
        prezzo_min = min(prezzi) if prezzi else 0
        prezzo_max = max(prezzi) if prezzi else 0
        prezzo_medio = sum(prezzi) / len(prezzi) if prezzi else 0
        
        # Pizze speciali
        pizze_vegetariane = Pizza.objects.filter(
            disponibile=True,
            vegetariana=True
        ).count()
        
        pizze_senza_glutine = Pizza.objects.filter(
            disponibile=True,
            senza_glutine=True
        ).count()
        
        pizze_popolari = Pizza.objects.filter(
            disponibile=True,
            popolare=True
        ).count()
        
        statistiche = {
            'totali': {
                'pizze': totale_pizze,
                'categorie': totale_categorie,
                'ingredienti': totale_ingredienti
            },
            'distribuzione_categorie': pizze_per_categoria,
            'prezzi': {
                'minimo': float(prezzo_min),
                'massimo': float(prezzo_max),
                'medio': round(float(prezzo_medio), 2)
            },
            'speciali': {
                'vegetariane': pizze_vegetariane,
                'senza_glutine': pizze_senza_glutine,
                'popolari': pizze_popolari
            },
            'percentuali': {
                'vegetariane': round((pizze_vegetariane / totale_pizze * 100), 1) if totale_pizze > 0 else 0,
                'senza_glutine': round((pizze_senza_glutine / totale_pizze * 100), 1) if totale_pizze > 0 else 0,
                'popolari': round((pizze_popolari / totale_pizze * 100), 1) if totale_pizze > 0 else 0
            }
        }
        
        return JsonResponse({
            'statistiche': statistiche,
            'ultimo_aggiornamento': 'oggi'  # Sostituire con timestamp reale
        })
        
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento statistiche',
            'dettaglio': str(errore)
        }, status=500)