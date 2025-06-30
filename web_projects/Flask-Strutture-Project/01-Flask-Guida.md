# Guida per la realizzazione di un progetto Flask(Pricipianti)

## Desscrizione del progetto

Applicazione web sviluppata in Flask, con struttura modulare e uso dei blueprint. Questo progetto serve come base per applicazioni web scalabili e manutenibili.

## Tecnologie utilizzate

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Jinja2
- JavaScript (per interattività lato client)
- SQLite / PostgreSQL
- Bootstrap / TailwindCSS (opzionali)

## Struttura del progetto

Prima di creare le cartelle del progetto, clonare il repository `Github` dentro la quale si intende localizzare il progetto con commando:
```bash
git clone https://github.com/tuo-utente/tuo-repo.git
```

Lo script pyhton scritto sotto è per la creazione veloce delle cartelle e dei flie necesari per il progetto Flask.  Nella repository locale, crea un file che ho nominato `quick_start.py`, che deve essere messo nella stessa directory dove verra creato il file del progetto `nome_progetto` dentro il quale ci sarà l'ambiente virtuale `venv` e tutti gli altri file necessari.


```python
import os

# Nome del progetto (cartella principale)
base_dir = "nome_progetto"

# Struttura del progetto
struttura = {
    "cartella": ["__init__.py", "routes.py"],
    "utils": ["__init__.py", "utils.py"],
    "models": ["__init__.py", "models.py", "routes.py"],
    "root_files": ["main.py", "app.py", "README.md"]
}

# Crea la directory principale
os.makedirs(base_dir, exist_ok=True)

# Loop sulle cartelle e file da creare
for cartella, files in struttura.items():
    if cartella != "root_files":
        cartella_path = os.path.join(base_dir, cartella)
        os.makedirs(cartella_path, exist_ok=True)

        for file in files:
            file_path = os.path.join(cartella_path, file)
            with open(file_path, "w", encoding="utf-8") as f:
                pass  # File vuoto: lo scriverai tu a mano
    else:
        for file in files:
            file_path = os.path.join(base_dir, file)
            with open(file_path, "w", encoding="utf-8") as f:
                pass  # Anche questi file sono lasciati vuoti

```
---

Metteresi nella dir del file `quick_start.py` e eseguire il commando:

```bash
python quick_start.py
```
oppure
```bash
py quick_start.py
```

## Istallazione dei packages per flask

- Entra nella cartella del progetto Flask con commando:
```bash
cd nome_progetto
```
- Creazione dell'ambiente virtuale con il commando:
```bash
python3 -m venv venv  # oppure py -m venv venv
source venv/bin/activate  # Su linux
```
oppure
```bash
venv/Scripts/activate  # su Windows
```
Si puo proseguire manualmente l'istallazione delle librerie che ci servono. Possiamo istallare uno dopo l'altra:
```bash
pip install Flask
```
```bash
pip install sphinx
```
```bash
pip install flask_sqlalchemy
```
---
- Creare un file `requirements.txt` alla radice del progetto e copiare questo contenu dentro:
```bash
alabaster==1.0.0
babel==2.17.0
blinker==1.9.0
cachelib==0.13.0
certifi==2025.6.15
charset-normalizer==3.4.2
click==8.2.1
colorama==0.4.6
docutils==0.21.2
Flask==3.1.1
Flask-Login==0.6.3
Flask-Session==0.8.0
Flask-SQLAlchemy==3.1.1
greenlet==3.2.3
idna==3.10
imagesize==1.4.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
msgspec==0.19.0
packaging==25.0
Pygments==2.19.2
requests==2.32.4
snowballstemmer==3.0.1
Sphinx==8.1.3
sphinxcontrib-applehelp==2.0.0
sphinxcontrib-devhelp==2.0.0
sphinxcontrib-htmlhelp==2.1.0
sphinxcontrib-jsmath==1.0.1
sphinxcontrib-qthelp==2.0.0
sphinxcontrib-serializinghtml==2.0.0
SQLAlchemy==2.0.41
tomli==2.2.1
typing_extensions==4.14.0
urllib3==2.5.0
Werkzeug==3.1.3
```
Poi eseguire il commando:
```bash
pip install -r requirements.txt
```
## impostazione di alcune cartelle importanti
### Generazione della documentazione : 

#### Sphinx

 è un potente generatore di documentazione che può leggere i docstring in stile reStructuredText o Google/Numpy-style dai tuoi file .py e generare documentazione in HTML, PDF o altri formati

creazione ambiente virtuale
```bash
python -m venv venv
source venv/bin/activate 
# Su Windows usa 'venv\Scripts\activate'
```

Passaggi per generare la documentazione in Python con Sphinx

1. Installa Sphinx
```bash
pip install sphinx
```

2. Crea la struttura del progetto

