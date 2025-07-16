# Gioco di Ruolo - Web App Flask

## Obiettivo

Portare il gioco di ruolo in versione web, organizzando l'app con moduli Flask separati e struttura OOP per:

* Creazione e gestione dei personaggi
* Selezione delle missioni
* Combattimento con logica a turni
* Inventario e oggetti con effetti diversi
* Salvataggio e caricamento dello stato di gioco

---

## Setup Iniziale

### Ambiente Virtuale

```bash
python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Installazione Dipendenze

```bash
pip install Flask Flask-SQLAlchemy Flask-Login Flask-Session
```

---

## Struttura del Progetto

```
gdr-web-app/
│
├── app.py                     # Entry point Flask, registra i blueprint
├── requirements.txt           # Dipendenze del progetto
├── README.md                  # Documentazione
│
├── venv/                      # Ambiente virtuale
│
├── static/                    # CSS, JS, immagini (es. ambiente.jpg)
│
├── templates/                 # Template Jinja2
│   ├── layout.html
│   ├── index.html
│   ├── menu.html
│   ├── create_char.html
│   ├── select_mission.html
│   ├── battle.html
│   ├── guide_game.html
│   ├── credits.html
│   └── ...
│
├── data/                      # Eventuali salvataggi (es. salvataggio.json)
│
├── utils/                     # Moduli condivisi
│   ├── log.py
│   ├── messaggi.py
│   └── salvataggio.py
│
├── gioco/                     # Logica principale
│   ├── __init__.py
│   ├── ambiente.py
│   ├── basic.py
│   ├── classi.py
│   ├── inventario.py
│   ├── missione.py
│   ├── oggetto.py
│   ├── personaggio.py
│   ├── scontro.py
│   ├── strategy.py
│   └── routes.py
│
├── battle/                    # Modulo battaglia
│   ├── __init__.py
│   └── routes.py
│
├── characters/                # Modulo gestione personaggi
│   ├── __init__.py
│   └── routes.py
│
├── environment/               # Ambienti disponibili
│   ├── __init__.py
│   └── routes.py
│
├── inventory/                 # Inventario dei personaggi
│   ├── __init__.py
│   └── routes.py
│
├── mission/                   # Missioni selezionabili
│   ├── __init__.py
│   └── routes.py
```

---

## Blueprint: Uso e Vantaggi

Un Blueprint in Flask consente di organizzare il codice in moduli riutilizzabili. È utile per:

* Separare le rotte per area funzionale (`gioco`, `inventory`, ecc.)
* Facilitare manutenzione e scalabilità
* Evitare import circolari

### Registrazione in `app.py`

```python
from flask import Flask
from flask_session import Session
from gioco.routes import gioco
from inventory.routes import inventory
from mission.routes import mission
# ...

app = Flask(__name__)
app.config['SECRET_KEY'] = '...'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.register_blueprint(gioco)
app.register_blueprint(inventory)
app.register_blueprint(mission)
# ...
```

---

## Route Chiave

| Route             | Descrizione                        |
| ----------------- | ---------------------------------- |
| `/`               | Menu principale                    |
| `/new-game`       | Creazione compagnia/personaggi     |
| `/load-game`      | Caricamento stato da file/sessione |
| `/select-mission` | Selezione missione                 |
| `/battle`         | Combattimento a turni              |
| `/inventory`      | Visualizzazione oggetti/personaggi |
| `/save-game`      | Esporta salvataggio in JSON        |

---

## Concetti Avanzati

### Serializzazione degli Oggetti

Ogni classe importante (es. Personaggio, Missione) deve:

```python
def to_dict(self): ...
@classmethod
def from_dict(cls, data): ...
```

Serve per salvataggio in sessione o file.

### Factory Pattern

Per ambienti, missioni e classi personaggio:

* `.get_opzioni()` – restituisce opzioni da mostrare
* `.seleziona_da_id(id)` – restituisce oggetto istanziato

### Sessione

* Salva oggetti Python convertiti in dict
* Memorizza lo stato di gioco (scontro attivo, inventario, ecc.)

### Salvataggio

* JSON (leggibile, esportabile)
* Possibile anche in Pickle o database

---

## Static & Template

**Static:**

* `/static/css/` — stili personalizzati
* `/static/js/` — interazioni dinamiche
* `/static/img/` — ambienti, icone, ritratti

**Templates:**

* `layout.html` – base comune
* `menu.html` – schermata principale
* `create_char.html` – creazione personaggi
* `select_mission.html` – missioni disponibili
* `battle.html` – combattimento
* `inventory.html` – visualizzazione inventario
* `guide_game.html` – guida
* `credits.html` – ringraziamenti

---

## Problemi Risolti

### PowerShell non riconosce `python`

Errore:

```
The term 'C:\Python39\python.exe' is not recognized...
```

Soluzione:

```powershell
notepad $PROFILE
```

E commenta la funzione personalizzata `python`.

### `pip3 --list` non funziona

Soluzione:

```bash
pip list
# oppure
python -m pip list
```

---

## Avvio dell’App

Con ambiente attivo:

```bash
python app.py
```

---

## Prossimi Step

* Aggiungere immagini per personaggi e missioni
* Migliorare lo stile con Bootstrap
* Introdurre boss battle o finale narrativo
* Aggiungere interattività con JavaScript (log dinamico)
* Autenticazione con Flask-Login
* Persistenza con Flask-SQLAlchemy
* Scrittura di test automatizzati

user_name : developer
password: ^z%mWE7!v^8q


