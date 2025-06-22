import os
from flask import Flask
from flask_session import Session
from gioco.routes import gioco_bp
from battle.routes import battle_bp
from characters.routes import characters_bp
from environment.routes import environment_bp
from inventory.routes import inventory_bp
from mission.routes import mission_bp
from auth.routes import auth_bp

def create_app():
    app = Flask( __name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cambia_questa_chiave_per_una_più_sicura')
    app.config['SESSION_TYPE'] = 'filesystem'

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


if __name__ == '__main__':
    # Modalità di sviluppo con reload automatico
    app = create_app()
    app.run(debug=True)