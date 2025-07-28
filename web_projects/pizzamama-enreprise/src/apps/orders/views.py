# apps/orders/views.py
"""
🍕 PIZZAMAMA ENTERPRISE - Views Ordini Frontend
Views per gestione carrello e checkout
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import json
import uuid

from .models import Order, Cart, CartItem, Payment
from apps.products.models import Pizza
from apps.accounts.models import Address


def carrello_view(request):
    """
    View principale per la pagina del carrello
    """
    contesto_pagina = {
        'titolo_pagina': 'Carrello - PizzaMama',
        'descrizione_meta': 'Gestisci il tuo carrello e procedi all\'ordine',
        'breadcrumb': [
            {'nome': 'Home', 'url': '/'},
            {'nome': 'Catalogo', 'url': '/catalogo/'},
            {'nome': 'Carrello', 'attivo': True}
        ],
        
        # Configurazione checkout
        'config_checkout': {
            'costo_consegna_domicilio': 3.50,
            'costo_consegna_ritiro': 0.00,
            'tempo_consegna_domicilio': '25-35 minuti',
            'tempo_consegna_ritiro': '15-20 minuti',
            'metodi_pagamento_disponibili': [
                'carta', 'paypal', 'contrassegno'
            ],
            'importo_minimo_ordine': 8.00
        },
        
        # Codici sconto disponibili (per demo)
        'codici_sconto_demo': [
            'BENVENUTO10', 'PIZZA5', 'STUDENT15'
        ]
    }
    
    return render(request, 'carrello/carrello.html', contesto_pagina)


@csrf_exempt
@require_http_methods(["POST"])
def api_aggiungi_al_carrello(request):
    """
    API per aggiungere prodotti al carrello
    """
    try:
        dati = json.loads(request.body)
        pizza_id = dati.get('pizza_id')
        quantita = int(dati.get('quantita', 1))
        ingredienti_extra = dati.get('ingredienti_extra', [])
        note_speciali = dati.get('note_speciali', '')
        
        # Validazione
        if not pizza_id:
            return JsonResponse({
                'errore': 'ID pizza obbligatorio'
            }, status=400)
        
        if quantita < 1:
            return JsonResponse({
                'errore': 'Quantità deve essere maggiore di 0'
            }, status=400)
        
        pizza = get_object_or_404(Pizza, id=pizza_id, disponibile=True)
        
        # Calcola prezzo totale con ingredienti extra
        prezzo_base = pizza.prezzo
        prezzo_extra = Decimal('0.00')
        
        if ingredienti_extra:
            from apps.products.models import Ingredient
            for ingrediente_id in ingredienti_extra:
                try:
                    ingrediente = Ingredient.objects.get(
                        id=ingrediente_id,
                        disponibile=True,
                        extra=True
                    )
                    prezzo_extra += ingrediente.prezzo_extra or Decimal('0.00')
                except Ingredient.DoesNotExist:
                    continue
        
        prezzo_totale = (prezzo_base + prezzo_extra) * quantita
        
        # Gestione carrello sessione (per utenti non autenticati)
        if not request.user.is_authenticated:
            carrello_sessione = request.session.get('carrello', {})
            
            # Crea chiave univoca per l'elemento
            chiave_elemento = f"{pizza_id}_{hash(tuple(sorted(ingredienti_extra)))}"
            
            if chiave_elemento in carrello_sessione:
                carrello_sessione[chiave_elemento]['quantita'] += quantita
            else:
                carrello_sessione[chiave_elemento] = {
                    'pizza_id': pizza_id,
                    'nome_pizza': pizza.nome,
                    'prezzo_base': float(prezzo_base),
                    'prezzo_extra': float(prezzo_extra),
                    'quantita': quantita,
                    'ingredienti_extra': ingredienti_extra,
                    'note_speciali': note_speciali,
                    'immagine': pizza.immagine.url if pizza.immagine else None
                }
            
            request.session['carrello'] = carrello_sessione
            request.session.modified = True
            
            return JsonResponse({
                'successo': True,
                'messaggio': f'{pizza.nome} aggiunta al carrello',
                'carrello': {
                    'elementi_totali': sum(item['quantita'] for item in carrello_sessione.values()),
                    'totale': sum(
                        (item['prezzo_base'] + item['prezzo_extra']) * item['quantita']
                        for item in carrello_sessione.values()
                    )
                }
            })
        
        # Gestione carrello database (per utenti autenticati)
        else:
            carrello, creato = Cart.objects.get_or_create(
                utente=request.user,
                attivo=True
            )
            
            # Verifica se elemento già esistente
            elemento_esistente = CartItem.objects.filter(
                carrello=carrello,
                pizza=pizza,
                note_speciali=note_speciali
            ).first()
            
            if elemento_esistente:
                elemento_esistente.quantita += quantita
                elemento_esistente.save()
            else:
                CartItem.objects.create(
                    carrello=carrello,
                    pizza=pizza,
                    quantita=quantita,
                    prezzo_unitario=prezzo_base + prezzo_extra,
                    note_speciali=note_speciali
                )
            
            # Aggiorna totale carrello
            carrello.aggiorna_totale()
            
            return JsonResponse({
                'successo': True,
                'messaggio': f'{pizza.nome} aggiunta al carrello',
                'carrello': {
                    'elementi_totali': carrello.elementi_totali(),
                    'totale': float(carrello.totale)
                }
            })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'errore': 'Formato dati non valido'
        }, status=400)
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nell\'aggiunta al carrello',
            'dettaglio': str(errore)
        }, status=500)


@require_http_methods(["GET"])
def api_contenuto_carrello(request):
    """
    API per ottenere il contenuto del carrello
    """
    try:
        if not request.user.is_authenticated:
            # Carrello da sessione
            carrello_sessione = request.session.get('carrello', {})
            
            elementi = []
            for chiave, item in carrello_sessione.items():
                elementi.append({
                    'id': chiave,
                    'pizza_id': item['pizza_id'],
                    'nome': item['nome_pizza'],
                    'prezzo_unitario': item['prezzo_base'] + item['prezzo_extra'],
                    'quantita': item['quantita'],
                    'prezzo_totale': (item['prezzo_base'] + item['prezzo_extra']) * item['quantita'],
                    'immagine': item['immagine'],
                    'ingredienti_extra': item['ingredienti_extra'],
                    'note_speciali': item['note_speciali']
                })
            
            totale_generale = sum(elem['prezzo_totale'] for elem in elementi)
            
            return JsonResponse({
                'elementi': elementi,
                'totale': totale_generale,
                'elementi_totali': sum(elem['quantita'] for elem in elementi),
                'vuoto': len(elementi) == 0
            })
        
        # Carrello da database
        else:
            try:
                carrello = Cart.objects.get(utente=request.user, attivo=True)
                elementi = []
                
                for item in carrello.items.all():
                    elementi.append({
                        'id': item.id,
                        'pizza_id': item.pizza.id,
                        'nome': item.pizza.nome,
                        'prezzo_unitario': float(item.prezzo_unitario),
                        'quantita': item.quantita,
                        'prezzo_totale': float(item.prezzo_totale()),
                        'immagine': item.pizza.immagine.url if item.pizza.immagine else None,
                        'note_speciali': item.note_speciali,
                        'data_aggiunta': item.data_aggiunta.isoformat()
                    })
                
                return JsonResponse({
                    'elementi': elementi,
                    'totale': float(carrello.totale),
                    'elementi_totali': carrello.elementi_totali(),
                    'vuoto': not elementi
                })
                
            except Cart.DoesNotExist:
                return JsonResponse({
                    'elementi': [],
                    'totale': 0,
                    'elementi_totali': 0,
                    'vuoto': True
                })
    
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento carrello',
            'dettaglio': str(errore)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_aggiorna_quantita(request):
    """
    API per aggiornare la quantità di un elemento del carrello
    """
    try:
        dati = json.loads(request.body)
        elemento_id = dati.get('elemento_id')
        nuova_quantita = int(dati.get('quantita', 1))
        
        if nuova_quantita < 0:
            return JsonResponse({
                'errore': 'Quantità non può essere negativa'
            }, status=400)
        
        if not request.user.is_authenticated:
            # Carrello sessione
            carrello_sessione = request.session.get('carrello', {})
            
            if elemento_id in carrello_sessione:
                if nuova_quantita == 0:
                    del carrello_sessione[elemento_id]
                else:
                    carrello_sessione[elemento_id]['quantita'] = nuova_quantita
                
                request.session['carrello'] = carrello_sessione
                request.session.modified = True
                
                return JsonResponse({
                    'successo': True,
                    'messaggio': 'Quantità aggiornata'
                })
            else:
                return JsonResponse({
                    'errore': 'Elemento non trovato'
                }, status=404)
        
        # Carrello database
        else:
            try:
                carrello = Cart.objects.get(utente=request.user, attivo=True)
                elemento = CartItem.objects.get(id=elemento_id, carrello=carrello)
                
                if nuova_quantita == 0:
                    elemento.delete()
                else:
                    elemento.quantita = nuova_quantita
                    elemento.save()
                
                carrello.aggiorna_totale()
                
                return JsonResponse({
                    'successo': True,
                    'messaggio': 'Quantità aggiornata'
                })
                
            except (Cart.DoesNotExist, CartItem.DoesNotExist):
                return JsonResponse({
                    'errore': 'Elemento non trovato'
                }, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'errore': 'Formato dati non valido'
        }, status=400)
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nell\'aggiornamento quantità',
            'dettaglio': str(errore)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_rimuovi_dal_carrello(request):
    """
    API per rimuovere un elemento dal carrello
    """
    try:
        dati = json.loads(request.body)
        elemento_id = dati.get('elemento_id')
        
        if not request.user.is_authenticated:
            # Carrello sessione
            carrello_sessione = request.session.get('carrello', {})
            
            if elemento_id in carrello_sessione:
                nome_elemento = carrello_sessione[elemento_id]['nome_pizza']
                del carrello_sessione[elemento_id]
                
                request.session['carrello'] = carrello_sessione
                request.session.modified = True
                
                return JsonResponse({
                    'successo': True,
                    'messaggio': f'{nome_elemento} rimossa dal carrello'
                })
            else:
                return JsonResponse({
                    'errore': 'Elemento non trovato'
                }, status=404)
        
        # Carrello database
        else:
            try:
                carrello = Cart.objects.get(utente=request.user, attivo=True)
                elemento = CartItem.objects.get(id=elemento_id, carrello=carrello)
                
                nome_elemento = elemento.pizza.nome
                elemento.delete()
                carrello.aggiorna_totale()
                
                return JsonResponse({
                    'successo': True,
                    'messaggio': f'{nome_elemento} rimossa dal carrello'
                })
                
            except (Cart.DoesNotExist, CartItem.DoesNotExist):
                return JsonResponse({
                    'errore': 'Elemento non trovato'
                }, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'errore': 'Formato dati non valido'
        }, status=400)
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nella rimozione elemento',
            'dettaglio': str(errore)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_svuota_carrello(request):
    """
    API per svuotare completamente il carrello
    """
    try:
        if not request.user.is_authenticated:
            # Svuota carrello sessione
            request.session['carrello'] = {}
            request.session.modified = True
        else:
            # Svuota carrello database
            try:
                carrello = Cart.objects.get(utente=request.user, attivo=True)
                carrello.items.all().delete()
                carrello.aggiorna_totale()
            except Cart.DoesNotExist:
                pass  # Carrello già vuoto
        
        return JsonResponse({
            'successo': True,
            'messaggio': 'Carrello svuotato con successo'
        })
    
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nello svuotamento carrello',
            'dettaglio': str(errore)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_applica_codice_sconto(request):
    """
    API per applicare un codice sconto
    """
    try:
        dati = json.loads(request.body)
        codice = dati.get('codice', '').strip().upper()
        
        # Codici sconto disponibili (in produzione andrebbero in database)
        codici_validi = {
            'BENVENUTO10': {
                'tipo': 'percentuale',
                'valore': 10,
                'descrizione': '10% di sconto di benvenuto',
                'importo_minimo': 15.00
            },
            'PIZZA5': {
                'tipo': 'fisso',
                'valore': 5.00,
                'descrizione': '5€ di sconto',
                'importo_minimo': 20.00
            },
            'STUDENT15': {
                'tipo': 'percentuale',
                'valore': 15,
                'descrizione': '15% sconto studenti',
                'importo_minimo': 12.00
            }
        }
        
        if codice not in codici_validi:
            return JsonResponse({
                'errore': 'Codice sconto non valido o scaduto'
            }, status=400)
        
        sconto_info = codici_validi[codice]
        
        # Verifica importo minimo (qui dovremmo controllare il totale carrello)
        # Per semplicità assumiamo che il controllo sia fatto dal frontend
        
        return JsonResponse({
            'successo': True,
            'sconto': {
                'codice': codice,
                'tipo': sconto_info['tipo'],
                'valore': sconto_info['valore'],
                'descrizione': sconto_info['descrizione']
            },
            'messaggio': f"Codice sconto '{codice}' applicato con successo"
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'errore': 'Formato dati non valido'
        }, status=400)
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nell\'applicazione sconto',
            'dettaglio': str(errore)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_crea_ordine(request):
    """
    API per creare un nuovo ordine dal carrello
    """
    try:
        dati = json.loads(request.body)
        
        # Validazione dati obbligatori
        dati_richiesti = [
            'indirizzo_consegna', 'modalita_consegna', 'metodo_pagamento'
        ]
        
        for campo in dati_richiesti:
            if campo not in dati:
                return JsonResponse({
                    'errore': f'Campo {campo} obbligatorio'
                }, status=400)
        
        # Genera numero ordine univoco
        numero_ordine = f"PM{timezone.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
        
        # Calcola totali
        subtotale = Decimal(str(dati.get('subtotale', 0)))
        costo_consegna = Decimal('3.50') if dati['modalita_consegna'] == 'domicilio' else Decimal('0.00')
        sconto = Decimal(str(dati.get('sconto_importo', 0)))
        totale = subtotale + costo_consegna - sconto
        
        # Crea ordine
        ordine_data = {
            'numero_ordine': numero_ordine,
            'utente': request.user if request.user.is_authenticated else None,
            'email_contatto': dati['indirizzo_consegna'].get('email', ''),
            'telefono_contatto': dati['indirizzo_consegna']['telefono'],
            'stato': 'ricevuto',
            'tipo_consegna': dati['modalita_consegna'],
            'subtotale': subtotale,
            'costo_consegna': costo_consegna,
            'sconto': sconto,
            'totale': totale,
            'note_ordine': dati.get('note_ordine', ''),
            'indirizzo_consegna': json.dumps(dati['indirizzo_consegna'], ensure_ascii=False),
            'data_consegna_prevista': timezone.now() + timezone.timedelta(minutes=30)
        }
        
        ordine = Order.objects.create(**ordine_data)
        
        # Aggiungi elementi ordine dal carrello
        elementi_carrello = dati.get('elementi_carrello', [])
        
        for elemento in elementi_carrello:
            try:
                pizza = Pizza.objects.get(id=elemento['pizza_id'])
                # Qui creeresti OrderItem (da implementare nel model)
                # OrderItem.objects.create(...)
            except Pizza.DoesNotExist:
                continue
        
        # Crea record pagamento
        pagamento_data = {
            'ordine': ordine,
            'metodo': dati['metodo_pagamento'],
            'importo': totale,
            'stato': 'in_attesa' if dati['metodo_pagamento'] != 'contrassegno' else 'completato',
            'id_transazione': str(uuid.uuid4())
        }
        
        pagamento = Payment.objects.create(**pagamento_data)
        
        # Svuota carrello dopo ordine confermato
        if request.user.is_authenticated:
            try:
                carrello = Cart.objects.get(utente=request.user, attivo=True)
                carrello.attivo = False
                carrello.save()
            except Cart.DoesNotExist:
                pass
        else:
            request.session['carrello'] = {}
            request.session.modified = True
        
        # Invia email di conferma (opzionale)
        if ordine.email_contatto:
            try:
                invia_email_conferma_ordine(ordine)
            except Exception as e:
                # Log errore ma non bloccare il processo
                print(f"Errore invio email: {e}")
        
        return JsonResponse({
            'successo': True,
            'ordine': {
                'numero_ordine': numero_ordine,
                'id': ordine.id,
                'totale': float(totale),
                'stato': ordine.stato,
                'tempo_consegna_stimato': '25-35 minuti' if dati['modalita_consegna'] == 'domicilio' else '15-20 minuti'
            },
            'messaggio': f'Ordine {numero_ordine} creato con successo'
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'errore': 'Formato dati non valido'
        }, status=400)
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nella creazione ordine',
            'dettaglio': str(errore)
        }, status=500)


@require_http_methods(["GET"])
def api_stato_ordine(request, numero_ordine):
    """
    API per ottenere lo stato di un ordine
    """
    try:
        ordine = get_object_or_404(Order, numero_ordine=numero_ordine)
        
        # Verifica autorizzazione
        if request.user.is_authenticated and ordine.utente != request.user:
            return JsonResponse({
                'errore': 'Non autorizzato'
            }, status=403)
        
        return JsonResponse({
            'ordine': {
                'numero_ordine': ordine.numero_ordine,
                'stato': ordine.stato,
                'stato_display': ordine.get_stato_display(),
                'data_ordine': ordine.data_ordine.isoformat(),
                'data_consegna_prevista': ordine.data_consegna_prevista.isoformat() if ordine.data_consegna_prevista else None,
                'tipo_consegna': ordine.tipo_consegna,
                'totale': float(ordine.totale),
                'telefono_contatto': ordine.telefono_contatto,
                'note_ordine': ordine.note_ordine
            }
        })
    
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento stato ordine',
            'dettaglio': str(errore)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def api_storico_ordini(request):
    """
    API per ottenere lo storico ordini dell'utente
    """
    try:
        ordini = Order.objects.filter(utente=request.user).order_by('-data_ordine')
        
        # Paginazione
        from django.core.paginator import Paginator
        paginator = Paginator(ordini, 10)
        pagina = request.GET.get('pagina', 1)
        ordini_paginati = paginator.get_page(pagina)
        
        risultati = []
        for ordine in ordini_paginati:
            risultati.append({
                'id': ordine.id,
                'numero_ordine': ordine.numero_ordine,
                'data_ordine': ordine.data_ordine.isoformat(),
                'stato': ordine.stato,
                'stato_display': ordine.get_stato_display(),
                'totale': float(ordine.totale),
                'tipo_consegna': ordine.tipo_consegna,
                'elementi_count': 0  # Implementare con OrderItem
            })
        
        return JsonResponse({
            'ordini': risultati,
            'paginazione': {
                'pagina_corrente': ordini_paginati.number,
                'pagine_totali': paginator.num_pages,
                'totale_ordini': paginator.count
            }
        })
    
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento storico ordini',
            'dettaglio': str(errore)
        }, status=500)


def invia_email_conferma_ordine(ordine):
    """
    Funzione per inviare email di conferma ordine
    """
    try:
        indirizzo_data = json.loads(ordine.indirizzo_consegna)
        
        soggetto = f'Conferma Ordine #{ordine.numero_ordine} - PizzaMama'
        
        messaggio = f"""
        Ciao {indirizzo_data.get('nome', '')},
        
        Il tuo ordine #{ordine.numero_ordine} è stato ricevuto con successo!
        
        Dettagli Ordine:
        - Numero: {ordine.numero_ordine}
        - Totale: €{ordine.totale}
        - Modalità: {ordine.get_tipo_consegna_display()}
        - Stato: {ordine.get_stato_display()}
        
        Tempo stimato: {'25-35 minuti' if ordine.tipo_consegna == 'domicilio' else '15-20 minuti'}
        
        Riceverai un SMS di aggiornamento quando l'ordine sarà in preparazione.
        
        Grazie per aver scelto PizzaMama!
        
        Il Team PizzaMama
        """
        
        send_mail(
            soggetto,
            messaggio,
            settings.DEFAULT_FROM_EMAIL,
            [ordine.email_contatto],
            fail_silently=False,
        )
        
    except Exception as e:
        # Log dell'errore in produzione
        print(f"Errore invio email conferma ordine {ordine.numero_ordine}: {e}")
        raise


@require_http_methods(["GET"])
def api_metodi_pagamento(request):
    """
    API per ottenere i metodi di pagamento disponibili
    """
    try:
        metodi = [
            {
                'id': 'carta',
                'nome': 'Carta di Credito/Debito',
                'descrizione': 'Visa, Mastercard, American Express',
                'icona': 'fab fa-cc-visa',
                'commissione': 0,
                'disponibile': True
            },
            {
                'id': 'paypal',
                'nome': 'PayPal',
                'descrizione': 'Paga con il tuo account PayPal',
                'icona': 'fab fa-paypal',
                'commissione': 0,
                'disponibile': True
            },
            {
                'id': 'contrassegno',
                'nome': 'Contrassegno',
                'descrizione': 'Paga alla consegna in contanti',
                'icona': 'fas fa-money-bill-wave',
                'commissione': 2.00,
                'disponibile': True,
                'note': 'Commissione €2.00 per ordini sotto €25'
            }
        ]
        
        return JsonResponse({
            'metodi_pagamento': metodi
        })
    
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento metodi pagamento',
            'dettaglio': str(errore)
        }, status=500)


@require_http_methods(["GET"])
def api_zone_consegna(request):
    """
    API per verificare le zone di consegna disponibili
    """
    try:
        # Zone di consegna (in produzione da database)
        zone_consegna = [
            {
                'nome': 'Centro Milano',
                'cap': ['20121', '20122', '20123'],
                'costo': 3.50,
                'tempo_min': 25,
                'tempo_max': 35,
                'disponibile': True
            },
            {
                'nome': 'Zona Nord',
                'cap': ['20124', '20125', '20126'],
                'costo': 4.00,
                'tempo_min': 30,
                'tempo_max': 40,
                'disponibile': True
            },
            {
                'nome': 'Zona Sud',
                'cap': ['20135', '20136', '20137'],
                'costo': 4.00,
                'tempo_min': 30,
                'tempo_max': 40,
                'disponibile': True
            }
        ]
        
        # Controlla se è fornito un CAP specifico
        cap_richiesto = request.GET.get('cap')
        if cap_richiesto:
            for zona in zone_consegna:
                if cap_richiesto in zona['cap']:
                    return JsonResponse({
                        'disponibile': zona['disponibile'],
                        'zona': zona
                    })
            
            return JsonResponse({
                'disponibile': False,
                'messaggio': 'Zona non coperta dal servizio di consegna'
            })
        
        return JsonResponse({
            'zone_consegna': zone_consegna
        })
    
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento zone consegna',
            'dettaglio': str(errore)
        }, status=500)


@require_http_methods(["GET"])
def api_statistiche_ordini(request):
    """
    API per statistiche ordini (per admin/dashboard)
    """
    try:
        from django.db.models import Count, Sum, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        # Filtri temporali
        oggi = timezone.now().date()
        settimana_fa = oggi - timedelta(days=7)
        mese_fa = oggi - timedelta(days=30)
        
        # Statistiche base
        stats = {
            'oggi': {
                'ordini': Order.objects.filter(data_ordine__date=oggi).count(),
                'incasso': Order.objects.filter(
                    data_ordine__date=oggi,
                    stato__in=['completato', 'consegnato']
                ).aggregate(Sum('totale'))['totale__sum'] or 0
            },
            'settimana': {
                'ordini': Order.objects.filter(data_ordine__date__gte=settimana_fa).count(),
                'incasso': Order.objects.filter(
                    data_ordine__date__gte=settimana_fa,
                    stato__in=['completato', 'consegnato']
                ).aggregate(Sum('totale'))['totale__sum'] or 0
            },
            'mese': {
                'ordini': Order.objects.filter(data_ordine__date__gte=mese_fa).count(),
                'incasso': Order.objects.filter(
                    data_ordine__date__gte=mese_fa,
                    stato__in=['completato', 'consegnato']
                ).aggregate(Sum('totale'))['totale__sum'] or 0
            }
        }
        
        # Ordini per stato
        ordini_per_stato = dict(
            Order.objects.values('stato').annotate(
                count=Count('id')
            ).values_list('stato', 'count')
        )
        
        # Metodi pagamento più utilizzati
        metodi_pagamento = dict(
            Payment.objects.values('metodo').annotate(
                count=Count('id')
            ).values_list('metodo', 'count')
        )
        
        # Valore medio ordine
        valore_medio_ordine = Order.objects.filter(
            stato__in=['completato', 'consegnato']
        ).aggregate(Avg('totale'))['totale__avg'] or 0
        
        return JsonResponse({
            'statistiche': stats,
            'ordini_per_stato': ordini_per_stato,
            'metodi_pagamento': metodi_pagamento,
            'valore_medio_ordine': round(float(valore_medio_ordine), 2),
            'ultimo_aggiornamento': timezone.now().isoformat()
        })
    
    except Exception as errore:
        return JsonResponse({
            'errore': 'Errore nel caricamento statistiche',
            'dettaglio': str(errore)
        }, status=500)