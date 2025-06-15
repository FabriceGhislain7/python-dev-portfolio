"""
Modulo per creare la struttura di cartelle e file del progetto Gdr-flask.

La struttura è definita da un dizionario che associa nomi di cartelle a liste di file.
"""

import os

# Definizione delle cartelle e dei file
structure = {
    "gioco": [
        "ambiente.py", "classi.py", "compagnia.py", "inventario.py",
        "menu-principale.py", "missione.py", "oggetto.py", "personaggio.py",
        "routes.py", "scontro.py", "strategy.py", "turno.py"
    ],
    "templates": [
        "create_char.html", "layout.html", "select_mission.html"
    ],
    "utils": [
        "log.py", "salvataggio.py"
    ],
    "static": [  # sottocartelle statiche comuni
        "css/", "js/", "img/"
    ]
}

# Cartella principale
base_dir = "Gdr-flask"
os.makedirs(base_dir, exist_ok=True)

# Creazione delle cartelle e dei file
for folder, files in structure.items():
    folder_path = os.path.join(base_dir, folder)
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        file_path = os.path.join(folder_path, file)
        if file.endswith("/"):
            os.makedirs(file_path, exist_ok=True)  # crea sottocartelle
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                pass  # crea file vuoto

# Creazione dei file nella root del progetto
root_files = [".gitignore", "app.py"]
for file in root_files:
    file_path = os.path.join(base_dir, file)
    with open(file_path, "w", encoding="utf-8") as f:
        pass  # crea file vuoto

print("Struttura cartelle e file creata con successo!")
