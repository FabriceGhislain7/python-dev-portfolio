import os
import json

from flask import render_template, request, redirect, url_for, session, abort, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin

from . import characters_bp
from gioco.personaggio import Personaggio
from gioco.oggetto import Oggetto
from gioco.inventario import Inventario
from utils.log import Log
from auth.models import User, db
from auth.credits import credits_to_create, credits_to_refund
from config import DATA_JSON_DIR

# ------------------------------------------------------
# MAPPING CLASSI E OGGETTI DISPONIBILI
# ------------------------------------------------------
classi = {cls.__name__: cls for cls in Personaggio.__subclasses__()}
oggetti = {ogg.__name__: ogg for ogg in Oggetto.__subclasses__()}


# -------------------------LOAD CHAR (PLACEHOLDER)----------------------------
@characters_bp.route('/load_char')
# @login_required
def load_char():
    pass


# -------------------------CARICA PERSONAGGI DA ID----------------------------
def carica_personaggi_da_ids(owned_chars_ids: list[str]) -> list[dict]:
    personaggi = []
    for id in owned_chars_ids:
        path = os.path.join(DATA_JSON_DIR, f"{id}.json")
        if os.path.exists(path):
            with open(path, "r", encoding='utf-8') as file:
                char_dict = json.load(file)
                personaggi.append(char_dict)
        else:
            print(f"[AVVISO] File JSON non trovato per il personaggio con ID: {id}")
    return personaggi


# -------------------------SALVATAGGIO SINGOLO FILE JSON----------------------
def CharSingleJson(pg_creato: Personaggio):
    pg_dict = pg_creato.to_dict()
    name_file = f"{pg_dict['id']}.json"
    path = os.path.join(DATA_JSON_DIR, name_file)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(pg_dict, file, indent=4)


# -------------------------CREAZIONE PERSONAGGIO------------------------------
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

        # Aggiorna sessione
        pg_current_list = session.get('personaggi', [])
        inv_current_list = session.get('inventari', [])
        pg_current_list.append(pg.to_dict())
        inv_current_list.append(inv.to_dict())
        session['personaggi'] = pg_current_list
        session['inventari'] = inv_current_list

        # Salva ID nel profilo utente
        characters_ids = (current_user.character_ids or []) + [pg.id]
        current_user.character_ids = characters_ids

        # Salva su file
        CharSingleJson(pg)

        db.session.commit()

        msg = f"Creato personaggio: {pg.nome}, Classe: {classe_sel}, id: {pg.id}, Oggetto iniziale: {oggetto_sel}"
        Log.scrivi_log(msg)
        flash(msg, "success")

        return redirect(url_for('characters.mostra_personaggi'))

    return render_template('create_char.html', classi=classi, oggetti=oggetti)


# -------------------------MODIFICA PERSONAGGIO------------------------------
@characters_bp.route('/modified_char/<string:id_pers>', methods=['POST', 'GET'])
@login_required
def modifica_personaggio(id_pers):
    # ------------------------------------------------------
    # CARICAMENTO E VERIFICA DEL PERSONAGGIO
    # ------------------------------------------------------
    owned_ids = current_user.character_ids or []

    if id_pers not in owned_ids:
        flash("Impossibile trovare il personaggio", "danger")
        return redirect(url_for("characters.mostra_personaggi"))

    path = os.path.join(DATA_JSON_DIR, f"{id_pers}.json")

    if not os.path.isfile(path):
        flash("Personaggio non raggiungibile", "danger")
        return redirect(url_for('characters.mostra_personaggi'))

    with open(path, 'r', encoding='utf-8') as f:
        pg = json.load(f)

    classi = {cls.__name__: cls for cls in Personaggio.__subclasses__()}

    # ------------------------------------------------------
    # GESTIONE FORM POST
    # ------------------------------------------------------
    if request.method == 'POST':
        vecchio_nome = pg['nome']
        nuovo_nome = request.form['nome'].strip()
        nuova_classe = request.form['classe']

        pg['nome'] = nuovo_nome
        pg['classe'] = nuova_classe

        pg_obj = Personaggio.from_dict(pg)
        CharSingleJson(pg_obj)

        Log.scrivi_log(
            f"Modificato personaggio id={id_pers}: "
            f"Nome: da '{vecchio_nome}' a '{nuovo_nome}', "
            f"Nuova classe: '{nuova_classe}'"
        )

        flash("Personaggio aggiornato con successo", "success")
        return redirect(url_for('characters.mostra_personaggi'))

    # ------------------------------------------------------
    # RENDERING FORM GET
    # ------------------------------------------------------
    return render_template(
        'char_modified.html',
        pg=pg,
        classi=list(classi.keys())
    )


# -------------------------MOSTRA PERSONAGGI------------------------------
@characters_bp.route('/personaggi', methods=['GET'])
def mostra_personaggi():
    chars_ids = current_user.character_ids
    personaggi = carica_personaggi_da_ids(chars_ids)
    session['personaggi'] = personaggi
    return render_template('list_characters.html', personaggi=personaggi)


# -------------------------DETTAGLIO PERSONAGGIO--------------------------
@characters_bp.route('/personaggi/<string:id_pers>', methods=['GET'])
@login_required
def dettaglio_personaggio(id_pers):
    list_personaggi = session.get('personaggi', [])
    personaggio = next((p for p in list_personaggi if p['id'] == id_pers), None)
    return render_template('details_char.html', pg=personaggio)


# -------------------------ELIMINA PERSONAGGIO----------------------------
@characters_bp.route('/elimina/<string:id_pers>', methods=['POST'])
@login_required
def elimina_personaggio(id_pers):
    list_personaggi = session.get('personaggi', [])
    pg = next((p for p in list_personaggi if p['id'] == id_pers), None)

    if not pg:
        Log.scrivi_log(f"[ERRORE] Personaggio con ID {id_pers} non trovato nella sessione")
        flash("Personaggio non trovato", "danger")
        return redirect(url_for('characters.mostra_personaggi'))

    # Rimuovi dalla sessione
    list_personaggi = [p for p in list_personaggi if p['id'] != id_pers]
    session['personaggi'] = list_personaggi

    # Elimina file JSON
    file_path = os.path.join(DATA_JSON_DIR, f"{pg['id']}.json")
    if os.path.exists(file_path):
        os.remove(file_path)
        Log.scrivi_log(f"Eliminato file JSON: {file_path}")

    # Aggiorna lista ID e crediti
    ids = current_user.character_ids or []
    if id_pers in ids:
        ids.remove(id_pers)
        current_user.character_ids = ids

    try:
        pg_ogg = classi.get(pg['classe'])(pg['nome'])
        current_user.crediti += credits_to_refund(pg_ogg)
    except Exception as e:
        Log.scrivi_log(f"Errore nel rimborso: {e}")

    db.session.commit()
    flash("Personaggio eliminato con successo!", "success")
    return redirect(url_for('characters.mostra_personaggi'))


# -------------------------INIZIA COMBATTIMENTO (PLACEHOLDER)-----------------
@characters_bp.route('/combattimento', methods=['GET', 'POST'])
def inizio_combattimento():
    pass
