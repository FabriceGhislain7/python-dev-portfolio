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
