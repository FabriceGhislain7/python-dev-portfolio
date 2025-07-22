# Step 2: Installazione Django

## Obiettivo
Installare Django 5.0.1 nell'ambiente virtuale isolato e comprendere le dipendenze installate per preparare il framework web enterprise.

---

## Prerequisiti
- **Step 1 completato** → Ambiente virtuale attivo
- **(venv) visibile** nel prompt PowerShell
- **Python funzionante** nell'ambiente isolato

---

## Flowchart Step 2

```mermaid
flowchart TD
    A[Inizio con ambiente venv attivo] --> B{Ambiente virtuale attivo?<br/>Prompt mostra venv?}
    B -->|No| C[Attiva ambiente<br/>.\venv\Scripts\activate]
    B -->|Sì| D[Aggiorna pip<br/>py -m pip install --upgrade pip]
    C --> D
    
    D --> E[Installa Django 5.0.1<br/>py -m pip install Django==5.0.1]
    E --> F[Verifica installazione<br/>pip list | django --version]
    
    F --> G{Django installato correttamente?}
    G -->|Sì| H[Analizza dipendenze installate<br/>asgiref, sqlparse, tzdata, typing_extensions]
    G -->|No| I[Troubleshooting<br/>Errori di rete/permessi?]
    
    I --> J[Fix problemi<br/>Proxy/Admin/Cache]
    J --> E
    
    H --> K[Step 2 Completato<br/>Django 5.0.1 Ready]
    K --> L[Procedi a Step 3<br/>Creazione Progetto Django]

    style A fill:#e1f5fe
    style K fill:#c8e6c9
    style I fill:#ffcdd2
    style L fill:#f3e5f5
```

---

## Comandi Step by Step

### 2.1 Verifica ambiente virtuale attivo
```powershell
# Controlla che l'ambiente sia attivo
echo $env:VIRTUAL_ENV

# Se non attivo, attivalo
.\venv\Scripts\activate

# Verifica prompt (deve mostrare (venv))
# (venv) PS C:\...\pizzamama-enreprise>
```

### 2.2 Aggiorna pip (opzionale ma consigliato)
```powershell
# Aggiorna pip alla versione più recente
py -m pip install --upgrade pip
```

**Spiegazione:**
- **py -m pip** → Usa pip dell'ambiente virtuale
- **--upgrade pip** → Aggiorna il package manager stesso
- **Perché aggiornare?** → Evita warning e migliora compatibilità

### 2.3 Installa Django 5.0.1
```powershell
# Installa versione specifica di Django
py -m pip install Django==5.0.1
```

**Spiegazione:**
- **Django==5.0.1** → Versione stabile e specifica (non latest)
- **Versione fissa** → Garantisce riproducibilità del progetto
- **Installazione automatica** → Include tutte le dipendenze necessarie

---

## Verifica Installazione

### Test 1: Verifica package installato
```powershell
# Lista tutti i package nell'ambiente
pip list

# Cerca specificamente Django
pip show Django
```

**Output atteso:**
```
Name: Django
Version: 5.0.1
Summary: A high-level Python Web framework
Location: C:\...\venv\lib\site-packages
```

### Test 2: Verifica comando django-admin
```powershell
# Testa comando CLI di Django
django-admin --version

# Output atteso: 5.0.1
```

### Test 3: Verifica import Python
```powershell
# Test import Django in Python
python -c "import django; print(django.VERSION)"

# Output atteso: (5, 0, 1, 'final', 0)
```

---

## Analisi Dipendenze Installate

Durante l'installazione Django, vengono automaticamente installate queste dipendenze:

### **asgiref** (3.9.1)
- **Scopo:** Supporto ASGI per applicazioni asincrone
- **ASGI vs WSGI:** ASGI supporta WebSockets, HTTP/2, background tasks
- **Utilità:** Permette view asincrone e real-time features

### **sqlparse** (0.5.3)
- **Scopo:** Parser SQL per Django ORM
- **Funzione:** Analizza e formatta query SQL generate dall'ORM
- **Debug:** Utile per ottimizzazione query database

### **tzdata** (2025.2)
- **Scopo:** Database timezone aggiornato
- **Importanza:** Gestione corretta date/orari internazionali
- **Auto-update:** Si aggiorna con le modifiche timezone globali

### **typing_extensions** (4.14.1)
- **Scopo:** Type hints avanzati per Python
- **Python < 3.11:** Backport features typing più recenti
- **Code Quality:** Migliora IDE support e static analysis

---

## Troubleshooting

### Problema: "Could not fetch URL"
**Errore completo:**
```
WARNING: Retrying (Retry(total=4, ...)) after connection broken by 'SSLError'
Could not fetch URL https://pypi.org/simple/django/
```

