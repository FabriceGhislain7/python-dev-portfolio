"""
Viste principali per PizzaMama Enterprise - Step 12 Frontend

Viste principali per homepage e pagine generali del sito.
Integrazione con API REST per dati dinamici con nomi italiani.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
import json

def homepage(request):
    """
    Homepage del sito PizzaMama Enterprise
    
    Mostra:
    - Sezione hero con call-to-action
    - Pizze in evidenza (featured)
    - Categorie principali
    - Testimonianze clienti
    """
    contesto_pagina = {
        'titolo_pagina': 'PizzaMama - La Miglior Pizza a Domicilio',
        'descrizione_meta': 'Ordina la migliore pizza a domicilio. Ingredienti freschi, consegna veloce, prezzi imbattibili.',
        'titolo_hero': 'La Pizza Perfetta, Consegnata a Casa Tua',
        'sottotitolo_hero': 'Ingredienti freschi, ricette tradizionali e consegna veloce in tutta la città',
        'testo_cta': 'Ordina Ora',
        'url_catalogo': '/catalogo/',
        'numero_telefono': getattr(settings, 'IMPOSTAZIONI_BUSINESS', {}).get('telefono', '+39 010 123 4567'),
        
        # Sezione statistiche per homepage
        'statistiche_azienda': {
            'pizze_consegnate': '50.000+',
            'clienti_felici': '15.000+',
            'anni_esperienza': '5+',
            'citta_servite': '5'
        },
        
        # Testimonianze clienti
        'testimonianze': [
            {
                'nome': 'Marco R.',
                'voto': 5,
                'commento': 'Pizza fantastica e consegna velocissima! La migliore di Genova.',
                'data': '2025-07-25'
            },
            {
                'nome': 'Laura M.',
                'voto': 5,
                'commento': 'Ingredienti freschi e qualità eccellente. Super consigliata!',
                'data': '2025-07-23'
            },
            {
                'nome': 'Alessandro T.',
                'voto': 5,
                'commento': 'Servizio impeccabile e pizze deliziose. Ordino spesso qui.',
                'data': '2025-07-20'
            }
        ],
        
        # Caratteristiche principali
        'caratteristiche_principali': [
            {
                'icona': '🍕',
                'titolo': 'Ricette Autentiche',
                'descrizione': 'Ricette tradizionali della pizza napoletana'
            },
            {
                'icona': '🚚',
                'titolo': 'Consegna Veloce',
                'descrizione': 'Consegna garantita in 30 minuti'
            },
            {
                'icona': '🍅',
                'titolo': 'Ingredienti Freschi',
                'descrizione': 'Solo ingredienti di prima qualità'
            },
            {
                'icona': '💰',
                'titolo': 'Prezzi Onesti',
                'descrizione': 'Qualità alta a prezzi accessibili'
            }
        ]
    }
    
    return render(request, 'pages/home.html', contesto_pagina)

def chi_siamo(request):
    """
    Pagina Chi Siamo
    
    Racconta la storia di PizzaMama, i valori aziendali
    e l'impegno per la qualità.
    """
    contesto_pagina = {
        'titolo_pagina': 'Chi Siamo - PizzaMama',
        'descrizione_meta': 'Scopri la storia di PizzaMama, la nostra passione per la pizza e l\'impegno per la qualità.',
        'storia_azienda': {
            'anno_fondazione': '2020',
            'pizze_consegnate': '50.000+',
            'clienti_felici': '15.000+',
            'citta_servite': '5 città',
            'anni_esperienza': '5 anni',
            'motto': 'Passione, Qualità, Tradizione'
        },
        'valori_aziendali': [
            {
                'titolo': 'Qualità Ingredienti',
                'descrizione': 'Solo ingredienti freschi e di prima scelta, selezionati dai migliori fornitori italiani',
                'icona': '🍅'
            },
            {
                'titolo': 'Consegna Veloce', 
                'descrizione': 'Consegna garantita in 30 minuti per mantenere la pizza calda e fragrante',
                'icona': '🚚'
            },
            {
                'titolo': 'Ricette Tradizionali',
                'descrizione': 'Ricette autentiche della tradizione italiana tramandate di generazione in generazione',
                'icona': '🍕'
            },
            {
                'titolo': 'Sostenibilità',
                'descrizione': 'Impegno per l\'ambiente con packaging eco-sostenibile e fornitori locali',
                'icona': '🌱'
            },
            {
                'titolo': 'Innovazione',
                'descrizione': 'Tecnologia moderna per ordinazioni facili e tracking in tempo reale',
                'icona': '📱'
            },
            {
                'titolo': 'Comunità',
                'descrizione': 'Parte attiva della comunità locale con iniziative sociali e benefiche',
                'icona': '🤝'
            }
        ],
        'team': [
            {
                'nome': 'Giuseppe Marinelli',
                'ruolo': 'Founder & Head Chef',
                'esperienza': '15 anni',
                'specialita': 'Pizza Napoletana'
            },
            {
                'nome': 'Maria Rossi',
                'ruolo': 'Operations Manager',
                'esperienza': '8 anni',
                'specialita': 'Gestione Qualità'
            },
            {
                'nome': 'Antonio Bianchi',
                'ruolo': 'Delivery Manager',
                'esperienza': '5 anni',
                'specialita': 'Logistica Consegne'
            }
        ]
    }
    
    return render(request, 'pages/about.html', contesto_pagina)

def contatti(request):
    """
    Pagina contatti con form e informazioni aziendali
    """
    contesto_pagina = {
        'titolo_pagina': 'Contatti - PizzaMama',
        'descrizione_meta': 'Contatta PizzaMama per informazioni, suggerimenti o assistenza clienti.',
        'informazioni_contatto': {
            'telefono': '+39 010 123 4567',
            'email': 'info@pizzamama.it',
            'email_support': 'support@pizzamama.it',
            'indirizzo': 'Via Roma 123, 16121 Genova (GE)',
            'partita_iva': 'IT12345678901',
            'orari_apertura': {
                'giorni_feriali': '11:00 - 23:00',
                'fine_settimana': '11:00 - 24:00',
                'note_speciali': 'Chiusi il lunedì mattina per riposo',
                'giorni_festivi': 'Orari ridotti: 17:00 - 23:00'
            },
            'social_media': {
                'facebook': 'https://facebook.com/pizzamamagenova',
                'instagram': 'https://instagram.com/pizzamamagenova',
                'twitter': 'https://twitter.com/pizzamamagenova',
                'whatsapp': '+39 010 123 4567',
                'telegram': '@pizzamamagenova'
            }
        },
        'mappa_google': {
            'latitudine': 44.4056,
            'longitudine': 8.9463,
            'zoom_livello': 15,
            'marker_title': 'PizzaMama - Via Roma 123'
        },
        'form_contatti': {
            'motivi_contatto': [
                'Informazioni generali',
                'Problema con ordine',
                'Suggerimenti',
                'Lavora con noi',
                'Partnership commerciali',
                'Altro'
            ]
        }
    }
    
    return render(request, 'pages/contact.html', contesto_pagina)

def privacy_policy(request):
    """
    Pagina Privacy Policy per conformità GDPR
    """
    contesto_pagina = {
        'titolo_pagina': 'Privacy Policy - PizzaMama',
        'descrizione_meta': 'Informativa sulla privacy e trattamento dati personali di PizzaMama.',
        'ultimo_aggiornamento': '28 Luglio 2025',
        'sezioni_privacy': [
            {
                'titolo': 'Dati Raccolti',
                'contenuto': 'Nome, cognome, email, telefono, indirizzo di consegna, preferenze alimentari',
                'dettagli': [
                    'Dati anagrafici per identificazione utente',
                    'Informazioni di contatto per comunicazioni',
                    'Indirizzi per gestione consegne',
                    'Preferenze per personalizzazione servizio'
                ]
            },
            {
                'titolo': 'Finalità Utilizzo',
                'contenuto': 'Gestione ordini, consegne, comunicazioni commerciali, miglioramento servizi',
                'dettagli': [
                    'Elaborazione e gestione ordini',
                    'Organizzazione consegne',
                    'Invio comunicazioni promozionali',
                    'Analisi preferenze clienti',
                    'Assistenza clienti'
                ]
            },
            {
                'titolo': 'Diritti Utente',
                'contenuto': 'Accesso, rettifica, cancellazione, portabilità dati, opposizione trattamento',
                'dettagli': [
                    'Diritto di accesso ai propri dati',
                    'Diritto di rettifica dati inesatti',
                    'Diritto alla cancellazione',
                    'Diritto alla portabilità',
                    'Diritto di opposizione',
                    'Diritto di limitazione trattamento'
                ]
            },
            {
                'titolo': 'Cookie Policy',
                'contenuto': 'Utilizzo cookie tecnici e di analytics per migliorare esperienza utente',
                'dettagli': [
                    'Cookie tecnici per funzionamento sito',
                    'Cookie di preferenze per personalizzazione',
                    'Cookie analytics per statistiche anonime',
                    'Cookie di marketing (previa autorizzazione)'
                ]
            },
            {
                'titolo': 'Sicurezza Dati',
                'contenuto': 'Misure tecniche e organizzative per protezione dati personali',
                'dettagli': [
                    'Crittografia dati sensibili',
                    'Backup regolari sicuri',
                    'Accesso limitato al personale autorizzato',
                    'Monitoraggio accessi e attività'
                ]
            }
        ],
        'contatti_privacy': {
            'dpo_email': 'privacy@pizzamama.it',
            'dpo_nome': 'Responsabile Protezione Dati',
            'autorita_garante': 'Garante per la Protezione dei Dati Personali'
        }
    }
    
    return render(request, 'pages/privacy.html', contesto_pagina)

def termini_servizio(request):
    """
    Pagina Termini di Servizio e condizioni d'uso
    """
    contesto_pagina = {
        'titolo_pagina': 'Termini di Servizio - PizzaMama',
        'descrizione_meta': 'Termini e condizioni di utilizzo del servizio PizzaMama.',
        'ultimo_aggiornamento': '28 Luglio 2025',
        'sezioni_termini': [
            {
                'titolo': 'Condizioni Ordine',
                'contenuto': 'Ordine minimo €8, modalità pagamento accettate, tempi consegna standard',
                'dettagli': [
                    'Ordine minimo: €8,00 per consegna',
                    'Pagamenti: carta, PayPal, contrassegno',
                    'Tempi consegna: 20-30 minuti',
                    'Zone servite: centro città',
                    'Supplemento consegna: €3,50'
                ]
            },
            {
                'titolo': 'Responsabilità',
                'contenuto': 'Limitazioni responsabilità, garanzie qualità, politiche rimborso',
                'dettagli': [
                    'Garanzia qualità ingredienti',
                    'Responsabilità limitata per ritardi consegna',
                    'Esclusioni per eventi eccezionali',
                    'Assicurazione per danni consegna',
                    'Limitazioni responsabilità utente'
                ]
            },
            {
                'titolo': 'Politiche Annullamento',
                'contenuto': 'Termini per annullamento ordini, rimborsi, modifiche dell\'ultimo minuto',
                'dettagli': [
                    'Annullamento gratuito entro 5 minuti',
                    'Dopo 5 minuti: rimborso 50%',
                    'Pizza già in forno: nessun rimborso',
                    'Problemi qualità: rimborso completo',
                    'Ritardi oltre 45 min: sconto 20%'
                ]
            },
            {
                'titolo': 'Uso del Sito',
                'contenuto': 'Regole utilizzo sito web, account utente, comportamenti vietati',
                'dettagli': [
                    'Registrazione con dati veritieri',
                    'Divieto uso improprio sistema',
                    'Rispetto altri utenti',
                    'Segnalazione problemi tecnici',
                    'Aggiornamento dati personali'
                ]
            },
            {
                'titolo': 'Modifiche Servizio',
                'contenuto': 'Diritto modifica prezzi, menu, zone consegna con preavviso',
                'dettagli': [
                    'Preavviso modifiche: 7 giorni',
                    'Aggiornamenti menu stagionali',
                    'Possibili variazioni prezzi',
                    'Espansione/riduzione zone servite',
                    'Comunicazione via email/sito'
                ]
            }
        ],
        'info_legali': {
            'ragione_sociale': 'PizzaMama S.r.l.',
            'sede_legale': 'Via Roma 123, 16121 Genova (GE)',
            'partita_iva': 'IT12345678901',
            'codice_fiscale': '12345678901',
            'capitale_sociale': '€50.000 i.v.',
            'tribunale': 'Tribunale di Genova',
            'numero_rea': 'GE-123456'
        }
    }
    
    return render(request, 'pages/terms.html', contesto_pagina)

@login_required
def dashboard_utente(request):
    """
    Dashboard utente con panoramica ordini e profilo
    
    Mostra statistiche personali dell'utente:
    - Ordini recenti
    - Punti fedeltà
    - Indirizzi salvati
    - Preferenze alimentari
    """
    utente_corrente = request.user
    
    contesto_pagina = {
        'titolo_pagina': f'Dashboard - {utente_corrente.get_full_name() or utente_corrente.username}',
        'utente': utente_corrente,
        'ha_profilo': hasattr(utente_corrente, 'profile'),
    }
    
    # Aggiungi dati profilo se esiste
    if hasattr(utente_corrente, 'profile'):
        profilo_utente = utente_corrente.profile
        
        # Calcola tier loyalty
        punti_loyalty = profilo_utente.loyalty_points
        if punti_loyalty >= 1000:
            tier_loyalty = {'nome': 'Gold', 'icona': '🥇', 'colore': '#FFD700', 'sconto': 15}
        elif punti_loyalty >= 500:
            tier_loyalty = {'nome': 'Silver', 'icona': '🥈', 'colore': '#C0C0C0', 'sconto': 10}
        elif punti_loyalty >= 100:
            tier_loyalty = {'nome': 'Bronze', 'icona': '🥉', 'colore': '#CD7F32', 'sconto': 5}
        else:
            tier_loyalty = {'nome': 'Base', 'icona': '👤', 'colore': '#666666', 'sconto': 0}
        
        # Punti necessari per tier successivo
        punti_prossimo_tier = 0
        if punti_loyalty < 100:
            punti_prossimo_tier = 100 - punti_loyalty
        elif punti_loyalty < 500:
            punti_prossimo_tier = 500 - punti_loyalty
        elif punti_loyalty < 1000:
            punti_prossimo_tier = 1000 - punti_loyalty
        
        contesto_pagina.update({
            'punti_loyalty': punti_loyalty,
            'tier_loyalty': tier_loyalty,
            'punti_prossimo_tier': punti_prossimo_tier,
            'totale_ordini': profilo_utente.total_orders,
            'totale_speso': profilo_utente.total_spent,
            'media_ordine': (profilo_utente.total_spent / profilo_utente.total_orders) if profilo_utente.total_orders > 0 else 0,
            'preferenze_dietetiche': profilo_utente.preferences.get('dietary_restrictions', []),
            'pizze_preferite': profilo_utente.preferences.get('favorite_pizzas', []),
            'ultimo_ordine': profilo_utente.preferences.get('last_order_date'),
            'pizza_piu_ordinata': profilo_utente.preferences.get('most_ordered_pizza', 'Margherita')
        })
    
    return render(request, 'accounts/dashboard.html', contesto_pagina)

@require_http_methods(["GET"])
def suggerimenti_ricerca(request):
    """
    Endpoint API per suggerimenti di ricerca intelligente
    
    Ritorna JSON con suggerimenti basati su query utente
    per implementare autocomplete nella barra di ricerca.
    """
    termine_ricerca = request.GET.get('q', '').strip()
    
    if len(termine_ricerca) < 2:
        return JsonResponse({'suggerimenti': []})
    
    lista_suggerimenti = []
    
    # Suggerimenti nomi pizze italiane
    pizze_popolari = [
        'Margherita', 'Napoletana', 'Quattro Stagioni', 'Diavola',
        'Quattro Formaggi', 'Prosciutto e Funghi', 'Capricciosa',
        'Marinara', 'Vegetariana', 'Tonno e Cipolle', 'Ortolana',
        'Bufalina', 'Salsiccia e Friarielli', 'Parmigiana', 'Boscaiola',
        'Americana', 'Mexicana', 'Hawaiana', 'Rustica', 'Contadina'
    ]
    
    # Filtra pizze che contengono il termine di ricerca
    pizze_trovate = [
        pizza for pizza in pizze_popolari 
        if termine_ricerca.lower() in pizza.lower()
    ]
    
    # Aggiungi suggerimenti pizze
    lista_suggerimenti.extend([
        {
            'tipo': 'pizza', 
            'testo': nome_pizza, 
            'url': f'/catalogo/ricerca/?q={nome_pizza}',
            'icona': '🍕',
            'categoria': 'Pizza'
        }
        for nome_pizza in pizze_trovate[:5]
    ])
    
    # Suggerimenti categorie
    categorie_mapping = {
        ('classic', 'tradizional', 'napoletan'): {
            'nome': 'Pizze Classiche',
            'url': '/catalogo/categoria/classiche/',
            'icona': '📋'
        },
        ('specia', 'gourmet', 'premium'): {
            'nome': 'Pizze Speciali',
            'url': '/catalogo/categoria/speciali/',
            'icona': '⭐'
        },
        ('vegetarian', 'veggie', 'verdure'): {
            'nome': 'Pizze Vegetariane',
            'url': '/catalogo/categoria/vegetariane/',
            'icona': '🥬'
        },
        ('vegan', 'vegana'): {
            'nome': 'Pizze Vegane',
            'url': '/catalogo/categoria/vegane/',
            'icona': '🌱'
        },
        ('senza glutine', 'gluten free', 'celiaci'): {
            'nome': 'Senza Glutine',
            'url': '/catalogo/categoria/senza-glutine/',
            'icona': '🌾'
        }
    }
    
    for termini, categoria in categorie_mapping.items():
        if any(termine in termine_ricerca.lower() for termine in termini):
            lista_suggerimenti.append({
                'tipo': 'categoria', 
                'testo': categoria['nome'], 
                'url': categoria['url'],
                'icona': categoria['icona'],
                'categoria': 'Categoria'
            })
    
    # Suggerimenti ingredienti
    ingredienti_comuni = [
        'mozzarella', 'pomodoro', 'basilico', 'prosciutto', 'funghi',
        'salame', 'olive', 'capperi', 'rucola', 'gorgonzola', 'speck',
        'bresaola', 'tonno', 'cipolle', 'peperoni', 'melanzane', 'zucchine'
    ]
    
    ingredienti_trovati = [
        ingrediente for ingrediente in ingredienti_comuni
        if termine_ricerca.lower() in ingrediente.lower()
    ]
    
    lista_suggerimenti.extend([
        {
            'tipo': 'ingrediente',
            'testo': f'Pizze con {ingrediente}',
            'url': f'/catalogo/ricerca/?ingrediente={ingrediente}',
            'icona': '🧄',
            'categoria': 'Ingrediente'
        }
        for ingrediente in ingredienti_trovati[:3]
    ])
    
    # Suggerimenti località (per consegna)
    if any(termine in termine_ricerca.lower() for termine in ['consegn', 'domicilio', 'zona']):
        lista_suggerimenti.append({
            'tipo': 'servizio',
            'testo': 'Verifica Zona Consegna',
            'url': '/zona-consegna/',
            'icona': '🚚',
            'categoria': 'Servizio'
        })
    
    # Suggerimenti offerte
    if any(termine in termine_ricerca.lower() for termine in ['offert', 'scont', 'promo']):
        lista_suggerimenti.append({
            'tipo': 'offerta',
            'testo': 'Offerte Speciali',
            'url': '/offerte/',
            'icona': '🎉',
            'categoria': 'Promozione'
        })
    
    return JsonResponse({
        'suggerimenti': lista_suggerimenti[:8],
        'termine_ricerca': termine_ricerca,
        'totale_risultati': len(lista_suggerimenti)
    })

@require_http_methods(["GET", "POST"])
def ricerca_globale(request):
    """
    Pagina risultati ricerca globale
    """
    if request.method == 'POST':
        # Gestione ricerca AJAX
        try:
            termine_ricerca = request.POST.get('q', '').strip()
            if len(termine_ricerca) < 2:
                return JsonResponse({
                    'errore': 'Termine di ricerca troppo breve'
                }, status=400)
            
            # Simula risultati ricerca (in produzione: query database)
            risultati = {
                'pizze': [],
                'categorie': [],
                'ingredienti': [],
                'totale': 0
            }
            
            return JsonResponse({
                'successo': True,
                'risultati': risultati,
                'termine': termine_ricerca
            })
            
        except Exception as e:
            return JsonResponse({
                'errore': 'Errore nella ricerca',
                'dettaglio': str(e)
            }, status=500)
    
    # GET - Mostra pagina ricerca
    termine_ricerca = request.GET.get('q', '').strip()
    
    contesto_pagina = {
        'titolo_pagina': f'Ricerca: {termine_ricerca} - PizzaMama' if termine_ricerca else 'Ricerca - PizzaMama',
        'termine_ricerca': termine_ricerca,
        'ha_risultati': bool(termine_ricerca and len(termine_ricerca) >= 2),
        'suggerimenti_popolari': [
            'Margherita', 'Diavola', 'Quattro Stagioni', 'Capricciosa',
            'Vegetariana', 'Prosciutto e Funghi', 'Quattro Formaggi'
        ]
    }
    
    return render(request, 'pages/search.html', contesto_pagina)

@csrf_exempt
@require_http_methods(["POST"])
def gestione_newsletter(request):
    """
    Gestione iscrizione/disiscrizione newsletter
    """
    try:
        data = json.loads(request.body)
        email_utente = data.get('email', '').strip()
        azione = data.get('azione', 'iscrizione')  # iscrizione/cancellazione
        nome_utente = data.get('nome', '').strip()
        
        if not email_utente:
            return JsonResponse({
                'errore': 'Email obbligatoria'
            }, status=400)
        
        # Validazione email base
        if '@' not in email_utente or '.' not in email_utente:
            return JsonResponse({
                'errore': 'Email non valida'
            }, status=400)
        
        # In produzione: salvare in database o servizio newsletter
        if azione == 'iscrizione':
            messaggio = f'Iscrizione alla newsletter confermata per {email_utente}'
            
            # Invia email di benvenuto (opzionale)
            try:
                send_mail(
                    'Benvenuto nella Newsletter PizzaMama!',
                    f'Ciao {nome_utente or ""},\n\nGrazie per esserti iscritto alla newsletter di PizzaMama!\nRiceverai le nostre migliori offerte e novità direttamente nella tua casella email.\n\nBuona pizza!\nIl Team PizzaMama',
                    settings.DEFAULT_FROM_EMAIL,
                    [email_utente],
                    fail_silently=True,
                )
            except:
                pass  # Non bloccare se invio email fallisce
                
        else:
            messaggio = f'Cancellazione dalla newsletter confermata per {email_utente}'
        
        return JsonResponse({
            'successo': True,
            'messaggio': messaggio,
            'email': email_utente,
            'azione': azione
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'errore': 'Formato dati non valido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'errore': 'Errore nella gestione newsletter',
            'dettaglio': str(e)
        }, status=500)

def pagina_offerte(request):
    """
    Pagina offerte speciali e promozioni
    """
    contesto_pagina = {
        'titolo_pagina': 'Offerte Speciali - PizzaMama',
        'descrizione_meta': 'Scopri le migliori offerte e promozioni PizzaMama. Sconti esclusivi e menu convenienza.',
        'offerte_attive': [
            {
                'id': 1,
                'titolo': 'Menu Famiglia',
                'descrizione': '2 Pizze Grandi + 2 Bibite + Dolce',
                'prezzo_originale': 35.00,
                'prezzo_scontato': 25.00,
                'sconto_percentuale': 29,
                'validita': '31 Agosto 2025',
                'codice_promo': 'FAMIGLIA25',
                'condizioni': 'Valido tutti i giorni, esclusi festivi',
                'popolare': True
            },
            {
                'id': 2,
                'titolo': 'Pizza del Giorno',
                'descrizione': 'Sconto del 20% sulla pizza del giorno',
                'prezzo_originale': None,
                'prezzo_scontato': None,
                'sconto_percentuale': 20,
                'validita': 'Ogni giorno',
                'codice_promo': 'GIORNO20',
                'condizioni': 'Valido dal lunedì al venerdì',
                'popolare': False
            },
            {
                'id': 3,
                'titolo': 'Student Special',
                'descrizione': '15% di sconto per studenti universitari',
                'prezzo_originale': None,
                'prezzo_scontato': None,
                'sconto_percentuale': 15,
                'validita': '31 Dicembre 2025',
                'codice_promo': 'STUDENT15',
                'condizioni': 'Presentare tessera universitaria valida',
                'popolare': True
            },
            {
                'id': 4,
                'titolo': 'Happy Hour',
                'descrizione': 'Pizza + Bibita a soli 10€',
                'prezzo_originale': 15.00,
                'prezzo_scontato': 10.00,
                'sconto_percentuale': 33,
                'validita': 'Tutti i giorni',
                'codice_promo': 'HAPPY10',
                'condizioni': 'Valido dalle 17:00 alle 19:00',
                'popolare': False
            },
            {
                'id': 5,
                'titolo': 'Weekend Special',
                'descrizione': '3 Pizze medie al prezzo di 2',
                'prezzo_originale': 36.00,
                'prezzo_scontato': 24.00,
                'sconto_percentuale': 33,
                'validita': 'Solo Weekend',
                'codice_promo': 'WEEKEND3X2',
                'condizioni': 'Valido sabato e domenica',
                'popolare': True
            }
        ],
        'codici_sconto': [
            {
                'codice': 'BENVENUTO10',
                'descrizione': '10% di sconto primo ordine',
                'tipo': 'Nuovo cliente'
            },
            {
                'codice': 'FEDELE20',
                'descrizione': '20% di sconto dopo 10 ordini',
                'tipo': 'Cliente fedele'
            },
            {
                'codice': 'COMPLEANNO',
                'descrizione': 'Pizza gratis nel tuo compleanno',
                'tipo': 'Speciale'
            }
        ]
    }
    
    return render(request, 'pages/offers.html', contesto_pagina)

@require_http_methods(["GET", "POST"])
def verifica_zona_consegna(request):
    """
    Verifica se un indirizzo è nella zona di consegna
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            indirizzo_utente = data.get('indirizzo', '').strip()
            cap_utente = data.get('cap', '').strip()
            citta_utente = data.get('citta', '').strip()
            
            # Zone servite con dettagli (in produzione: da database)
            zone_servite = {
                '16121': {
                    'nome': 'Centro Storico',
                    'costo_consegna': 3.00,
                    'tempo_minimo': 20,
                    'tempo_massimo': 30,
                    'note': 'Zona a traffico limitato'
                },
                '16122': {
                    'nome': 'Brera',
                    'costo_consegna': 3.50,
                    'tempo_minimo': 25,
                    'tempo_massimo': 35,
                    'note': 'Zona residenziale'
                },
                '16123': {
                    'nome': 'Spianata Castelletto',
                    'costo_consegna': 4.00,
                    'tempo_minimo': 30,
                    'tempo_massimo': 40,
                    'note': 'Zona collinare'
                },
                '16124': {
                    'nome': 'Foce',
                    'costo_consegna': 3.50,
                    'tempo_minimo': 25,
                    'tempo_massimo': 35,
                    'note': 'Zona mare'
                },
                '16125': {
                    'nome': 'Albaro',
                    'costo_consegna': 4.50,
                    'tempo_minimo': 35,
                    'tempo_massimo': 45,
                    'note': 'Zona periferica'
                }
            }
            
            if cap_utente in zone_servite:
                zona = zone_servite[cap_utente]
                return JsonResponse({
                    'zona_coperta': True,
                    'zona_nome': zona['nome'],
                    'costo_consegna': zona['costo_consegna'],
                    'tempo_consegna_min': zona['tempo_minimo'],
                    'tempo_consegna_max': zona['tempo_massimo'],
                    'tempo_stimato': f"{zona['tempo_minimo']}-{zona['tempo_massimo']} minuti",
                    'note': zona['note'],
                    'ordine_minimo': 8.00,
                    'messaggio': f'Ottimo! Consegniamo in {zona["nome"]}'
                })
            else:
                # Suggerisci zone vicine
                zone_vicine = ['16121', '16122', '16123'] if cap_utente.startswith('16') else []
                
                return JsonResponse({
                    'zona_coperta': False,
                    'messaggio': 'Spiacenti, non consegniamo ancora nella tua zona',
                    'zone_vicine': zone_vicine,
                    'contatto_support': 'Contatta il supporto per maggiori informazioni',
                    'espansione_prevista': 'Stiamo valutando l\'espansione in nuove zone'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'errore': 'Formato dati non valido'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'errore': 'Errore nella verifica zona',
                'dettaglio': str(e)
            }, status=500)
    
    # GET - Mostra pagina verifica zona
    contesto_pagina = {
        'titolo_pagina': 'Verifica Zona Consegna - PizzaMama',
        'descrizione_meta': 'Verifica se il tuo indirizzo è coperto dal servizio di consegna PizzaMama.',
        'zone_principali': [
            {'nome': 'Centro Storico', 'cap': '16121', 'costo': '3.00€'},
            {'nome': 'Brera', 'cap': '16122', 'costo': '3.50€'},
            {'nome': 'Spianata Castelletto', 'cap': '16123', 'costo': '4.00€'},
            {'nome': 'Foce', 'cap': '16124', 'costo': '3.50€'},
            {'nome': 'Albaro', 'cap': '16125', 'costo': '4.50€'}
        ],
        'info_consegna': {
            'ordine_minimo': '8.00€',
            'tempo_standard': '20-35 minuti',
            'orari_consegna': '11:00 - 23:00',
            'mezzi_trasporto': 'Scooter ecologici'
        }
    }
    
    return render(request, 'pages/delivery_zone.html', contesto_pagina)

