from flask import Blueprint, render_template, request, session, redirect, url_for, flash

#from gioco.menu_principale import MenuPrincipale
#from gioco.missione import MissioneFactory
#from gioco.ambiente import AmbienteFactory
#from gioco.scontro import Scontro

gioco = Blueprint('gioco',
                  __name__,
                  template_folder='../templates')

# --------------- INDEX -------------------------------------
@gioco.route('/')
def index():
    return render_template('index.html')

# --------------- MENU ---------------------------------------
@gioco.route('/menu')
def menu():
    return render_template('menu.html')

# --------------- SELEZIONA_AMBIENTE -------------------------
@gioco.route('/seleziona_ambiente', methods=['GET', 'POST'])
def seleziona_ambiente():
    return render_template('seleziona_ambiente.html')

# --------------- CREA_PERSONAGGIO ---------------------------
@gioco.route('/crea_personaggio', methods=['GET', 'POST'])
def crea_personaggio():
    return render_template('crea_personaggi.html')

# --------------- INVENTARIO ---------------------------------
@gioco.route('/inventario', methods=['GET', 'POST'])
def inventario():
    return render_template('inventario.html')

# --------------- PERSONAGGI_CREATI--------------------------
@gioco.route('/personaggi_creati', methods=['GET', 'POST'])
def personaggi_creati():
    return render_template('personaggi_creati.html')

# --------------- BATTAGLIA --------------------------------
@gioco.route('/battaglia', methods=['GET', 'POST'])
def battaglia():
    return render_template('battaglia.html')

# --------------- NUOVA_PARTITA ----------------------------
@gioco.route('/nuova_partita', methods=['GET', 'POST'])
def nuova_partita():
    return render_template('nuova_partita.html')

# --------------- CARICA_PARTITA ---------------------------
@gioco.route('/carica_partita', methods=['GET', 'POST'])
def carica_partita():
    return render_template('carica_partita.html')

# --------------- SELZIONA_MISSIONE ------------------------
@gioco.route('/seleziona_missione', methods=['GET', 'POST'])
def seleziona_missione():
    return render_template('seleziona_missione.html')
