"""
Main views per PizzaMama Enterprise - Step 12 Frontend

Views principali per homepage e pagine generali del sito.
Integrazione con API REST per dati dinamici.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

def home(request):
    """
    Homepage del sito PizzaMama Enterprise
    
    Mostra:
    - Hero section con call-to-action
    - Pizze in evidenza (featured)
    - Categorie principali
    - Testimonianze clienti
    """
    context = {
        'page_title': 'PizzaMama - La Miglior Pizza a Domicilio',
        'meta_description': 'Ordina la migliore pizza a domicilio. Ingredienti freschi, consegna veloce, prezzi imbattibili.',
        'hero_title': 'La Pizza Perfetta, Consegnata a Casa Tua',
        'hero_subtitle': 'Ingredienti freschi, ricette tradizionali e consegna veloce in tutta la città',
        'cta_text': 'Ordina Ora',
    }
    
    return render(request, 'pages/home.html', context)

def about(request):
    """
    Pagina Chi Siamo
    
    Racconta la storia di PizzaMama, i valori aziendali
    e l'impegno per la qualità.
    """
    context = {
        'page_title': 'Chi Siamo - PizzaMama',
        'meta_description': 'Scopri la storia di PizzaMama, la nostra passione per la pizza e l\'impegno per la qualità.',
        'company_story': {
            'founded': '2020',
            'pizzas_delivered': '50.000+',
            'happy_customers': '15.000+',
            'locations': '5 città'
        }
    }
    
    return render(request, 'pages/about.html', context)

@login_required
def dashboard(request):
    """
    Dashboard utente con overview ordini e profilo
    
    Mostra statistiche personali dell'utente:
    - Ordini recenti
    - Punti fedeltà
    - Indirizzi salvati
    """
    user = request.user
    
    context = {
        'page_title': f'Dashboard - {user.get_full_name() or user.username}',
        'user': user,
        'has_profile': hasattr(user, 'profile'),
    }
    
    # Aggiungi dati profilo se esiste
    if hasattr(user, 'profile'):
        context.update({
            'loyalty_points': user.profile.loyalty_points,
            'total_orders': user.profile.total_orders,
            'total_spent': user.profile.total_spent,
        })
    
    return render(request, 'accounts/dashboard.html', context)

def search_suggestions(request):
    """
    API endpoint per suggerimenti di ricerca
    
    Ritorna JSON con suggerimenti basati su query utente
    per implementare autocomplete nella barra di ricerca.
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Simuliamo suggerimenti (in futuro integrazione con API search)
    suggestions = []
    
    # Pizza names suggestions
    pizza_suggestions = [
        'Margherita', 'Napoletana', 'Quattro Stagioni', 'Diavola',
        'Quattro Formaggi', 'Prosciutto e Funghi', 'Capricciosa',
        'Marinara', 'Vegetariana', 'Tonno e Cipolle'
    ]
    
    # Filtra suggerimenti basati su query
    matching_pizzas = [
        pizza for pizza in pizza_suggestions 
        if query.lower() in pizza.lower()
    ]
    
    suggestions.extend([
        {'type': 'pizza', 'text': pizza, 'url': f'/products/search/?q={pizza}'}
        for pizza in matching_pizzas[:5]
    ])
    
    # Category suggestions
    if 'classic' in query.lower() or 'tradizional' in query.lower():
        suggestions.append({
            'type': 'category', 
            'text': 'Pizze Classiche', 
            'url': '/products/category/classiche/'
        })
    
    if 'specia' in query.lower() or 'gourmet' in query.lower():
        suggestions.append({
            'type': 'category', 
            'text': 'Pizze Speciali', 
            'url': '/products/category/speciali/'
        })
    
    return JsonResponse({'suggestions': suggestions[:8]})

def contact(request):
    """
    Pagina contatti con form e informazioni
    """
    context = {
        'page_title': 'Contatti - PizzaMama',
        'meta_description': 'Contatta PizzaMama per informazioni, suggerimenti o assistenza clienti.',
        'contact_info': {
            'phone': '+39 010 123 4567',
            'email': 'info@pizzamama.it',
            'address': 'Via Roma 123, 16121 Genova (GE)',
            'hours': {
                'weekdays': '11:00 - 23:00',
                'weekend': '11:00 - 24:00'
            }
        }
    }
    
    return render(request, 'pages/contact.html', context)

def privacy_policy(request):
    """
    Pagina Privacy Policy per GDPR compliance
    """
    context = {
        'page_title': 'Privacy Policy - PizzaMama',
        'meta_description': 'Informativa sulla privacy e trattamento dati personali di PizzaMama.',
        'last_updated': '28 Luglio 2025'
    }
    
    return render(request, 'pages/privacy.html', context)

def terms_of_service(request):
    """
    Pagina Termini di Servizio
    """
    context = {
        'page_title': 'Termini di Servizio - PizzaMama',
        'meta_description': 'Termini e condizioni di utilizzo del servizio PizzaMama.',
        'last_updated': '28 Luglio 2025'
    }
    
    return render(request, 'pages/terms.html', context)