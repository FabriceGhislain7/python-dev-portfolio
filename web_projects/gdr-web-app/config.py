import os

# cartella root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# directory file JSON dei personaggi
DATA_DIR_PGS = os.path.join(BASE_DIR, 'data', 'json', 'personaggi')

# directory file JSON degli inventari
DATA_DIR_INV = os.path.join(BASE_DIR, 'data', 'json', 'inventari')

# directory file JSON del salvataggio della battaglia
DATA_DIR_SAVE = os.path.join(BASE_DIR, 'data', 'json', 'save')

# directory file JSON delle missioni
DATA_DIR_MIS = os.path.join(BASE_DIR, 'static', 'json', 'missions')

# directory dei log messaggi
DATA_DIR_LOG = os.path.join(BASE_DIR, 'data', 'json', 'log')
print(f"DATA_DIR_LOG ===========> : {DATA_DIR_LOG}")
LOG_JSON_PATH = os.path.join(DATA_DIR_LOG, 'log_evento.json')

print(f"LOG_JSOM_PATH ===========> : {LOG_JSON_PATH}")

def CreateDirs():
    """
    Crea directory per i file JSON per i personaggi e gli inventari
    se non sono esistenti
    """
    for d in (DATA_DIR_PGS, DATA_DIR_INV, DATA_DIR_SAVE, DATA_DIR_MIS, DATA_DIR_LOG):
        os.makedirs(d, exist_ok=True)

        # crea file gitkeep se non esiste
        gitkeep = os.path.join(d, '.gitkeep')
        if not os.path.exists(gitkeep):
            open(gitkeep, 'a').close()