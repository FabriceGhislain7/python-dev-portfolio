import os
from flask import Flask
from flask_session import Session
from gioco.routes import gioco_bp
from battle.routes import battle_bp
from characters.routes import characters_bp
from environment.routes import environment_bp
from inventory.routes import inventory_bp
from mission.routes import mission_bp
from auth.routes import auth_bp  # Importa il blueprint di autenticazione 1
from flask_migrate import Migrate
from auth import auth_bp  # Importa il blueprint di autenticazione 2
from auth.models import db, User
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY',
        'cambia_questa_chiave_per_una_più_sicura'
    )
    app.config['SESSION_TYPE'] = 'filesystem'
    # Configurazione per il database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

    db.init_app(app)
    migrate = Migrate(app, db)  # Assegnata non utilizzata
    login_manager.init_app(app)
    Session(app)

    app.register_blueprint(gioco_bp)
    app.register_blueprint(battle_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(environment_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(auth_bp)

    return app

# Imposta una SECRET_KEY sicura (meglio via variabile d'ambiente)

# Inizializza il supporto alle sessioni sul filesystem


# Registra il blueprint che contiene tutte le route di gioco


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    # Modalità di sviluppo con reload automatico
    app = create_app()
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0", port=5001)
