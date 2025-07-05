import os, json
from . import characters_bp
from flask import render_template, request, redirect, url_for, session, abort, flash
from gioco.personaggio import Personaggio
from gioco.oggetto import Oggetto
from gioco.inventario import Inventario
from utils.log import Log
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from auth.models import User
from auth.models import db
from auth.credits import credits_to_create, credits_to_refund
from config import DATA_DIR

# -------------------------LOAD CHAR----------------------------------
@characters_bp.route('load_char')
@login_required
def load_char():
    pass

# -------------------------CREAZIONE SINGLO FILE JSON------------------
def CreateJsonChar(pg_creato: Personaggio):
    pass

# -------------------------CREAZIONE PERSONAGGIO-------------------------
@characters_bp.route('/create_char', methods=['POST', 'GET'])
@login_required
def create_char():
    pass

# -------------------------EDIT PERSONAGGIO------------------------------
@characters_bp.route('/edit_cha/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_char(id):
    pass

# -------------------------RECUPERA PERSONAGGI----------------------------
@characters_bp.route('/recupera_personaggi_posseduti')
def recupera_personaggi_posseduti(owned_chars):
    pass 

# -------------------------MOSTRA PERSONAGGI----------------------------
@characters_bp.route('/personaggi', methods=['GET'])
def mostra_personaggi():
    pass

# -------------------------DETAGLI PERSONAGGIO----------------------------
@characters_bp.route('/personaggi/<string:char_id>', methods=['GET'])
@login_required
def dettaglio_personaggio(char_id):
    pass

# -------------------------ELIMINA PERSONAGGIO----------------------------
@characters_bp.route('/personaggi/<int:id>', methods=['POST'])
def elimina_personaggio(id):
    pass

# -------------------------INIZIA COMBATTIMENTO----------------------------
@characters_bp.route('/combattimento', methods=['GET', 'POST'])
def inizio_combattimento():
    pass