**Soluzioni:**
```powershell
# Opzione 1: Aggiorna certificati
py -m pip install --upgrade pip certifi

# Opzione 2: Usa mirror PyPI diverso
py -m pip install Django==5.0.1 -i https://pypi.python.org/simple/

# Opzione 3: Disabilita SSL (solo temporaneo)
py -m pip install Django==5.0.1 --trusted-host pypi.org
```

### Problema: "Permission denied"
**Soluzioni:**
```powershell
# Opzione 1: Esegui come amministratore
# Right-click PowerShell → "Run as Administrator"

# Opzione 2: Installa solo per utente corrente
py -m pip install Django==5.0.1 --user

# Opzione 3: Verifica che venv sia attivato
.\venv\Scripts\activate
```

### Problema: "django-admin not found"
**Debug:**
```powershell
# Verifica dove sono i script
ls venv\Scripts\

# Dovresti vedere django-admin.exe
# Se non c'è, reinstalla Django
py -m pip uninstall Django
py -m pip install Django==5.0.1

# Verifica PATH dell'ambiente
echo $env:PATH
```

### Problema: "Module 'django' not found"
**Debug:**
```powershell
# Verifica ambiente attivo
echo $env:VIRTUAL_ENV

# Verifica installazione Django
pip show Django

# Se Django non è installato nell'ambiente corretto
pip list | findstr Django

# Reinstalla se necessario
py -m pip install Django==5.0.1
```

---

## Verifica Finale Installazione

### Test Completo
```powershell
# 1. Ambiente attivo
echo $env:VIRTUAL_ENV

# 2. Django installato
django-admin --version

# 3. Import Python funziona
python -c "import django; print('Django', django.get_version(), 'installed successfully')"

# 4. Lista completa package
pip list
```

**Output atteso completo:**
```
Package           Version
----------------- -------
asgiref           3.9.1
Django            5.0.1
pip               25.1.1
setuptools        65.5.0
sqlparse          0.5.3
tzdata            2025.2
typing_extensions 4.14.1
```

---

## Struttura Post-Installazione

Dopo Step 2, la struttura del progetto è:

```
pizzamama-enreprise/
├── venv/                          ← Ambiente virtuale
│   ├── Scripts/
│   │   ├── activate              ← Script attivazione
│   │   ├── django-admin.exe      ← CLI Django (NEW)
│   │   ├── pip.exe
│   │   └── python.exe
│   ├── Lib/
│   │   └── site-packages/
│   │       ├── django/           ← Framework Django (NEW)
│   │       ├── asgiref/          ← Dipendenza ASGI (NEW)
│   │       ├── sqlparse/         ← Parser SQL (NEW)
│   │       └── ...               ← Altre dipendenze (NEW)
│   └── pyvenv.cfg
└── (file progetto Django - prossimi step)
```

---

## Cosa Abbiamo Realizzato

### **Framework Web Installato**
- **Django 5.0.1** → Framework web Python professionale
- **Versione stabile** → Compatibility e long-term support
- **Ambiente isolato** → Non interferisce con sistema

### **Dipendenze Enterprise**
- **ASGI support** → Capacità asincrone e real-time
- **SQL parsing** → ORM avanzato per database
- **Timezone handling** → Supporto internazionale
- **Type hints** → Code quality e IDE support

### **CLI Tools Disponibili**
- **django-admin** → Comando per creare progetti
- **Gestione progetti** → Scaffold automatico
- **Development server** → Server integrato

---

## Prossimo Step

Una volta completato con successo questo step:

1. **Verifica** django-admin --version restituisce 5.0.1
2. **Testa** import django in Python funziona
3. **Procedi** a **Step 3: Creazione Progetto Django**

### Collegamento al prossimo step:
```
README-Step3-Progetto.md
Creeremo il progetto Django con struttura enterprise
Configureremo la directory src/ e file principali
```

---

## Note Importanti

### **Versioni e Compatibilità**
- **Django 5.0.1** → Richiede Python 3.8+
- **Stability** → Versione LTS consigliata per produzione
- **Security updates** → Supporto sicurezza fino a Django 6.0

### **Package Management**
- **Requirements.txt** → Documenteremo dipendenze nei prossimi step
- **Virtual environment** → Mantiene dipendenze isolate
- **Riproducibilità** → Stesso setup su diversi ambienti

### **Best Practices**
```powershell
# Sempre usa py -m pip nell'ambiente virtuale
py -m pip install package_name

# Non python -m pip o solo pip
# Per evitare confusione ambiente globale/virtuale
```

---

## Checklist Completamento Step 2

- [ ] **Ambiente virtuale attivo** → (venv) nel prompt
- [ ] **Django installato** → django-admin --version = 5.0.1
- [ ] **Import funziona** → python -c "import django" senza errori
- [ ] **Dipendenze corrette** → pip list mostra asgiref, sqlparse, tzdata
- [ ] **Pronto per Step 3** → Creazione progetto Django

**Una volta completata la checklist, sei pronto per creare il progetto Django con struttura enterprise!**