Nella cartella del tuo progetto Python, esegui:

```bash
sphinx-quickstart docs
```
Dovrebbe creare una cartella `docs` con una struttura di base per la documentazione
```bash
nome_progetto/
│
├── modulo/
│   └── calcolatrice.py        # Modulo Python con Google-style docstring
│
├── docs/                      # Cartella documentazione Sphinx
│   ├── conf.py                # Configurazione
│   ├── index.rst              # Indice principale
│   ├── modulo.rst             # Documentazione automatica
│   └── _build/                # Output HTML (vuoto finché non esegui `make html`)
│
└── requirements.txt           # (opzionale)
```

3. Configura Sphinx

Apri il file `docs/conf.py` e aggiungi il percorso del tuo progetto Python:

```python
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

extensions = [
    'sphinx.ext.autodoc',  # per generare doc dai docstrings
    'sphinx.ext.napoleon', # per supporto Google/Numpy style docstrings
    'sphinx_autodoc_typehints', # mostra i tipi come annotazioni
]

html_theme = 'sphinx_rtd_theme'
```

4. Crea i file .rst per i tuoi moduli

Puoi farlo manualmente o con:
```bash
sphinx-apidoc -o docs/source ../tuo_pacchetto
```

Sostituisci tuo_pacchetto con la cartella che contiene i tuoi file .py

5. Costruisci la documentazione

Esegui:

```bash
cd docs
make html  # oppure 'make.bat html' su Windows
```
Troverai la documentazione HTML in docs/_build/html/index.html


# Guida Completa a Flask SqlAlchemy

## 10. Connessione a Database (es. SQLite)
Con Flask puoi usare sqlite3 standard o meglio ancora Flask-SQLAlchemy:

```bash
# crea  l ambiente virtuale
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
# Installa Flask e Flask-SQLAlchemy
pip install flask_sqlalchemy
```

Esempio semplice:

in app.py:

```python
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utenti.db'
db = SQLAlchemy(app)

class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)

# Per creare il database:
with app.app_context():
    db.create_all()
```

## 11. Esempio Mini-app completa
```python
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", titolo="Benvenuto", messaggio="Homepage!")

@app.route('/login', methods=['GET', 'POST'])
def login():
    nome = None
    if request.method == 'POST':
        nome = request.form['nome']
    return render_template("login.html", nome=nome)

if __name__ == '__main__':
    app.run(debug=True)
```
`adduser.html` e `utenti.html`.

adduser.html

```html
<!doctype html>
<html>
  <head><title>Aggiungi Utente</title></head>
  <body>
    <h1>Aggiungi Utente</h1>
    <form method="POST">
      Nome: <input type="text" name="nome" required>
      <input type="submit" value="Aggiungi">
    </form>
    {% if messaggio %}
      <p>{{ messaggio }}</p>
    {% endif %}
    <a href="/utenti">Vedi tutti gli utenti</a>
  </body>
</html>
```
adduser.html (con template)
```html
{% extends "base.html" %}

{% block title %}Aggiungi Utente{% endblock %}

{% block content %}
  <h2>Aggiungi Utente</h2>
  <form method="POST">
    Nome: <input type="text" name="nome" required><br>
    <input type="submit" value="Aggiungi">
  </form>
  {% if messaggio %}
    <p>{{ messaggio }}</p>
  {% endif %}

  <a href="{{ url_for('utenti') }}">Vedi tutti gli utenti</a>
{% endblock %}
```
utenti.html

```html
<!doctype html>
<html>
  <head><title>Lista Utenti</title></head>
  <body>
    <h1>Lista Utenti</h1>
    <ul>
      {% for utente in utenti %}
        <li>{{ utente.nome }}</li>
      {% endfor %}
    </ul>
    <a href="/adduser">Aggiungi nuovo utente</a>
  </body>
</html>
```
utenti.html (con template)
```html
{% extends "base.html" %}

{% block title %}Lista Utenti{% endblock %}

{% block content %}
  <h2>Lista Utenti</h2>
  <ul>
    {% for utente in utenti %}
      <li>{{ utente.nome }}</li>
    {% endfor %}
  </ul>
  <a href="{{ url_for('adduser') }}">Aggiungi nuovo utente</a>
{% endblock %}
```
2. Aggiorna il file app.py
Aggiungi queste route:

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utenti.db'
db = SQLAlchemy(app)

class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)

# Per creare il database:
with app.app_context():
    db.create_all()

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    messaggio = None
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            nuovo_utente = Utente(nome=nome)
            db.session.add(nuovo_utente)
            db.session.commit()
            messaggio = f'Utente {nome} aggiunto!'
    return render_template("adduser.html", messaggio=messaggio)

@app.route('/utenti')
def utenti():
    lista_utenti = Utente.query.all()
    return render_template("utenti.html", utenti=lista_utenti)

