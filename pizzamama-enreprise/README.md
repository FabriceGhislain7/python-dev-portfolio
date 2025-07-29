# PizzaMama Enterprise - Setup Guide

## 🚀 Guida Completa Setup Professionale

### Prerequisiti
- Python 3.9+ installato
- PowerShell o Command Prompt
- Git (opzionale ma consigliato)

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

## 🏗️ Step 7: Creazione Apps Enterprise

### 7.1 Crea cartella apps/ (devi essere in src/)
```powershell
mkdir apps
cd apps
```

### 7.2 Crea file __init__.py per package Python
```powershell
# Windows PowerShell
New-Item -Path "__init__.py" -ItemType File -Force
```

### 7.3 Crea le app Django una alla volta
```powershell
# Crea app accounts (gestione utenti)
py ../manage.py startapp accounts

# Crea app products (catalogo pizze)
py ../manage.py startapp products

# Crea app orders (gestione ordini)
py ../manage.py startapp orders
```

### 7.4 Verifica struttura creata
```powershell
ls
```

**📁 Dovresti vedere:**
```
apps/
├── __init__.py
├── accounts/
├── products/
└── orders/
```

### 7.5 Configura apps nei Django settings
**Torna in src/ e modifica settings.py:**
```powershell
cd ..
code pizzamama/settings.py
```

**Aggiorna `INSTALLED_APPS`:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    
    # Local apps
    'apps.accounts',    # ← AGGIUNGI
    'apps.products',    # ← AGGIUNGI
    'apps.orders',      # ← AGGIUNGI
]
```

### 7.6 Fix configurazione app (IMPORTANTE!)
**Per ogni app creata, modifica il file `apps.py`:**

**`apps/accounts/apps.py`:**
```python
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'  # ← Cambia da 'accounts' a 'apps.accounts'
```

**`apps/products/apps.py`:**
```python
from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'  # ← Cambia da 'products' a 'apps.products'
```

**`apps/orders/apps.py`:**
```python
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'  # ← Cambia da 'orders' a 'apps.orders'
```

### 7.7 Test configurazione
```powershell
py manage.py check
```

**✅ Output atteso:** `System check identified no issues (0 silenced).`

### 7.8 Crea migrazioni iniziali (opzionale)
```powershell
py manage.py makemigrations accounts
py manage.py makemigrations products
py manage.py makemigrations orders
```

**📋 Output atteso:** `No changes detected` (normale, non ci sono ancora modelli custom)

---

## 📂 Struttura Attuale del Progetto

```
pizzamama-enreprise/
├── venv/                    ← Ambiente virtuale
├── src/                     ← Codice sorgente (approccio enterprise)
│   ├── manage.py           ← Comando principale Django
│   ├── db.sqlite3          ← Database SQLite (creato dopo migrate)
│   ├── apps/               ← Apps business logic (NUOVO!)
│   │   ├── __init__.py
│   │   ├── accounts/       ← Gestione utenti
│   │   ├── products/       ← Catalogo pizze
│   │   └── orders/         ← Gestione ordini
│   └── pizzamama/          ← Configurazioni progetto Django
│       ├── __init__.py
│       ├── settings.py     ← Tutte le configurazioni
│       ├── urls.py         ← URL routing con API
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
- [x] Apps enterprise create (accounts, products, orders)
- [x] Struttura moduli configurata

### 🔄 Prossimi Step (da completare)
- [x] Django REST Framework (API)
- [x] Struttura apps (accounts, products, orders, etc.)
- [ ] Models e database design
- [ ] PostgreSQL setup (database produzione)
- [ ] Frontend templates
- [ ] Sistema autenticazione custom
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

Finora, abbiamo completato il setup enterprise di **PizzaMama**! 

### 🏗️ **Architettura Enterprise Creata:**
- ✅ **Ambiente isolato** con virtual environment
- ✅ **Django 5.0.1** con best practices
- ✅ **API REST** con Django REST Framework
- ✅ **Struttura modulare** con apps separate
- ✅ **Database** SQLite per development
- ✅ **Admin panel** funzionante con superuser

### 📦 **Apps Business Logic:**
- ✅ **`apps.accounts`** → Gestione utenti e autenticazione
- ✅ **`apps.products`** → Catalogo pizze e ingredienti
- ✅ **`apps.orders`** → Carrello e gestione ordini

### 🔗 **API Endpoints Attivi:**
- **`/admin/`** → Panel amministrazione Django
- **`/api/`** → Homepage API con informazioni
- **`/api/auth/login/`** → Interfaccia login DRF
- **`/api/auth/logout/`** → Interfaccia logout DRF

Il progetto è ora pronto per:
1. **📊 Database modeling** → Creare modelli User, Pizza, Order
2. **🎨 Frontend development** → Templates e interfacce
3. **🔐 Authentication system** → Login, registrazione, profili
4. **💳 Payment integration** → Stripe, PayPal
5. **🤖 ML features** → Raccomandazioni, analytics
6. **🚀 Production deployment** → Docker, PostgreSQL

**Prossimo step:** Creazione modelli database enterprise per gestire utenti, prodotti e ordini!