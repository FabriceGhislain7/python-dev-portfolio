from flask import Blueprint, render_template, request, session, redirect, url_for, flash  # [1]
from werkzeug.security import check_password_hash  # [2]
from flask_login import login_user, logout_user, login_required, current_user  # [3]
from auth.models import User
from . import auth_bp
from app import db  # [4]
from characters.routes import load_char
from auth.utils import controllo_email, psw_proteggi_hash  # [5] - Import delle nostre utility
import os
import logging

# Setup logger per sicurezza
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

#----------------------------REGISTRAZIONE-----------------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])  # [6]
def register():
    """
    Gestisce la registrazione di un nuovo utente.

    - Con metodo GET: mostra il form HTML.
    - Con metodo POST: verifica i dati inviati, controlla se l'utente esiste già,
      valida email e password, e se tutto va bene salva l'utente nel database.

    Returns:
        Response: redirezione alla register oppure visualizzazione del form.

    References:
        [7] - Flask form handling and validation
        [8] - User registration security best practices
    """
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        psw = request.form.get('psw')
        re_psw = request.form.get('re_psw')

        # Validazioni input base
        if not username:
            flash('Il campo Nome è obbligatorio')
            return redirect(url_for('auth.register'))

        if len(username) < 3:
            flash('Il nome utente deve essere almeno 3 caratteri')
            return redirect(url_for('auth.register'))

        if not email:
            flash('Il campo Email è obbligatorio')
            return redirect(url_for('auth.register'))

        if not controllo_email(email):  # Funzione da utils
            flash('Formato email non valido')
            return redirect(url_for('auth.register'))

        if not psw or not re_psw or psw != re_psw:
            flash('Le password non coincidono')
            return redirect(url_for('auth.register'))

        # Controllo duplicati più robusto: email OR nome
        utente_exist = User.query.filter(
            (User.email == email) | (User.nome == username)
        ).first()  # [9]

        if utente_exist:
            if utente_exist.email == email:
                flash('Email già registrata')
                security_logger.warning(f"Tentativo registrazione email duplicata: {email}")
            else:
                flash('Nome utente già in uso')
                security_logger.warning(f"Tentativo registrazione nome duplicato: {username}")
            return redirect(url_for('auth.register'))

        # Crea nuovo utente
        try:
            hash_psw = psw_proteggi_hash(psw)  # Funzione da utils
            nuovo_utente = User(
                nome=username,
                email=email,
                password_hash=hash_psw,
                crediti=100.0,
                character_ids=[]
            )

            db.session.add(nuovo_utente)  # [10]
            db.session.commit()

            security_logger.info(f"Nuovo utente registrato: {email}")
            flash('Registrazione completata con successo. Puoi accedere ora!')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            security_logger.error(f"Errore registrazione utente {email}: {str(e)}")
            flash('Errore durante la registrazione. Riprova.')
            return redirect(url_for('auth.register'))

    return render_template('register.html')  # [11]