# Home redirect a utenti (opzionale)
@app.route('/')
def home():
    return redirect(url_for('utenti'))

if __name__ == '__main__':
    app.run(debug=True)
```
# Estensione App Flask: ricerca, modifica, elimina
1. Ricerca utenti

Aggiungiamo un campo di ricerca nella pagina della lista utenti.

utenti.html (sostituisci la versione precedente):

```html
<!doctype html>
<html>
  <head><title>Lista Utenti</title></head>
  <body>
    <h1>Lista Utenti</h1>
    <form method="GET" action="/utenti">
      <input type="text" name="query" placeholder="Cerca nome..." value="{{ request.args.get('query', '') }}">
      <input type="submit" value="Cerca">
    </form>
    <ul>
      {% for utente in utenti %}
        <li>
          {{ utente.nome }} 
          <a href="/modifica/{{ utente.id }}">Modifica</a> 
          <a href="/elimina/{{ utente.id }}" onclick="return confirm('Sicuro di voler eliminare?')">Elimina</a>
        </li>
      {% endfor %}
    </ul>
    <a href="/adduser">Aggiungi nuovo utente</a>
  </body>
</html>
```
utenti.html (con template)
```html
{% extends "base.html" %}

{% block title %}Lista Utenti{% endblock %}

{% block content %}
  <h2>Lista Utenti</h2>
  <form method="GET" action="{{ url_for('utenti') }}">
    <input type="text" name="query" placeholder="Cerca nome..." value="{{ request.args.get('query', '') }}">
    <input type="submit" value="Cerca">
  </form>
  <ul>
    {% for utente in utenti %}
      <li>
        {{ utente.nome }}
        <a href="{{ url_for('modifica', id=utente.id) }}">Modifica</a>
        <a href="{{ url_for('elimina', id=utente.id) }}" onclick="return confirm('Sicuro di voler eliminare?')">Elimina</a>
      </li>
    {% endfor %}
  </ul>
  <a href="{{ url_for('adduser') }}">Aggiungi nuovo utente</a>
{% endblock %}
```
Modifica la route /utenti in app.py così:

```python
@app.route('/utenti')
def utenti():
    query = request.args.get('query', '')
    if query:
        lista_utenti = Utente.query.filter(Utente.nome.ilike(f'%{query}%')).all()
    else:
        lista_utenti = Utente.query.all()
    return render_template("utenti.html", utenti=lista_utenti)
```
2. Eliminazione utenti

Aggiungi questo import:
```python
from flask import redirect, url_for
```

Aggiungi questa route:

```python
@app.route('/elimina/<int:id>')
def elimina(id):
    utente = Utente.query.get_or_404(id)
    db.session.delete(utente)
    db.session.commit()
    return redirect(url_for('utenti'))
```
3. Modifica utenti

Crea modifica.html nei template:

```html
<!doctype html>
<html>
  <head><title>Modifica Utente</title></head>
  <body>
    <h1>Modifica Utente</h1>
    <form method="POST">
      Nome: <input type="text" name="nome" value="{{ utente.nome }}" required>
      <input type="submit" value="Salva">
    </form>
    <a href="/utenti">Torna alla lista</a>
  </body>
</html>
```
modifica.html (con template)
```html
{% extends "base.html" %}

{% block title %}Modifica Utente{% endblock %}

{% block content %}
  <h2>Modifica Utente</h2>
  <form method="POST">
    Nome: <input type="text" name="nome" value="{{ utente.nome }}" required>
    <input type="submit" value="Salva">
  </form>
  <a href="{{ url_for('utenti') }}">Torna alla lista</a>
{% endblock %}
```
Aggiungi questa route:
```python
@app.route('/modifica/<int:id>', methods=['GET', 'POST'])
def modifica(id):
    utente = Utente.query.get_or_404(id)
    if request.method == 'POST':
        nuovo_nome = request.form['nome']
        utente.nome = nuovo_nome
        db.session.commit()
        return redirect(url_for('utenti'))
    return render_template("modifica.html", utente=utente)
```
4. Riepilogo delle nuove route nel tuo app.py

Aggiungi queste (in qualsiasi ordine dopo la definizione della classe):

```python
@app.route('/utenti')
def utenti():
    query = request.args.get('query', '')
    if query:
        lista_utenti = Utente.query.filter(Utente.nome.ilike(f'%{query}%')).all()
    else:
        lista_utenti = Utente.query.all()
    return render_template("utenti.html", utenti=lista_utenti)

@app.route('/elimina/<int:id>')
def elimina(id):
    utente = Utente.query.get_or_404(id)
    db.session.delete(utente)
    db.session.commit()
    return redirect(url_for('utenti'))

