#  Integrazione SQLAlchemy in progetto Flask GDR – Versione 1.0

Questa guida documenta l'integrazione del sistema di **autenticazione utenti**, **gestione personaggi** e **salvataggio su database SQLAlchemy** in un'app Flask per gioco di ruolo (GDR).

---

##  Obiettivo della v1.0

Un'applicazione web con:
- Registrazione e login utenti
- Creazione personaggi associati a ciascun utente
- Salvataggio persistente su database SQLite
- Flask + SQLAlchemy come stack base

---

##  Struttura consigliata del progetto

```

gdr-web-app/
│
├── app.py                  # App principale
├── config.py               # Config opzionale
│
├── /templates/             # HTML Jinja2
│   ├── layout.html
│   ├── login.html
│   ├── signup.html
│   └── dashboard.html
│
├── /auth/                  # Login, signup, logout
│   └── routes.py
│
├── /characters/            # Gestione personaggi
│   └── routes.py
│
├── /database/              # SQLAlchemy & modelli
│   ├── db.py
│   ├── models.py
│   └── seed.py
│
├── /utils/                 # Funzioni extra (es. JSON, log)
│   └── salvataggio.py

````

---

##  Dipendenze richieste

Installa i pacchetti con:

```bash
pip install Flask Flask-SQLAlchemy Flask-Session
````

---

##  Modelli (database/models.py)

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    personaggi = db.relationship('Personaggio', backref='utente', lazy=True)

class Personaggio(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    nome        = db.Column(db.String(50), nullable=False)
    classe      = db.Column(db.String(50), nullable=False)
    salute      = db.Column(db.Integer, default=100)
    attacco_min = db.Column(db.Integer, default=5)
    attacco_max = db.Column(db.Integer, default=15)
    livello     = db.Column(db.Integer, default=1)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

---

##  Configurazione Flask (app.py)

```python
from flask import Flask
from flask_session import Session
from database.db import db
from auth.routes import auth_bp
from characters.routes import characters_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sostituisci_questa_chiave'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gdr.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    Session(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(characters_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

---

##  Sistema di autenticazione (auth/routes.py)

Contiene:

* `GET/POST /signup` – registrazione utente con password hash
* `GET/POST /login` – login con verifica
* `GET /logout` – rimozione sessione

> Salva `session['user_id']` e `session['username']`.

---

##  Gestione personaggi (characters/routes.py)

> Solo accessibile da utenti loggati.

* `GET /personaggi` → mostra lista personaggi utente
* `GET/POST /personaggi/crea` → crea nuovo personaggio legato all’utente

---

##  Funzionalità coperte

| Funzione               | Route              | Protezione |
| ---------------------- | ------------------ | ---------- |
| Registrazione          | `/signup`          | pubblica   |
| Login                  | `/login`           | pubblica   |
| Logout                 | `/logout`          | loggati    |
| Lista personaggi       | `/personaggi`      | loggati    |
| Crea nuovo personaggio | `/personaggi/crea` | loggati    |

---

##  Passaggi chiave

1. **Inizializza DB in `db.py`**:

   ```python
   from flask_sqlalchemy import SQLAlchemy
   db = SQLAlchemy()
   ```

2. **Chiama `db.init_app(app)` in `app.py`**

3. **Usa `with app.app_context(): db.create_all()` per creare le tabelle**

---

##  Sicurezza consigliata

* Password salvate con `werkzeug.security.generate_password_hash`
* Verifica con `check_password_hash`
* Sessioni gestite via `Flask-Session`

---

##  Possibili estensioni (v1.1+)

* Inventario e oggetti (relazione uno-a-molti)
* Missioni e ambienti (molti-a-molti)
* Scontri e log battaglia
* API REST o GraphQL
* Salvataggi esportabili in JSON (`utils/salvataggio.py`)

---

##  Conclusione

Questo schema fornisce una base solida per evolvere il tuo GDR web, separando chiaramente:

* logica del database
* gestione degli utenti
* interazione del giocatore

Con Flask + SQLAlchemy + sessioni ben strutturate.

```
