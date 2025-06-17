from flask import Blueprint, render_template, redirect, url_for, session

gioco = Blueprint('gioco',
                  __name__,
                  template_folder='../templates')


@gioco.route('/')
def index():
    return render_template('index.html')


@gioco.route('/new_game', methods=['GET', 'POST'])
def new_game():
    # Qui andrà il form di creazione dei personaggi
    return render_template('create_char.html')


@gioco.route('/load_game')
def load_game():
    # Qui andrà la logica per caricare un salvataggio
    return render_template('load_game.html')


@gioco.route('/select_mission', methods=['GET', 'POST'])
def select_mission():
    # Qui andrà la selezione e attivazione missioni
    return render_template('select_mission.html')


@gioco.route('/battle', methods=['GET', 'POST'])
def battle():
    # Qui andrà lo svolgimento dello scontro
    return render_template('battle.html')


@gioco.route('/inventory')
def inventory():
    # Qui andrà la visualizzazione dell'inventario del giocatore
    return render_template('inventory.html')


@gioco.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('gioco.index'))