@app.route('/modifica/<int:id>', methods=['GET', 'POST'])
def modifica(id):
    utente = Utente.query.get_or_404(id)
    if request.method == 'POST':
        nuovo_nome = request.form['nome']
        utente.nome = nuovo_nome
        db.session.commit()
        return redirect(url_for('utenti'))
    return render_template("modifica.html", utente=utente)
```
# 5. Funzionalità extra

- Controllo duplicati: prima di aggiungere/modificare, controlla se il nome esiste già.
- Messaggi di successo/errore: puoi mostrare messaggi di conferma.
- Aggiungi altri campi: es. cognome, email…

## 1. Modifica il modello
app.py cambia così la classe Utente:

```python
class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    cognome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
```
Nota: Qui email è unique (non può esistere doppia email nel DB).

> Se hai già il database con solo “nome”, dovresti cancellare il file utenti.db e ricrearlo, oppure fare una migrazione (per semplicità: cancella e rifai se sei in test).

# Migrazioni

Esempio di migrazione con Flask-Migrate (opzionale):

```bash
pip install Flask-Migrate
```
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
# Aggiungi questa riga dopo db = SQLAlchemy(app)
```
Verifica che le dipendenze siano installate:

```bash
pip list
```
## Setta le variabili di ambiente per Flask-Migrate:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```
oppure su Windows:
```cmd
set FLASK_APP=app-sqlalchemy.py
set FLASK_ENV=development
```
## Esegui i comandi per migrare:
```bash
flask db init
flask db migrate -m "Inizializzazione"
flask db upgrade
```
# Comandi di stato:
```bash
flask db history     # vedi la cronologia delle migrazioni
flask db current     # vedi a che punto sei
flask db downgrade -1  # torna indietro di una migrazione
```
Se la migrazione non funziona controllare il file migrations/env.py e assicurarsi che sia configurato correttamente per il tuo database.

Flask/Alembic genera una constraint UNIQUE senza nome, che su SQLite non va bene quando si fa una migrazione su una tabella che c'è già. Per risolvere, puoi modificare il file di migrazione generato in migrations/versions/xxxx_add_cognome_email.py e aggiungere un nome alla constraint:

```python
batch_op.create_unique_constraint('uq_email', ['email'])
```
Dopo aver fatto questo, puoi eseguire nuovamente `flask db upgrade`.
```bash
flask db init
flask db migrate -m "Aggiungi cognome ed email modifica"
flask db upgrade
```

2. Modifica/aggiungi template
adduser.html
```html
<form method="POST">
  Nome: <input type="text" name="nome" required><br>
  Cognome: <input type="text" name="cognome" required><br>
  Email: <input type="email" name="email" required><br>
  <input type="submit" value="Aggiungi">
</form>
```
modifica.html
```html
<form method="POST">
  Nome: <input type="text" name="nome" required><br>
  Cognome: <input type="text" name="cognome" required><br>
  Email: <input type="email" name="email" required><br>
  <input type="submit" value="Aggiungi">
</form>
```
utenti.html
(Sostituisci l’elenco utenti: ora si vedono anche cognome ed email)

```html
<ul>
  {% for utente in utenti %}
    <li>
      {{ utente.nome }} {{ utente.cognome }} ({{ utente.email }})
      <a href="/modifica/{{ utente.id }}">Modifica</a>
      <a href="/elimina/{{ utente.id }}" onclick="return confirm('Sicuro di voler eliminare?')">Elimina</a>
    </li>
  {% endfor %}
</ul>
```
3. Aggiorna le route nel file app.py
```python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utenti.db'
db = SQLAlchemy(app)

class Utente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    cognome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

with app.app_context():
    db.create_all()

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    messaggio = None
    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        email = request.form['email']
        # Controllo duplicati: email o combinazione nome+cognome
        utente_exist = Utente.query.filter((Utente.email == email) | ((Utente.nome == nome) & (Utente.cognome == cognome))).first()
        if utente_exist:
            messaggio = "Utente già presente (email oppure nome+cognome già esistenti)."
        else:
            nuovo_utente = Utente(nome=nome, cognome=cognome, email=email)
            db.session.add(nuovo_utente)
            db.session.commit()
            messaggio = f'Utente {nome} {cognome} aggiunto con successo!'
    return render_template("adduser.html", messaggio=messaggio)

@app.route('/utenti')
def utenti():
    query = request.args.get('query', '')
    messaggio = request.args.get('messaggio', None)
    if query:
        lista_utenti = Utente.query.filter(
            (Utente.nome.ilike(f'%{query}%')) | (Utente.cognome.ilike(f'%{query}%')) | (Utente.email.ilike(f'%{query}%'))
        ).all()
    else:
        lista_utenti = Utente.query.all()
    return render_template("utenti.html", utenti=lista_utenti, messaggio=messaggio)

@app.route('/elimina/<int:id>')
def elimina(id):
    utente = Utente.query.get_or_404(id)
    db.session.delete(utente)
    db.session.commit()
    return redirect(url_for('utenti', messaggio=f"Utente {utente.nome} {utente.cognome} eliminato."))

@app.route('/modifica/<int:id>', methods=['GET', 'POST'])
def modifica(id):
    utente = Utente.query.get_or_404(id)
    messaggio = None
    if request.method == 'POST':
        nuovo_nome = request.form['nome']
        nuovo_cognome = request.form['cognome']
        nuova_email = request.form['email']
        # Controllo duplicati: email o combinazione nome+cognome diversa dall'utente attuale
        utente_exist = Utente.query.filter(
            ((Utente.email == nuova_email) | ((Utente.nome == nuovo_nome) & (Utente.cognome == nuovo_cognome)))
            & (Utente.id != utente.id)
        ).first()
        if utente_exist:
            messaggio = "Altro utente con questi dati già presente (email o nome+cognome)."
        else:
            utente.nome = nuovo_nome
            utente.cognome = nuovo_cognome
            utente.email = nuova_email
            db.session.commit()
            return redirect(url_for('utenti', messaggio=f"Utente {utente.nome} {utente.cognome} modificato con successo!"))
    return render_template("modifica.html", utente=utente, messaggio=messaggio)

@app.route('/')
def home():
    return redirect(url_for('utenti'))

if __name__ == '__main__':
    app.run(debug=True)
```
# Gestire autenticazione e ruoli in Flask
Gestire autenticazione e ruoli in Flask è un passaggio fondamentale per qualsiasi app.
Per una soluzione professionale e veloce si usa la libreria `Flask-Login` (per login/logout) insieme a un campo “ruolo” nella tabella utenti.
In più, per la gestione delle password in modo sicuro, si usa `Werkzeug` (già incluso in Flask) per l’hash delle password.

