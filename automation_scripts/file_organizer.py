"""
MÉTHODES POUR FICHIERS ET RÉPERTOIRES EN PYTHON
----------------------------------------------
Mots-clés Python (immuables) : with, open, as, for, in, if, else
Fonctions natives (non modifiables) : print(), strftime(), strip()
Mots techniques (à respecter) : 'w', 'a', 'r' (modes d'ouverture)
"""

import os
import shutil
import datetime

# ===== OPÉRATIONS SUR LES FICHIERS =====

# Création/écriture (mode 'w' = write)
chemin_fichier = "test.txt"  # 'chemin_fichier' est une variable (modifiable)
with open(chemin_fichier, "w") as f:  # 'open' et 'with' sont des mots-clés
    f.write("Contenu initial\n")  # '\n' pour saut de ligne

# Ajout de contenu (mode 'a' = append)
with open(chemin_fichier, "a") as f:
    f.writelines([f"Ligne {i}\n" for i in range(1,4)])  # writelines pour liste

# Lecture complète (mode 'r' = read)
with open(chemin_fichier, "r") as f:
    contenu = f.read()  # Lit tout le contenu dans une chaîne
    print("Contenu complet:\n", contenu)

# Lecture ligne par ligne (économise la mémoire)
with open(chemin_fichier, "r") as f:
    print("\nLigne par ligne:")
    for ligne in f:  # 'for' et 'in' sont des mots-clés
        print(ligne.strip())  # Enlève les espaces et sauts de ligne

# Gestion des chemins (os.path)
nom_fichier = os.path.basename(chemin_fichier)  # 'test.txt'
nom_sans_ext = os.path.splitext(nom_fichier)[0]  # 'test'
extension = os.path.splitext(nom_fichier)[1]  # '.txt'

# ===== OPÉRATIONS SUR LES RÉPERTOIRES =====

# Création de répertoire
chemin_repertoire = "mon_dossier"
os.makedirs(chemin_repertoire, exist_ok=True)  # Crée si n'existe pas

# Vérification
if os.path.isdir(chemin_repertoire):  # 'isdir' vérifie si c'est un répertoire
    print(f"\nLe répertoire {chemin_repertoire} existe")

# Chemin complet avec os.path.join
fichier_dans_repertoire = os.path.join(chemin_repertoire, "sous_fichier.txt")
with open(fichier_dans_repertoire, "w") as f:
    f.write("Contenu dans sous-répertoire")

# Liste le contenu
print("\nContenu du répertoire:")
for element in os.listdir(chemin_repertoire):  # Parcourt les éléments
    print(f"- {element}")

# ===== FONCTIONS UTILES =====
"""
Input/Output types:
- os.path.exists(chemin: str) -> bool
- os.path.getsize(chemin: str) -> int
- os.listdir(chemin: str) -> List[str]
- shutil.copy(src: str, dst: str) -> None
"""

# Copie de fichier
shutil.copy(chemin_fichier, os.path.join(chemin_repertoire, "copie.txt"))

# Fichier avec timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
fichier_temp = f"temp_{timestamp}.txt"