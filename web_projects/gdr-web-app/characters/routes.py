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
from config import DATA_JSON_DIR

classi = {cls.__name__: cls for cls in Personaggio.__subclasses__()}
oggetti = {ogg.__name__: ogg for ogg in Oggetto.__subclasses__()}

# -------------------------LOAD CHAR----------------------------------
@characters_bp.route('/load_char')
# @login_required
def load_char():
    pass

# -------------------------CREAZIONE SINGLO FILE JSON------------------
def CharSingleJson(pg_creato: Personaggio):
    """
    Salva su disco i dati di un personaggio in formato JSON.

    Questa funzione prende un oggetto `Personaggio`, ne estrae i dati tramite 
    `to_dict()` e li salva in un file JSON identificato dal suo ID, 
    all'interno della directory definita da `DATA_JSON_DIR`.

    Il file viene chiamato `<id>.json`, dove `id` è l'identificatore univoco del personaggio.

    Args:
        pg_creato (Personaggio): L'istanza del personaggio da salvare.

    Side Effects:
        - Crea o sovrascrive un file JSON nella directory `DATA_JSON_DIR`.

    Raises:
        TypeError: Se `pg_creato` non implementa il metodo `to_dict()`.
        OSError: Se ci sono problemi nella scrittura del file (es. permessi, spazio disco).
    """
    pg_dict = pg_creato.to_dict()
    name_file = f"{pg_dict['id']}.json"
    path = os.path.join(DATA_JSON_DIR, name_file)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(pg_dict, file, indent=4)


# -------------------------CREAZIONE PERSONAGGIO-------------------------
@characters_bp.route('/create_char', methods=['POST', 'GET'])
@login_required
def create_char():
    classi = {cls.__name__: cls for cls in Personaggio.__subclasses__()}
    oggetti = {ogg.__name__: ogg for ogg in Oggetto.__subclasses__()}

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        classe_sel = request.form.get('classe')
        oggetto_sel = request.form.get('oggetto')

        pg = classi[classe_sel](nome, npc=False)
        ogg = oggetti[oggetto_sel]()
        inv = Inventario(id_proprietario=pg.id)
        inv.aggiungi_oggetto(ogg)

        costo_pg = credits_to_create(pg)
        if current_user.crediti < costo_pg:
            flash(f"Non hai abbastanza crediti (minimo richiesto: {costo_pg}).", "danger")
            return redirect(url_for('auth.area_personale'))
        else:
            current_user.crediti -= costo_pg

        # Aggiorna lista personaggi e inventario in sessione
        pg_current_list = session.get('personaggi', [])
        inv_current_list = session.get('inventari', [])
        pg_current_list.append(pg.to_dict())
        inv_current_list.append(inv.to_dict())
        session['personaggi'] = pg_current_list
        session['inventari'] = inv_current_list

        # Salva id nel profilo utente
        characters_ids = (current_user.character_ids or []) + [pg.id]
        current_user.character_ids = characters_ids

        # Genera file JSON singolo
        CharSingleJson(pg)

        db.session.commit()

        msg = f"Creato personaggio: {pg.nome}, Classe: {classe_sel}, id: {pg.id}, Oggetto iniziale: {oggetto_sel}"
        Log.scrivi_log(msg)
        flash(msg, "success")

        return redirect(url_for('characters.mostra_personaggi'))

    return render_template('create_char.html', classi=classi, oggetti=oggetti)

# -------------------------EDIT PERSONAGGIO------------------------------
@characters_bp.route('/edit_cha/<int:id>', methods=['POST', 'GET'])
# @login_required
def edit_char(id):
    pass

# -------------------------RECUPERA PERSONAGGI----------------------------
@characters_bp.route('/recupera_personaggi_posseduti')
def recupera_personaggi_posseduti(owned_chars):
    pass

# -------------------------MOSTRA PERSONAGGI----------------------------
@characters_bp.route('/personaggi', methods=['GET'])
def mostra_personaggi():
    return render_template('characters.html')

# -------------------------DETAGLI PERSONAGGIO----------------------------
@characters_bp.route('/personaggi/<string:char_id>', methods=['GET'])
# @login_required
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
