from . import auth_bp
from flask import render_template, request, redirect, url_for, session, flash

# route per il Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            flash('Login effettuato con successo!', 'success')
            return redirect(url_for('gioco.menu'))
        else:
            flash('Insersci un nome utente valido.', 'damger')
    return render_template('login.html')

# Route per il Logout
@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logout effettuato!', 'info')
    return redirect(url_for('gioco.index'))

# Route per signup
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            # Per ora proviamo una registrazione automatica
            session['session'] = username
            flash('Account creato con successo!', 'success')
            return redirect(url_for('gioco.menu'))
        else:
            flash('inserisce un nome valido', 'danger')

    return render_template('signup.html')
