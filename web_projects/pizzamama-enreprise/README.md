# PizzaMama Enterprise - Setup Guide

## 🚀 Guida Completa Setup Professionale

### Prerequisiti
- Python 3.9+ installato
- PowerShell o Command Prompt
- Git (opzionale ma consigliato)

---

## 🌐 Step 6: Django REST Framework Setup

### 6.1 Installa Django REST Framework
```powershell
py -m pip install djangorestframework==3.14.0
```

**📋 Cosa installa:**
- `djangorestframework==3.14.0` → Framework API REST
- `pytz` → Gestione timezone (dipendenza DRF)

### 6.2 Configura DRF in settings.py
**Apri `src/pizzamama/settings.py` e modifica:**

**Aggiungi a `INSTALLED_APPS`:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',          # ← AGGIUNGI QUESTA RIGA
]
```

**Aggiungi alla fine del file:**
```python
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

### 6.3 Configura URL API
**Modifica `src/pizzamama/urls.py`:**
```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Benvenuto alle API di PizzaMama!',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api-auth': '/api/auth/login/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),           # ← Homepage API
    path('api/auth/', include('rest_framework.urls')), # ← Login/logout DRF
]
```

### 6.4 Test API
```powershell
py manage.py runserver
```

**🔗 URL da testare:**
- `http://127.0.0.1:8000/api/` → Vista benvenuto API (JSON)
- `http://127.0.0.1:8000/api/auth/login/` → Login DRF
- `http://127.0.0.1:8000/admin/` → Admin Django

**🎯 Risultato atteso:** Interfaccia API browsable di DRF con messaggio di benvenuto

---

## 📁 Step 1: Creazione Ambiente e Struttura

### 1.1 Crea la directory del progetto
```powershell
mkdir pizzamama-enreprise
cd pizzamama-enreprise
```

### 1.2 Crea ambiente virtuale
```powershell
py -m venv venv
```

### 1.3 Attiva ambiente virtuale
```powershell
# Windows PowerShell
.\venv\Scripts\activate

# Windows CMD
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**✅ Verifica:** Dovresti vedere `(venv)` all'inizio del prompt

---

## 📦 Step 2: Installazione Django

### 2.1 Aggiorna pip (opzionale ma consigliato)
```powershell
py -m pip install --upgrade pip
```

### 2.2 Installa Django
```powershell
py -m pip install Django==5.0.1
```

**📋 Cosa installa:**
- `Django==5.0.1` → Framework web principale
- `asgiref` → Supporto ASGI per apps asincrone
- `sqlparse` → Parser SQL per Django ORM
- `tzdata` → Database timezone
- `typing_extensions` → Type hints avanzati

---

## 🏗️ Step 3: Creazione Progetto Django

### 3.1 Crea directory src/ (approccio enterprise)
```powershell
mkdir src
cd src
```

### 3.2 Crea progetto Django
```powershell
django-admin startproject pizzamama .
```

**📁 Struttura creata:**
```
src/
├── manage.py          ← File principale Django
└── pizzamama/         ← Configurazioni progetto
    ├── __init__.py
    ├── settings.py    ← Configurazioni Django
    ├── urls.py        ← URL routing principale
    ├── wsgi.py        ← Server produzione
    └── asgi.py        ← Server asincrono
```

**🎯 Spiegazione comando:**
- `django-admin` → Tool CLI di Django
- `startproject` → Crea nuovo progetto
- `pizzamama` → Nome del progetto
- `.` → Crea nella directory corrente (importante!)

---

## ✅ Step 4: Test Installazione

### 4.1 Avvia server di sviluppo
```powershell
py manage.py runserver
```

**📊 Output atteso:**
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
You have 18 unapplied migration(s)...
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 4.2 Verifica nel browser
- Apri: `http://127.0.0.1:8000/`
- Dovresti vedere: "The install worked successfully! Congratulations!"

### 4.3 Ferma il server
```powershell
# Premi Ctrl+C (o Ctrl+Break su Windows)
```

---

## 🗄️ Step 5: Setup Database

### 5.1 Applica migrazioni iniziali
```powershell
py manage.py migrate
```