**Passaggi base:**
## 1. Installa Flask-Login
```bash
# crea il virtual environment
python -m venv venv
source venv/bin/activate  # su Linux/Mac
venv\Scripts\activate  # su Windows
# poi installa Flask-Login
pip install Flask-Login
```
## 2. Modifica il modello Utente
Aggiungi almeno questi campi:

- password_hash (hash della password, mai in chiaro)
- ruolo (es: "admin", "utente", "editor", ecc.)

E rendi il modello compatibile con Flask-Login:

```python
from flask_login import UserMixin  # user mixin serve in modo da avere la compatibilita con Flask-Login
from werkzeug.security import generate_password_hash, check_password_hash

class Utente(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    cognome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    ruolo = db.Column(db.String(20), nullable=False, default='utente')  # <-- nuovo campo

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```
> Nota: Dopo aver aggiunto i nuovi campi, crea una migrazione (flask db migrate + flask db upgrade).
```bash
flask db migrate -m "Aggiungi campi ruolo e password_hash"
flask db upgrade
```
## 3. Configura Flask-Login nell’app
Nel file app.py:

```python
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # rotta che mostra la form di login
app.secret_key = 'la_tua_chiave_segreta'  # chiave segreta per sessioni

@login_manager.user_loader
def load_user(user_id):
    return Utente.query.get(int(user_id))
```
## 4. Crea la form di login
login.html (esempio):

```html
<!doctype html>
<html>
  <head><title>Login</title></head>
  <body>
    <h1>Login</h1>
    <form method="POST">
      Email: <input type="email" name="email"><br>
      Password: <input type="password" name="password"><br>
      <input type="submit" value="Accedi">
    </form>
    {% if messaggio %}
      <p>{{ messaggio }}</p>
    {% endif %}
  </body>
</html>
```
versione con template Jinja2
login.html (esempio):
```html
{% extends "base.html" %}

{% block title %}Login{% endblock %}

{% block content %}
<h2>Login</h2>
  <form method="POST">
    Email: <input type="email" name="email" value="{{ utente.email }}" required>
    Password: <input type="password" name="password" required>
    {% if messaggio %}
      <p>{{ messaggio }}</p>
    {% endif %}
    <input type="submit" value="Invia">
  </form>
  {% if nome %}
    <p>Ciao, {{ nome }}!</p>
  {% endif %}

{% endblock %}
```
## 5. La rotta per il login
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    messaggio = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        utente = Utente.query.filter_by(email=email).first()
        if utente and utente.check_password(password):
            login_user(utente)
            return redirect(url_for('utenti'))
        else:
            messaggio = "Email o password errati!"
    return render_template("login.html", messaggio=messaggio)
```
## 6. Rotta per il logout
```python
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
```
Se si vuole avere unq rotta specifica del logout in modo da mostrare un messaggio di successo, si può fare così:

```python
@app.route('/logout')
@login_required
def logout():
    logout_user()
    # return redirect(url_for('login'))
    return render_template("logout.html")
```
logout.html (esempio):
```html
{% extends "base.html" %}

