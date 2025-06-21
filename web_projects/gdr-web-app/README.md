
# Gioco di Ruolo - Web App Flask

## Obiettivo
Migrare il gioco di ruolo in una versione web, usando Flask per gestire:

- Creazione dei personaggi
- Selezione delle missioni
- Gestione del combattimento
- Inventario e oggetti
- Salvataggio dello stato di gioco

---

## Setup iniziale

### Creazione ambiente virtuale

```bash
python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
````

### Installazione dipendenze

```bash
pip install Flask
pip install Flask-SQLAlchemy
pip install Flask-Login
pip install Flask-Session
```

---

gdr-web-app/
│
├── app.py                     # Entry point dell'applicazione Flask
├── README.md                  # Documentazione del progetto
├── requirements.txt           # Dipendenze del progetto
│
├── venv/                      # Ambiente virtuale Python
│
├── static/                    # File statici (CSS, immagini, JS)
│   └── ambiente.jpg           # Sfondo della homepage (esempio)
│
├── templates/                 # Template HTML (Jinja2)
│   ├── layout.html            # Layout base comune a tutte le pagine
│   ├── index.html             # Homepage
│   ├── guide_game.html        # Guida al gioco
│   ├── credits.html           # Ringraziamenti
│   └── ...                    # Altri template (menu, inventario, ambienti, missioni)
│
├── data/                      # Eventuali dati persistenti (JSON di salvataggio ecc.)
│   └── salvataggio.json       # (opzionale) Salvataggio partite
│
├── gioco/                     # Modulo principale con logica di gioco
│   ├── ambiente.py            # Definizione degli ambienti (Foresta, Palude, Vulcano)
│   ├── basic.py               # Classe base generica
│   ├── classi.py              # Mago, Ladro, Guerriero (specializzazioni di Personaggio)
│   ├── inventario.py          # Gestione inventari e oggetti contenuti
│   ├── missione.py            # Classi per le missioni
│   ├── oggetto.py             # Pozione, bomba, medaglione ecc.
│   ├── personaggio.py         # Classe `Personaggio` e sue logiche (attacco, cura ecc.)
│   ├── scontro.py             # Logica di combattimento
│   ├── strategy.py            # Strategia IA avversari?
│   └── routes.py              # Blueprint Flask per le rotte `/gioco/...`
│
├── environment/               # Blueprint Flask per ambienti (selezione ambiente)
│   └── routes.py              # Gestione delle view dell’ambiente
│
├── inventory/                 # Blueprint Flask per la gestione inventari
│   └── routes.py              # Rotte per visualizzare o modificare l'inventario
│
├── mission/                   # Blueprint Flask per le missioni
│   └── routes.py              # Rotte di selezione, inizio e verifica missioni
│
└── utils/                     # Utility varie (log, messaggi, ecc.)
    ├── log.py                 # Logging semplice su file/testo
    ├── messaggi.py            # Classe Messaggi per accumulare output del gioco
    └── salvataggio.py                    # Altri helper se presenti

```

---

## Blueprint: cosa sono e perché usarli

Un Blueprint in Flask è un "modulo" riutilizzabile con le sue route, template e risorse statiche. Ti aiuta a:

* Organizzare il codice per aree funzionali (es: gioco, auth, API)
* Evitare import circolari
* Riutilizzare le componenti anche in altri progetti

### Esempio di blueprint

```python
# gioco/routes.py
from flask import Blueprint, render_template

gioco = Blueprint('gioco', __name__, template_folder='../templates')

@gioco.route('/')
def index():
    return render_template('menu.html')
```

### Registrazione nel file principale

```python
# app.py
from flask import Flask
from flask_session import Session
from gioco.routes import gioco

app = Flask(__name__)
app.config['SECRET_KEY'] = '...'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.register_blueprint(gioco)
```

---

## Route previste

In `gioco/routes.py`:

* `/` — Menu principale
* `/new-game` — Form per creare la compagnia
* `/load-game` — Caricamento stato salvato
* `/select-mission` — Scelta missione
* `/battle` — Logica e turni di battaglia
* `/inventory` — Visualizzazione oggetti

---

## Templates

Posizionati in `templates/`:

* `layout.html` — Template base con navbar e footer
* `menu.html` — Pagina principale
* `create_char.html` — Form per personaggi
* `select_mission.html` — Lista missioni
* `battle.html` — Combattimento a turni

---

## Concetti avanzati da integrare

### Serializzazione oggetti

Tutte le classi (Personaggio, Missione, Ambiente, ecc.) devono:

* Avere un metodo `to_dict()` per salvare lo stato
* Un metodo `from_dict()` per ricostruirlo

Serve per salvare in sessione o file JSON.

### Factory

* `PersonaggioFactory`, `MissioneFactory`, `AmbienteFactory`
* Metodi:

  * `.get_opzioni()` → restituisce lista opzioni da mostrare nei form
  * `.seleziona_da_id(id)` → istanzia oggetto dalla scelta utente

### Sessione

Salvare in sessione:

* Lo stato della compagnia
* La missione corrente
* Eventualmente l'intero oggetto `Scontro`

### Salvataggio/caricamento file

* Route `/save-game` e `/load-game`
* File JSON o Pickle
* Possibilità di scegliere uno "slot" o scaricare il file

---

## Static files

In `static/` salviamo:

* CSS personalizzati
* JS per interazioni dinamiche
* Immagini (icone, sfondi, ritratti PG)

---

## Problemi risolti durante lo sviluppo

### Errore: `python` non riconosciuto in PowerShell

Messaggio:

```
The term 'C:\Python39\python.exe' is not recognized...
```

Soluzione: modifica `$PROFILE` con:

```powershell
notepad $PROFILE
```

E commenta la riga:

```powershell
function python { & 'C:\Python39\python.exe' @args }
```

### Errore: `pip3 --list` non funziona

Messaggio:

```
no such option: --list
```

Soluzione:

```bash
pip list
# oppure
py -m pip list
```

---

## Avvio dell’app

Con ambiente attivo:

```bash
python app.py
```

---

## Prossimi step consigliati

* Aggiunta immagini (personaggi, missioni)
* Stile personalizzato con Bootstrap
* Modalità "boss battle" o finale
* Effetti dinamici via JS (es. log a scorrimento automatico)