#----------------------------LOGIN-----------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])  # [6]
def login():
    """
    Gestisce l'autenticazione utente con logging di sicurezza.

    References:
        [12] - Flask-Login authentication flow
        [13] - Security event logging
    """
    if request.method == 'POST':  # [14]
        user_email = request.form.get('email', '').strip()  # [15]
        user_psw = request.form.get('psw', '').strip()

        # Validazione base degli input
        if not user_email:
            flash('Il campo Email è obbligatorio', 'danger')  # [16]
            return redirect(url_for('auth.login'))  # [17]

        if not controllo_email(user_email):  # Funzione da utils
            flash('Formato email non valido', 'danger')
            return redirect(url_for('auth.login'))

        if not user_psw:
            flash('Il campo Password è obbligatorio', 'danger')
            return redirect(url_for('auth.login'))

        # Ricerca utente nel database
        user = User.query.filter_by(email=user_email).first()  # [18]

        # Verifica della password tramite hash
        if user and check_password_hash(user.password_hash, user_psw):  # [19]
            login_user(user)  # [20]
            security_logger.info(f"Login riuscito: {user.email}")
            flash('Login effettuato con successo', 'success')
            return redirect(url_for('gioco.menu'))

        # Login fallito - logging di sicurezza
        security_logger.warning(f"Tentativo login fallito: {user_email}")
        flash('Email o password errati', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html')  # [11]

#----------------------------AREA PERSONALE----------------------------------------
@auth_bp.route('/area_personale', methods=['GET', 'POST'])
@login_required
def area_personale():
    """
    Area personale utente con caricamento personaggi.

    References:
        [21] - User dashboard implementation
    """
    load_char()
    message = ""
    message1 = request.args.get('message', '')
    if message1:
        message = message1
    return render_template("area_personale.html", user=current_user, message=message)

#----------------------------MODIFICA UTENTE--------------------------------------
@auth_bp.route('/modified_user', methods=['GET', 'POST'])
@login_required
def modified_user():
    """
    Modifica dati utente con validazioni avanzate.

    Features:
    - Controllo duplicati email
    - Validazione input sicura
    - Sicurezza: solo il proprio profilo

    References:
        [22] - User profile update security
    """
    user = current_user

    if request.method == 'POST':
        new_name = request.form.get('new_username', '').strip()
        new_email = request.form.get('new_email', '').strip()
        new_psw = request.form.get('new_password', '')

        # Validazioni input base
        if not new_name or len(new_name) < 3:
            flash("Il nome deve essere almeno 3 caratteri", "error")
            return render_template("modified_user.html", utente=user)

        if not controllo_email(new_email):  # Funzione da utils
            flash("Formato email non valido", "error")
            return render_template("modified_user.html", utente=user)

        # Controllo se nuova email già esiste (escludendo l'utente corrente)
        existing_user = User.query.filter(
            User.email == new_email,
            User.id != user.id
        ).first()

        if existing_user:
            flash("Email già in uso da un altro utente", "error")
            return render_template("modified_user.html", utente=user)

        try:
            # Aggiorna dati utente
            db_user = User.query.get_or_404(user.id)  # [23]
            db_user.nome = new_name
            db_user.email = new_email

            if new_psw:  # Aggiorna password solo se fornita
                db_user.password_hash = psw_proteggi_hash(new_psw)  # Funzione da utils
                security_logger.info(f"Password modificata per utente: {user.email}")

            db.session.commit()  # [24]
            security_logger.info(f"Utente modificato: {user.email} -> {new_email}")
            flash("Dati modificati con successo!", "success")
            return redirect(url_for('auth.area_personale'))

        except Exception as e:
            db.session.rollback()
            security_logger.error(f"Errore modifica utente {user.email}: {str(e)}")
            flash("Errore durante la modifica. Riprova.", "error")

    return render_template("modified_user.html", utente=user)

#----------------------------ELIMINAZIONE UTENTE-------------------------------------
@auth_bp.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    """
    Elimina account utente con controlli di sicurezza.

    Security features:
    - Solo l'utente può eliminare il proprio account
    - Logout automatico dopo eliminazione
    - Logging eventi di sicurezza

    References:
        [25] - Secure account deletion practices
    """
    # Controllo sicurezza: solo il proprio account
    if current_user.id != id:
        flash("Non puoi eliminare account di altri utenti", "error")
        security_logger.warning(f"Tentativo eliminazione account non autorizzato: user {current_user.id} tentando {id}")
        return redirect(url_for('auth.area_personale'))

    try:
        utente = User.query.get_or_404(id)  # [23]

        # TODO: Implementare eliminazione cascade personaggi
        # for char_id in utente.character_ids:
        #     # Elimina personaggi associati

        db.session.delete(utente)
        db.session.commit()

        # Logout automatico dopo eliminazione
        logout_user()  # [26]
        security_logger.info(f"Account eliminato: {utente.email}")
        flash("Account eliminato con successo", "info")
        return redirect(url_for('gioco.index'))

    except Exception as e:
        db.session.rollback()
        security_logger.error(f"Errore eliminazione account {id}: {str(e)}")
        flash("Errore durante l'eliminazione. Riprova.", "error")
        return redirect(url_for('auth.area_personale'))

#----------------------------RICARICA CREDITI----------------------------------
@auth_bp.route('/credit_refill', methods=['GET', 'POST'])
@login_required
def credit_refill():
    """
    Gestisce la ricarica crediti utente con validazioni e logging.

    References:
        [27] - Financial transaction security
    """
    message = None

    if request.method == 'POST':
        try:
            amount = int(request.form['amount'])  # Controllo tipo int
        except (KeyError, ValueError):  # [28]
            message = "Inserisci un numero valido."
            return redirect(url_for('auth.credit_refill', message=message))

        if amount <= 0:  # Controllo numero positivo
            message = "La quantità deve essere positiva."
            return redirect(url_for('auth.credit_refill', message=message))

        if amount > 10000:  # Limite massimo per sicurezza
            message = "Quantità massima: 10.000 crediti per transazione."
            return redirect(url_for('auth.credit_refill', message=message))

        try:
            current_user.crediti += amount
            db.session.commit()

            # Logging transazione
            security_logger.info(f"Ricarica crediti: {current_user.email} +{amount} (totale: {current_user.crediti})")
            message = f"Ricaricati {amount} crediti. Totale attuale: {int(current_user.crediti)}."
            return redirect(url_for('auth.credit_refill', message=message))

        except Exception as e:
            db.session.rollback()
            security_logger.error(f"Errore ricarica crediti {current_user.email}: {str(e)}")
            message = "Errore durante la ricarica. Riprova."
            return redirect(url_for('auth.credit_refill', message=message))

    message = request.args.get('message')  # [29]
    return render_template('credits_refill.html', message=message)

#----------------------------LOGOUT-------------------------------------------------------
@auth_bp.route('/logout')
@login_required  # [30]
def logout():
    """
    Gestisce il logout utente con pulizia sessione e logging.

    References:
        [31] - Secure logout implementation
    """
    user_email = current_user.email  # Salva prima del logout
    logout_user()  # [32]
    session.clear()  # [33]

    security_logger.info(f"Logout effettuato: {user_email}")
    flash("Logout effettuato con successo", "info")  # [16]
    return redirect(url_for('gioco.index'))  # [34]

# =============================================================================
# REFERENCES / DOCUMENTAZIONE
# =============================================================================
"""
[1] Flask API Documentation: https://flask.palletsprojects.com/en/latest/api/
[2] Werkzeug Security Utils: https://werkzeug.palletsprojects.com/en/latest/utils/
[3] Flask-Login Documentation: https://flask-login.readthedocs.io/en/latest/
[4] Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/en/latest/
[5] Local Utils Module: ./utils.py
[6] Flask Routing: https://flask.palletsprojects.com/en/latest/quickstart/#routing
[7] Flask Form Handling: https://flask.palletsprojects.com/en/latest/patterns/wtforms/
[8] User Registration Security: https://cheatsheetseries.owasp.org/cheatsheets/User_Registration_Design_Cheat_Sheet.html
[9] SQLAlchemy Filtering: https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html
[10] SQLAlchemy Sessions: https://flask-sqlalchemy.palletsprojects.com/en/latest/contexts/#using-the-session
[11] Flask Templates: https://flask.palletsprojects.com/en/latest/api/#flask.render_template
[12] Flask-Login Authentication: https://flask-login.readthedocs.io/en/latest/#flask_login.login_user
[13] Security Event Logging: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
[14] Flask Request Methods: https://flask.palletsprojects.com/en/latest/api/#flask.Request.method
[15] Flask Form Data: https://flask.palletsprojects.com/en/latest/api/#flask.Request.form
[16] Flask Message Flashing: https://flask.palletsprojects.com/en/latest/patterns/flashing/
[17] Flask URL Generation: https://flask.palletsprojects.com/en/latest/api/#flask.url_for
[18] SQLAlchemy Queries: https://flask-sqlalchemy.palletsprojects.com/en/latest/queries/
[19] Werkzeug Password Check: https://werkzeug.palletsprojects.com/en/latest/utils/#werkzeug.security.check_password_hash
[20] Flask-Login User Login: https://flask-login.readthedocs.io/en/latest/#flask_login.login_user
[21] User Dashboard Design: https://material.io/design/patterns/navigation-drawer.html
[22] User Profile Security: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
[23] SQLAlchemy get_or_404: https://flask-sqlalchemy.palletsprojects.com/en/latest/queries/#get-or-404
[24] Database Transactions: https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#committing
[25] Account Deletion Security: https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html
[26] Flask-Login Logout: https://flask-login.readthedocs.io/en/latest/#flask_login.logout_user
[27] Financial Transaction Security: https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html
[28] Python Exception Handling: https://docs.python.org/3/tutorial/errors.html
[29] Flask Request Args: https://flask.palletsprojects.com/en/latest/api/#flask.Request.args
[30] Flask-Login Required: https://flask-login.readthedocs.io/en/latest/#flask_login.login_required
[31] Secure Logout: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
[32] Flask-Login Logout: https://flask-login.readthedocs.io/en/latest/#flask_login.logout_user
[33] Flask Session Clear: https://flask.palletsprojects.com/en/latest/api/#flask.session
[34] Flask Redirects: https://flask.palletsprojects.com/en/latest/api/#flask.redirect
"""