{% block title %}Logout{% endblock %}

{% block content %}
  <h2>Logout</h2>
  <p>Logout effettuato con successo!</p>
  <a href="{{ url_for('login') }}">Vai al login</a>
{% endblock %}
```
## 7. Navber con lo stato di login dell'utente
Possiamo mostrare nella navbar lo stato dell utente (se è loggato o meno) e il suo nome usando il template header.html:
navbar dinamica (header.html):
```html
<header>
  <nav>
    <a href="{{ url_for('home') }}">Home</a>
    <a href="{{ url_for('utenti') }}">Utenti</a>
    <a href="{{ url_for('adduser') }}">Aggiungi utente</a>
    {% if current_user.is_authenticated %}
      <span style="margin-left: 2em;">
        👤 {{ current_user.nome }}
        [ruolo: {{ current_user.ruolo }}]
      </span>
      <a href="{{ url_for('logout') }}" style="margin-left: 1em;">Logout</a>
    {% else %}
      <span style="margin-left: 2em; color: #888;">Non autenticato</span>
      <a href="{{ url_for('login') }}" style="margin-left: 1em;">Login</a>
    {% endif %}
  </nav>
  <hr>
</header>
```
Se l’utente è autenticato, nella navbar apparirà:
> 👤 Nome [ruolo: admin] e il link Logout.

Se non è autenticato, appare “Non autenticato” e il link Login

## Mostrare un link solamente ad un ruolo specifico
Per mostrare un link solo a un ruolo specifico, puoi usare un controllo condizionale nel template:

```html
{% if current_user.is_authenticated and current_user.ruolo == 'admin' %}
  <a href="{{ url_for('admin_panel') }}">Area Admin</a>
{% endif %}
```
```css
nav {
  display: flex;
  align-items: center;
  gap: 1em;
}
nav a {
  text-decoration: none;
  color: #0a47a1;
}
nav span {
  font-weight: bold;
}
```

## 8. Proteggere una rotta (solo utenti loggati)
Aggiungi il decoratore:

```python
@app.route('/area_riservata')
@login_required
def area_riservata():
    return f'Ciao {current_user.nome}, sei nell’area riservata!'
```
## 9. Proteggere una rotta per ruolo specifico (es: solo admin) ->
Crea un decoratore personalizzato:
```python
from functools import wraps
from flask import abort

def ruolo_required(ruolo):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.ruolo != ruolo:
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
```
Usa così:

```python
@app.route('/admin')
@ruolo_required('admin')
def admin_panel():
    return 'Sei nell’area admin!'
```
Puoi creare decoratori simili per più ruoli, o controllare più ruoli dentro la funzione.

## 10. Il link corrente nella navbar

Per evidenziare il link corrente nella navbar, puoi usare la variabile request.endpoint di Flask e confrontarla con l’endpoint di ogni pagina

header.html:
```html
<header>
  <nav>
    <a href="{{ url_for('home') }}"
       {% if request.endpoint == 'home' %}style="font-weight: bold;"{% endif %}>
      Home
    </a>
    <a href="{{ url_for('utenti') }}"
       {% if request.endpoint == 'utenti' %}style="font-weight: bold;"{% endif %}>
      Utenti
    </a>
    <a href="{{ url_for('adduser') }}"
       {% if request.endpoint == 'adduser' %}style="font-weight: bold;"{% endif %}>
      Aggiungi utente
    </a>
    {% if current_user.is_authenticated %}
      <span style="margin-left: 2em;">
        👤 {{ current_user.nome }} [ruolo: {{ current_user.ruolo }}]
      </span>
      <a href="{{ url_for('logout') }}" {% if request.endpoint == 'logout' %}style="font-weight: bold;"{% endif %} style="margin-left: 1em;">
        Logout
      </a>
    {% else %}
      <span style="margin-left: 2em; color: #888;">Non autenticato</span>
      <a href="{{ url_for('login') }}"
         {% if request.endpoint == 'login' %}style="font-weight: bold;"{% endif %} style="margin-left: 1em;">
        Login
      </a>
    {% endif %}
  </nav>
  <hr>
</header>
```
## Come funziona:
Flask passa sempre l’oggetto request ai template.

Ogni route ha un endpoint (il nome della funzione della view).

Con {% if request.endpoint == 'nome_funzione' %} puoi confrontare se sei nella pagina corrente e applicare lo stile grassetto.

Puoi anche usare una classe CSS al posto di style, esempio:

```html
<a href="{{ url_for('home') }}"
   class="{% if request.endpoint == 'home' %}active{% endif %}">Home</a>
