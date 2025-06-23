from flask import Blueprint, render_template, request, session, redirect, url_for
import os

# Istanze di test
from gioco.personaggio import Personaggio
from gioco.classi import Mago, Guerriero, Ladro
# from gioco.menu_principale import MenuPrincipale
# from gioco.missione import MissioneFactory
# from gioco.ambiente import AmbienteFactory
# from gioco.scontro import Scontro

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
gioco_bp = Blueprint('gioco', __name__, template_folder=template_dir)

# Home Page
@gioco_bp.route('/')
def index():
    return render_template('index.html')

# About
@gioco_bp.route('/about')
def about():
    return render_template('about.html')

# Guide Game
@gioco_bp.route('/guide_game')
def guide_game():
    return render_template('guide_game.html')

# Credits
@gioco_bp.route("/credits")
def credits():
    return render_template("credits.html")

# Menu principale
@gioco_bp.route('/menu')
def menu():
    return render_template('menu.html')

# Route del Debug
@gioco_bp.route('/debug')
def debug():
    if not session.get('debug_mode'):
        return redirect(url_for('gioco.index'))
    return render_template('debug.html', session_data=session)

# Mostra i log dello scontro
@gioco_bp.route('/battle', methods=['GET', 'POST'])
def battle():
    personaggio_attivo = ""
    nome_personaggio_attivo = "Genoveffo"
    buttons_diasable = True
    return render_template('battle.html', nome_personaggio_attivo=nome_personaggio_attivo)

# Test Inventario
@gioco_bp.route('/test-inventory', methods=['GET', 'POST'])
def test_inventory():
    pg_nome = "Gandalf"
    oggetti = [
        {"nome": "Pozione di Guarigione"},
        {"nome": "Pergamena Magica"},
        {"nome": "Antidoto"}
    ]
    oggetto_selezionato = None
    bersagli = []
    messaggio = None

    if request.method == 'POST':
        if 'action' in request.form and request.form['action'] == 'close':
            return redirect(url_for('gioco.index'))

    oggetto = request.form.get('oggetto')
    if oggetto:
        oggetto_selezionato = oggetto
        bersagli = [
            {"nome": "Frodo", "salute": 50, "salute_max": 80, "classe": "Hobbit", "tipologia": "Alleato"},
            {"nome": "Orco", "salute": 30, "salute_max": 60, "classe": "Guerriero", "tipologia": "Nemico"}
        ]

    bersaglio = request.form.get('bersaglio')
    if oggetto and bersaglio:
        messaggio = f"{pg_nome} usa {oggetto} su {bersaglio}! Successo!"

    return render_template('inventory.html',
                           pg_nome=pg_nome,
                           oggetti=oggetti,
                           oggetto_selezionato=oggetto_selezionato,
                           bersagli=bersagli,
                           messaggio=messaggio)

# --- ROUTE COMMENTATE CHE VUOI TENERE PER IL FUTURO ---

"""
# Nuovo gioco: form per creare la compagnia (1-3 PG)
@gioco_bp.route('/new-game', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        personaggi_info = []
        initial_gifts = []
        for i in range(1, 4):
            nome = request.form.get(f'pg{i}_nome')
            cls  = request.form.get(f'pg{i}_classe')
            gift = request.form.get(f'gift_{i}')
            if nome and cls:
                personaggi_info.append({"nome": nome, "classe": cls})
                initial_gifts.append(gift)
        mp = MenuPrincipale()
        compagnia = mp.crea_compagnia(personaggi_info, initial_gifts)
        missione = None
        session['compagnia'] = mp.to_dict()
        return redirect(url_for('gioco_bp.select_mission'))

    classi = list(MenuPrincipale._classe_map.keys())
    gifts  = list(MenuPrincipale._oggetto_map.keys())
    return render_template('create_char.html', classi=classi, gifts=gifts)


# Seleziona missione e avvia Scontro
@gioco_bp.route('/select-mission', methods=['GET', 'POST'])
def select_mission():
    if 'compagnia' not in session:
        return redirect(url_for('gioco_bp.new_game'))

    if request.method == 'POST':
        missione_id = request.form['missione_id']
        missione = MissioneFactory.seleziona_da_id(missione_id)
        compagnia = MenuPrincipale.from_dict(session['compagnia']).personaggi_inventari
        s = Scontro(missione, compagnia)
        session['scontro'] = s.to_dict()
        return redirect(url_for('gioco_bp.battle'))

    missioni = MissioneFactory.get_opzioni()
    return render_template('select_mission.html', missioni=missioni)


# Carica gioco: form per caricare la compagnia e lo scontro precedente
@gioco_bp.route('/load-game', methods=['GET', 'POST'])
def load_game():
    if request.method == 'POST':
        mp = MenuPrincipale.carica_salvataggio()
"""