**📋 Cosa succede:**
- Crea database SQLite (`db.sqlite3`)
- Crea tabelle: User, Session, Admin, ContentType, Permission
- Setup necessario per sistema autenticazione Django

### 5.2 Crea superuser per admin
```powershell
py manage.py createsuperuser
```

**📝 Ti chiederà:**
- **Username:** (es. `admin`)
- **Email:** (opzionale, premi Enter)
- **Password:** (non si vede mentre scrivi)

### 5.3 Test admin panel
```powershell
py manage.py runserver
```
- Vai su: `http://127.0.0.1:8000/admin/`
- Login con le credenziali create

---

## 📂 Struttura Attuale del Progetto

```
pizzamama-enreprise/
├── venv/                    ← Ambiente virtuale
├── src/                     ← Codice sorgente (approccio enterprise)
│   ├── manage.py           ← Comando principale Django
│   ├── db.sqlite3          ← Database SQLite (creato dopo migrate)
│   └── pizzamama/          ← Configurazioni progetto Django
│       ├── __init__.py
│       ├── settings.py     ← Tutte le configurazioni
│       ├── urls.py         ← URL routing
│       ├── wsgi.py         ← Server produzione
│       └── asgi.py         ← Server asincrono
└── structure.py            ← File di esempio (da rimuovere)
```

---

## 🎯 Stato Attuale

### ✅ Completato
- [x] Ambiente virtuale Python
- [x] Django 5.0.1 installato
- [x] Progetto Django creato
- [x] Database setup (SQLite)
- [x] Admin panel funzionante
- [x] Server di sviluppo testato
- [x] Django REST Framework installato
- [x] API endpoint di benvenuto configurato

### 🔄 Prossimi Step (da completare)
- [x] Django REST Framework (API)
- [ ] PostgreSQL setup (database produzione)
- [ ] Struttura apps (accounts, products, orders, etc.)
- [ ] Models e database design
- [ ] Frontend templates
- [ ] Sistema autenticazione
- [ ] File statici e media
- [ ] Docker setup
- [ ] Testing framework
- [ ] CI/CD pipeline

---

## 🛠️ Comandi Utili

### Development
```powershell
# Attiva ambiente
.\venv\Scripts\activate

# Avvia server
py manage.py runserver

# Nuove migrazioni
py manage.py makemigrations

# Applica migrazioni
py manage.py migrate

# Shell Django
py manage.py shell

# Crea nuova app
py manage.py startapp nome_app
```

### Troubleshooting
```powershell
# Verifica installazioni
py -m pip list

# Reinstalla Django
py -m pip uninstall Django
py -m pip install Django==5.0.1

# Reset database (ATTENZIONE: cancella tutti i dati)
rm db.sqlite3
py manage.py migrate
py manage.py createsuperuser
```

---

## 📚 File Importanti Spiegati

### `manage.py`
File principale per tutti i comandi Django:
- `runserver` → Avvia server sviluppo
- `migrate` → Applica migrazioni database
- `createsuperuser` → Crea admin user
- `startapp` → Crea nuova app Django

### `settings.py`
Tutte le configurazioni Django:
- Database connection
- Apps installate
- Middleware
- Static files
- Security settings

### `urls.py`
Routing URL principale:
- Mappa URL a views
- Include URL di altre apps
- Admin panel routing

---

## 🔧 Environment Setup

### Windows PowerShell
```powershell
# Se hai problemi con pip, usa sempre:
py -m pip install package_name

# Per evitare problemi PowerShell execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Variabili Ambiente (per dopo)
```powershell
# Creeremo file .env per:
# - Database credentials
# - Secret keys
# - API keys
# - Debug settings
```

---

## 🎉 Congratulazioni!

Finora, abbiamo completato il setup base di **PizzaMama Enterprise**!

Il progetto è ora pronto per:
1. **Sviluppo delle apps** (products, orders, etc.)
2. **API development** con Django REST Framework
3. **Database modeling** professionale
4. **Frontend integration**
5. **Testing e deployment**

**Prossimo step:** Installazione Django REST Framework e creazione struttura apps enterprise!