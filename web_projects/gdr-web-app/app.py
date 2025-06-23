import os
from flask import Flask              # Importa la classe Flask
from flask_session import Session    # Per la gestione delle sessioni su filesystem

# Importa i blueprint (moduli di route)
from gioco.routes import gioco_bp
from battle.routes import battle_bp
from characters.routes import characters_bp
from environment.routes import environment_bp
from inventory.routes import inventory_bp
from mission.routes import mission_bp
from auth.routes import auth_bp

# Importa l'oggetto db (istanza di SQLAlchemy)
from database.db import db

def create_app():
    app = Flask(__name__)  # Crea l'app Flask

    # Configurazioni generali dell'app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia_questa_chiave_per_una_più_sicura')  # Chiave segreta per sessioni/sicurezza
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gdr.db"   # URL per il DB SQLite
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False         # Disabilita warning sul tracciamento modifiche
    app.config['SESSION_TYPE'] = 'filesystem'                    # Le sessioni verranno salvate su file

    db.init_app(app)       # Inizializza SQLAlchemy con l'app Flask
    Session(app)           # Inizializza il sistema di sessione

    # Registrazione dei blueprint per separare le route in moduli
    app.register_blueprint(gioco_bp)
    app.register_blueprint(battle_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(environment_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(auth_bp)

    return app  # Ritorna l'app inizializzata

# Solo se il file viene eseguito direttamente
if __name__ == '__main__':
    app = create_app()  # Crea l'app usando la funzione sopra
    with app.app_context():  # Serve per poter usare SQLAlchemy fuori dal contesto della richiesta
        db.create_all()      # Crea tutte le tabelle definite nei modelli (solo se non esistono)
    app.run(debug=True)      # Avvia il server Flask in modalità debug