```
in style.css:

```css
.active { font-weight: bold; }
```

## 2. CSS migliore con classi
header.html:

```html
<a href="{{ url_for('home') }}" class="{% if request.endpoint == 'home' %}active{% endif %}">Home</a>
```
style.css:

```css
.active {
  font-weight: bold;
  text-decoration: underline;
}
```
# 1. Statico vs Dinamico

**Pagina Statica**

- Cos’è: un file (HTML, CSS, JS, immagini…) che viene servito “così com’è” al client.

Caratteristiche:

- Nessuna elaborazione lato server: il contenuto non cambia in base all’utente né a variabili runtime.
- Veloce da servire, può essere messo su CDN.

> In Flask: si mette in static/ e si richiamano con url_for('static', filename='stile.css').

```html
<!-- es. static/index.html -->
<!doctype html>
<html>
  <head><link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}"></head>
  <body>
    <h1>Benvenuto!</h1>
  </body>
</html>
```
**Pagina Dinamica**

- Cos’è: un template (es. Jinja2) che Flask elabora al volo, sostituendo variabili e logica.

Caratteristiche:

- Il server costruisce l’HTML in base a dati (database, input utente, orari…).
- Utile per siti e app che cambiano frequentemente o personalizzati per ogni utente.

> In Flask: si mette in templates/ e si usa render_template():

```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/profilo/<username>')
def profilo(username):
    dati_utente = get_user_data(username)   # es. query DB
    return render_template('profilo.html', user=dati_utente)
```
```html
<!-- es. templates/profilo.html -->
<h1>Ciao, {{ user.name }}!</h1>
<p>Email: {{ user.email }}</p>
```
## 2. Sincrono vs Asincrono
**Richiesta Sincrona**

- Flusso: il browser invia la richiesta HTTP e “aspetta” la risposta interamente (page reload).

Comportamento:

- Blocca il thread finché il server non risponde: l’utente vede “loading…” fino al completamento.
- Semplice da implementare ma meno fluido (full page refresh).

Esempio: un form che fa POST e poi viene reindirizzato:t

```html
<form action="/invia" method="post">
  <input name="commento">
  <button type="submit">Invia</button>
</form>
```
```python
@app.route('/invia', methods=['POST'])
def invia_commento():
    testo = request.form['commento']
    salva_commento(testo)
    return redirect('/grazie')
```
**Richiesta Asincrona (AJAX / Fetch)**

- Flusso: il browser invia la richiesta “dietro le quinte” (JS) e aggiorna solo parte della pagina senza ricaricare tutto.

Comportamento:

- Più reattivo: si possono aggiornare sezioni (es. lista commenti) senza full reload.
- Richiede JavaScript client-side (fetch, XMLHttpRequest o librerie come Axios).

Esempio:

```html
<!-- parte di pagina HTML -->
<div id="commenti"></div>
<input id="nuovo-commento"><button id="btn">Invia</button>

<script>
document.getElementById('btn').onclick = async () => {
  let testo = document.getElementById('nuovo-commento').value;
  let resp = await fetch('/api/commenti', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ testo })
  });
  let dati = await resp.json();     // ricevo commenti aggiornati
  document.getElementById('commenti').innerHTML =
    dati.map(c=>`<p>${c.user}: ${c.text}</p>`).join('');
};
</script>
```
```python
from flask import jsonify, request

@app.route('/api/commenti', methods=['POST'])
def api_commenti():
    data = request.get_json()
    salva_commento(data['testo'])
    tutti = carica_commenti()
    return jsonify(tutti)
```
**Statico + Sincrono**
– Siti vetrina, landing pages, blog con hosting su CDN.

**Dinamico + Sincrono**
– Applicazioni tradizionali Flask con page reload per ogni azione (crud, autenticazione).

**Dinamico + Asincrono**
– Dashboard in tempo reale, chat, aggiornamenti parziali (infinite scroll, notifiche).

Flask tradizionalmente è sincrono, ma dalla 2.x supporta route async:

```python
@app.route('/async')
async def pagina_async():
    dati = await chiamata_io()   # es. HTTP esterno o DB asincrono
    return render_template('async.html', data=dati)
```
Tieni però conto che per sfruttare veramente l’asincronia devi usare un server ASGI (es. Hypercorn, Uvicorn) e librerie di database/HTTP compatibili con asyncio

# Flask-SocketIO

Flask-SocketIO estende Flask per supportare WebSocket e comunicazione in tempo reale.
Permette di creare applicazioni che comunicano in modo bidirezionale tra client e server, ideale per chat, notifiche, giochi online.

Il polling è un metodo tradizionale in cui il client invia richieste periodiche al server per verificare se ci sono nuovi dati. Questo può causare ritardi e inefficienze, specialmente in applicazioni con aggiornamenti frequenti.

Flask-SocketIO elimina la necessità di polling, permettendo al server di inviare dati ai client in tempo reale e viceversa, senza ricaricare la pagina.

Il polling non è più necessario: il server può inviare dati ai client in tempo reale, e i client possono inviare eventi al server senza dover ricaricare la pagina.

## Installazione

crea un ambiente virtuale e installa Flask-SocketIO e le dipendenze necessarie:

```bash
python -m venv venv
source venv/bin/activate  # su Linux/Mac
venv\Scripts\activate  # su Windows
# installa Flask-SocketIO e le dipendenze
pip install flask flask-socketio eventlet
```
## Esempio di base

- ogni utente può lanciare un dado;
- il risultato viene emesso a tutti i client in tempo reale;
- il tutto funziona senza polling, solo con WebSocket.
app.py
```python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersegreto'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

