from flask import Blueprint, render_template, request, session, redirect, url_for, flash  # https://flask.palletsprojects.com/en/latest/api/
from werkzeug.security import generate_password_hash, check_password_hash  # https://werkzeug.palletsprojects.com/en/latest/utils/
from flask_login import login_user, logout_user, login_required, current_user, UserMixin  # https://flask-register.readthedocs.io/en/latest/
from auth.models import User
from . import auth_bp
from app import db  # https://flask-sqlalchemy.palletsprojects.com/en/latest/
from characters.routes import load_char
import os
import re

#----------------------------CONTROLLO EMAIL------------------------------------
def controllo_email(email):
    """
    Verifica se una stringa è un'email valida.

    Args:
        email (str): L'indirizzo email da validare.

    Returns:
        bool: True se l'email è valida, False altrimenti.

    Docs: https://docs.python.org/3/library/re.html#re.match
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

#----------------------------PROTEZIONE DELLA PASSWORD--------------------------
def psw_proteggi_hash(psw):
    """
    Genera un hash sicuro per la password fornita.

    Args:
        psw (str): La password in chiaro.

    Returns:
        str: L'hash sicuro della password.

    Docs: https://werkzeug.palletsprojects.com/en/latest/utils/#werkzeug.security.generate_password_hash
    """
    return generate_password_hash(psw)

#----------------------------SIGN_IN (REGISTRAZIONE)----------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])  # https://flask.palletsprojects.com/en/latest/quickstart/#routing
def register():
    """
    Gestisce la registrazione di un nuovo utente.

    - Con metodo GET: mostra il form HTML.
    - Con metodo POST: verifica i dati inviati, controlla se l'utente esiste già,
      valida email e password, e se tutto va bene salva l'utente nel database.

    Returns:
        Response: redirezione alla register oppure visualizzazione del form.

    Docs:
    - Flask request/form: https://flask.palletsprojects.com/en/latest/api/#flask.Request.form
    - Flask flash: https://flask.palletsprojects.com/en/latest/patterns/flashing/
    - Flask redirect/url_for: https://flask.palletsprojects.com/en/latest/api/#flask.redirect
    - Flask template rendering: https://flask.palletsprojects.com/en/latest/api/#flask.render_template
    - SQLAlchemy querying: https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html
    """

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        psw = request.form.get('psw')
        re_psw = request.form.get('re_psw')

        # Validazioni input
        if not username:
            flash('Il campo Nome è obbligatorio ❗')
            return redirect(url_for('auth.register'))

        if not email:
            flash('Il campo Email è obbligatorio ❗')
            return redirect(url_for('auth.register'))

        if not controllo_email(email):
            flash('Formato email non valido ❗')
            return redirect(url_for('auth.register'))

        if not psw or not re_psw or psw != re_psw:
            flash('Le password non coincidono ❗')
            return redirect(url_for('auth.register'))

        # Verifica se l'utente esiste già nel DB
        utente_exist = User.query.filter_by(email=email).first()  # https://flask-sqlalchemy.palletsprojects.com/en/latest/queries/
        if utente_exist:
            flash('Email già registrata ❗')
            return redirect(url_for('auth.register'))

        # Crea nuovo utente
        hash_psw = psw_proteggi_hash(psw)
        nuovo_utente = User(
            nome=username,
            email=email,
            password_hash=hash_psw,
            crediti=100.0,
            character_ids=[]
        )

        db.session.add(nuovo_utente)       # https://flask-sqlalchemy.palletsprojects.com/en/latest/contexts/#using-the-session
        db.session.commit()

        flash('Registrazione completata con successo ✔️ Puoi accedere ora!')
        return redirect(url_for('auth.login'))  # assicurati che questa route esista

    return render_template('register.html')  # https://flask.palletsprojects.com/en/latest/api/#flask.render_template


#----------------------------LOGIN-----------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])  # https://flask.palletsprojects.com/en/latest/quickstart/#routing
def login():
    if request.method == 'POST':  # https://flask.palletsprojects.com/en/latest/api/#flask.Request.method
        user_email = request.form.get('email', '').strip()  # https://flask.palletsprojects.com/en/latest/api/#flask.Request.form
        user_psw = request.form.get('psw', '').strip()

        # ✅ Validazione base degli input
        if not user_email:
            flash('Il campo Email è obbligatorio ❗', 'danger')  # https://flask.palletsprojects.com/en/latest/patterns/flashing/
            return redirect(url_for('auth.login'))  # https://flask.palletsprojects.com/en/latest/api/#flask.url_for

        if not controllo_email(user_email):  # funzione personalizzata con regex
            flash('Formato email non valido ❗', 'danger')
            return redirect(url_for('auth.login'))

        if not user_psw:
            flash('Il campo Password è obbligatorio ❗', 'danger')
            return redirect(url_for('auth.login'))

        # ✅ Ricerca utente nel database
        user = User.query.filter_by(email=user_email).first()  # https://flask-sqlalchemy.palletsprojects.com/en/latest/queries/

        # ✅ Verifica della password tramite hash
        if user and check_password_hash(user.password_hash, user_psw):  # https://werkzeug.palletsprojects.com/en/latest/utils/#werkzeug.security.check_password_hash
            login_user(user)  # https://flask-login.readthedocs.io/en/latest/#flask_login.login_user
            flash('Login effettuato con successo ✔️', 'success')
            return redirect(url_for('gioco.menu'))  # redireziona al menu di gioco (modifica se diverso)

        # ❌ Email o password errati
        flash('Email o password errati ❗', 'danger')
        return redirect(url_for('auth.login'))

    # ✅ Render della pagina login
    return render_template('login.html')  # https://flask.palletsprojects.com/en/latest/api/#flask.render_template


#----------------------------AREA PERSONALE----------------------------------------
@auth_bp.route('/area_personale', methods=['GET', 'POST'])
def area_personale():
    pass

#----------------------------CREAZIONE UTENTE--------------------------------------
@auth_bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    pass

#----------------------------ELIMINAZIONE UTENTE-------------------------------------
@auth_bp.route('/delete_user', methods=['GET', 'POST'])
# @login_required
def delete_user():
    pass

#----------------------------CREAZIONE DEI CREDITI----------------------------------
@auth_bp.route('/credit_refill', methods=['GET', 'POST'])
# @login_required
def credit_refill():
    pass

#----------------------------LOGOUT-------------------------------------------------------
@auth_bp.route('/logout')
@login_required  # https://flask-login.readthedocs.io/en/latest/#flask_login.login_required
def logout():
    logout_user()  # https://flask-login.readthedocs.io/en/latest/#flask_login.logout_user
    session.clear()  # https://flask.palletsprojects.com/en/latest/api/#flask.session
    flash("Logout effettuato con successo", "info")  # https://flask.palletsprojects.com/en/latest/patterns/flashing/
    return redirect(url_for('gioco.index'))  # 🔄 Migliore di render_template (previene problemi di stato)