@csrf_exempt
@require_http_methods(["POST"])
def contatto_form_submit(request):
    """
    Gestione invio form contatti
    """
    try:
        data = json.loads(request.body)
        
        # Validazione campi obbligatori
        campi_obbligatori = ['nome', 'email', 'messaggio']
        for campo in campi_obbligatori:
            if not data.get(campo, '').strip():
                return JsonResponse({
                    'errore': f'Il campo {campo} è obbligatorio'
                }, status=400)
        
        nome = data.get('nome').strip()
        email = data.get('email').strip()
        telefono = data.get('telefono', '').strip()
        motivo = data.get('motivo', 'Informazioni generali')
        messaggio = data.get('messaggio').strip()
        
        # Validazione email
        if '@' not in email or '.' not in email:
            return JsonResponse({
                'errore': 'Email non valida'
            }, status=400)
        
        # Invia email al supporto
        try:
            subject = f'Nuovo messaggio da {nome} - {motivo}'
            message = f"""
Nuovo messaggio dal form contatti:

Nome: {nome}
Email: {email}
Telefono: {telefono}
Motivo: {motivo}

Messaggio:
{messaggio}

---
Inviato dal sito PizzaMama
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['support@pizzamama.it'],
                fail_silently=False,
            )
            
            # Email di conferma al cliente
            send_mail(
                'Messaggio ricevuto - PizzaMama',
                f'''Ciao {nome},

Abbiamo ricevuto il tuo messaggio e ti risponderemo entro 24 ore.

Riepilogo del tuo messaggio:
Motivo: {motivo}
Messaggio: {messaggio}

Grazie per averci contattato!

Il Team PizzaMama
''',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            
        except Exception as e:
            print(f"Errore invio email: {e}")
            # Non bloccare il processo se l'email fallisce
        
        return JsonResponse({
            'successo': True,
            'messaggio': 'Messaggio inviato con successo! Ti risponderemo entro 24 ore.',
            'id_ticket': f'TK{hash(nome + email) % 10000:04d}'  # ID ticket simulato
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'errore': 'Formato dati non valido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'errore': 'Errore nell\'invio del messaggio',
            'dettaglio': str(e)
        }, status=500)

@require_http_methods(["GET"])
def api_info_azienda(request):
    """
    API per informazioni aziendali (per footer, widget, etc.)
    """
    try:
        info = {
            'nome_azienda': 'PizzaMama',
            'slogan': 'La Pizza Perfetta, Consegnata a Casa Tua',
            'anno_fondazione': 2020,
            'telefono': '+39 010 123 4567',
            'email': 'info@pizzamama.it',
            'indirizzo': 'Via Roma 123, 16121 Genova (GE)',
            'partita_iva': 'IT12345678901',
            'orari': {
                'lunedi_venerdi': '11:00 - 23:00',
                'sabato_domenica': '11:00 - 24:00',
                'note': 'Chiusi il lunedì mattina'
            },
            'social_media': {
                'facebook': 'https://facebook.com/pizzamamagenova',
                'instagram': 'https://instagram.com/pizzamamagenova',
                'twitter': 'https://twitter.com/pizzamamagenova',
                'whatsapp': '+39 010 123 4567'
            },
            'statistiche': {
                'pizze_consegnate': '50000+',
                'clienti_attivi': '15000+',
                'anni_esperienza': 5,
                'zone_servite': 5
            },
            'certificazioni': [
                'ISO 22000 - Sicurezza Alimentare',
                'Certificazione Bio',
                'HACCP Compliant'
            ]
        }
        
        return JsonResponse({
            'successo': True,
            'info_azienda': info
        })
        
    except Exception as e:
        return JsonResponse({
            'errore': 'Errore nel caricamento informazioni',
            'dettaglio': str(e)
        }, status=500)

# ========================================
# GESTIONE ERRORI PERSONALIZZATE - STEP 12
# ========================================

def pagina_non_trovata(request, exception):
    """
    Handler personalizzato per errore 404 - Pagina non trovata
    """
    contesto_errore = {
        'titolo_pagina': 'Pagina Non Trovata - PizzaMama',
        'codice_errore': '404',
        'titolo_errore': 'Oops! Pagina Non Trovata',
        'messaggio_errore': 'La pagina che stai cercando non esiste o è stata spostata.',
        'icona_errore': '🍕',
        'suggerimenti': [
            {
                'testo': 'Torna alla Homepage',
                'url': '/',
                'icona': '🏠',
                'descrizione': 'Vai alla pagina principale'
            },
            {
                'testo': 'Sfoglia il Catalogo',
                'url': '/catalogo/',
                'icona': '📋',
                'descrizione': 'Scopri le nostre pizze'
            },
            {
                'testo': 'Contattaci',
                'url': '/contatti/',
                'icona': '📞',
                'descrizione': 'Hai bisogno di aiuto?'
            }
        ],
        'ricerche_popolari': [
            'Margherita', 'Diavola', 'Quattro Stagioni', 'Vegetariana'
        ],
        'messaggio_divertente': 'Sembra che questa pagina sia andata a fare una passeggiata... come le nostre pizze! 🚚'
    }
    
    return render(request, 'errors/404.html', contesto_errore, status=404)

def errore_server(request):
    """
    Handler personalizzato per errore 500 - Errore interno server
    """
    contesto_errore = {
        'titolo_pagina': 'Errore Server - PizzaMama',
        'codice_errore': '500',
        'titolo_errore': 'Errore Interno del Server',
        'messaggio_errore': 'Si è verificato un errore interno. Il nostro team è stato notificato automaticamente.',
        'icona_errore': '🔧',
        'suggerimenti': [
            {
                'testo': 'Riprova tra qualche minuto',
                'url': '',
                'icona': '🔄',
                'descrizione': 'Il problema potrebbe essere temporaneo'
            },
            {
                'testo': 'Torna alla Homepage',
                'url': '/',
                'icona': '🏠',
                'descrizione': 'Ricomincia dalla pagina principale'
            },
            {
                'testo': 'Contatta l\'Assistenza',
                'url': '/contatti/',
                'icona': '📞',
                'descrizione': 'Il nostro team ti aiuterà'
            }
        ],
        'contatto_urgente': {
            'telefono': '+39 010 123 4567',
            'email': 'support@pizzamama.it',
            'orari': '11:00 - 23:00 tutti i giorni'
        },
        'messaggio_tecnico': 'I nostri tecnici stanno lavorando per risolvere il problema. Ci scusiamo per il disagio.'
    }
    
    return render(request, 'errors/500.html', contesto_errore, status=500)

def accesso_negato(request, exception):
    """
    Handler personalizzato per errore 403 - Accesso negato
    """
    contesto_errore = {
        'titolo_pagina': 'Accesso Negato - PizzaMama',
        'codice_errore': '403',
        'titolo_errore': 'Accesso Negato',
        'messaggio_errore': 'Non hai i permessi necessari per accedere a questa pagina.',
        'icona_errore': '🚫',
        'suggerimenti': [
            {
                'testo': 'Effettua il Login',
                'url': '/utente/login/',
                'icona': '👤',
                'descrizione': 'Accedi al tuo account'
            },
            {
                'testo': 'Registrati',
                'url': '/utente/registrazione/',
                'icona': '📝',
                'descrizione': 'Crea un nuovo account'
            },
            {
                'testo': 'Torna alla Homepage',
                'url': '/',
                'icona': '🏠',
                'descrizione': 'Vai alla pagina principale'
            },
            {
                'testo': 'Contattaci',
                'url': '/contatti/',
                'icona': '📞',
                'descrizione': 'Segnala il problema'
            }
        ],
        'info_account': {
            'vantaggi_registrazione': [
                'Tracciamento ordini in tempo reale',
                'Punti fedeltà e sconti esclusivi',
                'Salvataggio indirizzi preferiti',
                'Accesso a offerte speciali'
            ]
        }
    }
    
    return render(request, 'errors/403.html', contesto_errore, status=403)

def richiesta_non_valida(request, exception):
    """
    Handler personalizzato per errore 400 - Richiesta non valida
    """
    contesto_errore = {
        'titolo_pagina': 'Richiesta Non Valida - PizzaMama',
        'codice_errore': '400',
        'titolo_errore': 'Richiesta Non Valida',
        'messaggio_errore': 'La richiesta inviata non è valida o contiene errori nei dati.',
        'icona_errore': '⚠️',
        'suggerimenti': [
            {
                'testo': 'Riprova',
                'url': '',
                'icona': '🔄',
                'descrizione': 'Controlla i dati inseriti'
            },
            {
                'testo': 'Torna alla Homepage',
                'url': '/',
                'icona': '🏠',
                'descrizione': 'Ricomincia dall\'inizio'
            },
            {
                'testo': 'Consulta la Guida',
                'url': '/contatti/',
                'icona': '❓',
                'descrizione': 'Come utilizzare il sito'
            }
        ],
        'possibili_cause': [
            'Dati del form non compilati correttamente',
            'Connessione internet instabile',
            'Sessione scaduta - prova a ricaricare la pagina',
            'Browser non aggiornato'
        ]
    }
    
    return render(request, 'errors/400.html', contesto_errore, status=400)

# ========================================
# UTILITY FUNCTIONS
# ========================================

def get_business_info():
    """
    Funzione utility per ottenere informazioni business
    """
    return {
        'nome': 'PizzaMama',
        'telefono': '+39 010 123 4567',
        'email': 'info@pizzamama.it',
        'indirizzo': 'Via Roma 123, 16121 Genova (GE)',
        'orari': {
            'feriali': '11:00 - 23:00',
            'weekend': '11:00 - 24:00'
        },
        'social': {
            'facebook': 'pizzamamagenova',
            'instagram': 'pizzamamagenova',
            'twitter': 'pizzamamagenova'
        }
    }

def get_seo_defaults():
    """
    Funzione utility per default SEO
    """
    return {
        'site_name': 'PizzaMama',
        'default_description': 'La migliore pizza a domicilio di Genova. Ingredienti freschi, consegna veloce.',
        'default_keywords': 'pizza, domicilio, genova, consegna, italiana, napoletana',
        'og_image': '/static/images/logo-pizzamama-og.jpg',
        'twitter_site': '@pizzamamagenova'
    }