ultimo_valore = None

@app.route('/')
def index():
    return render_template('dado.html')

@socketio.on('lancia_dado')
def handle_lancio():
    global ultimo_valore
    valore = random.randint(1, 6)
    ultimo_valore = valore
    emit('nuovo_risultato', {'valore': valore}, broadcast=True)

@socketio.on('connect')
def handle_connect():
    if ultimo_valore is not None:
        emit('nuovo_risultato', {'valore': ultimo_valore})

if __name__ == '__main__':
    socketio.run(app, debug=True)
```
templates/dado.html
```html
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Lancio del Dado</title>
  <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
  <script>
    const socket = io();  {# connessione al server WebSocket #}

    socket.on('connect', () => {
      console.log('Connesso al server WebSocket');
    });

    function lanciaDado() {
      socket.emit('lancia_dado');  {# invia evento al server per lanciare il dado #}
    }

    socket.on('nuovo_risultato', data => {
      document.getElementById('risultato').innerText = data.valore;  {# aggiorna il risultato nella pagina #}
    });
  </script>
</head>
<body>
  <h1>Lancio del Dado</h1>
  <button onclick="lanciaDado()">Lancia!</button>
  <h2>Ultimo risultato: <span id="risultato">---</span></h2>
</body>
</html>
```
# Versione multigiocatore:

- Ogni giocatore si sceglie un nome.
- Può lanciare il proprio dado.
- Tutti vedono il lancio dell’altro con nome e valore.
- Viene mantenuta la lista degli ultimi lanci (es. cronologia in chat)

app.py
```python
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersegreto'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Lista lanci recenti (max 10)
storico_lanci = []

@app.route('/')
def index():
    return render_template('gioco.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    join_room(request.sid)
    emit('chat', {'messaggio': f"{username} si è connesso."}, broadcast=True)

@socketio.on('lancia_dado')
def handle_lancia(data):
    username = data['username']
    valore = random.randint(1, 6)
    messaggio = f"{username} ha lanciato un {valore}"
    storico_lanci.append(messaggio)
    if len(storico_lanci) > 10:
        storico_lanci.pop(0)
    emit('nuovo_lancio', {'username': username, 'valore': valore, 'storico': storico_lanci}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```
templates/gioco.html
```html
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Lancio del Dado Multiplayer</title>
  <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
  <style>
    body { font-family: sans-serif; padding: 20px; }
    #log { border: 1px solid #ccc; padding: 10px; height: 200px; overflow-y: scroll; background: #f9f9f9; }
    #risultato { font-size: 24px; margin-top: 10px; }
  </style>
</head>
<body>

<h1>Dado Multiplayer</h1>

<div>
  <label for="username">Nome:</label>
  <input id="username" placeholder="Inserisci nome">
  <button onclick="connetti()">Entra</button>
</div>

<div id="gioco" style="display:none;">
  <button onclick="lancia()">Lancia il dado</button>
  <div id="risultato">Aspetta il tuo turno...</div>
  <h3>Storico lanci:</h3>
  <div id="log"></div>
</div>

<script>
let socket;
let username = '';

function connetti() {
  username = document.getElementById('username').value.trim();
  if (!username) return alert("Inserisci un nome!");

  document.getElementById('gioco').style.display = 'block';
  socket = io();

  socket.emit('join', { username });

  socket.on('nuovo_lancio', data => {
    document.getElementById('risultato').innerText = `${data.username} ha ottenuto: ${data.valore}`;
    aggiornaStorico(data.storico);
  });

  socket.on('chat', data => {
    aggiungiMessaggio(data.messaggio);
  });
}

function lancia() {
  socket.emit('lancia_dado', { username });
}

function aggiornaStorico(lista) {
  const log = document.getElementById('log');
  log.innerHTML = '';
  for (let m of lista) {
    log.innerHTML += `<div>${m}</div>`;
  }
  log.scrollTop = log.scrollHeight;
}

function aggiungiMessaggio(msg) {
  const log = document.getElementById('log');
  log.innerHTML += `<div><em>${msg}</em></div>`;
  log.scrollTop = log.scrollHeight;
}
</script>

</body>
</html>
```
# Esegui nel terminale:

Su Windows:
```bash
ipconfig
```