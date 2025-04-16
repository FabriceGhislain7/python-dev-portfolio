
# 🍕 PizzaMama - README Technique

## 📐 Architecture Générale

Ce projet Django est structuré autour de deux applications principales : `main` et `menu`, intégrées dans le projet `pizzamama`.

L'objectif de ce document est de clarifier le **flux de données**, les **relations entre fichiers**, et comment **chaque composant interagit** dans le projet.

---

## 📊 Diagramme Mermaid - Flux de Données & Structure

> Ce diagramme montre comment une requête est traitée, depuis le navigateur jusqu'à la base de données via Django.

```mermaid
graph TD

subgraph Utilisateur
    A1[Navigateur Web]
end

subgraph Django
    A1 --> B1[urls.py (projet)]
    B1 --> B2[main/urls.py ou menu/urls.py]
    B2 --> B3[vues.py (views.py)]

    B3 --> B4[models.py]
    B3 --> B5[templates (index.html)]
    B3 --> B6[static (CSS/Images)]

    B4 -->|ORM| C1[(db.sqlite3)]
end

subgraph Apps Django
    B4 --> M1[main/models.py]
    B4 --> M2[menu/models.py]
end

subgraph Fichiers statiques
    B6 --> S1[main/static/main/style.css]
    B6 --> S2[menu/static/menu/style.css]
end

subgraph Templates
    B5 --> T1[main/templates/main/index.html]
    B5 --> T2[menu/templates/menu/index.html]
end

subgraph Admin
    ADM1[admin.py] --> B4
end

subgraph Migrations
    MG1[makemigrations] --> MIG[menu/migrations/0001_initial.py]
    MIG -->|migrate| C1
end
```

---

## 🔍 Explication détaillée

### 🔁 1. Le parcours d'une requête

- L'utilisateur visite une page web (ex : `/menu/`).
- Django redirige cette requête via `pizzamama/urls.py`, qui inclut les `urls.py` des apps `main` ou `menu`.
- Le bon fichier `views.py` est appelé pour générer une réponse.

### 🧠 2. Rôle des vues (`views.py`)

- Les vues agissent comme **logique métier**.
- Elles peuvent :
  - Lire des données depuis `models.py` via l’ORM.
  - Passer ces données à des templates pour affichage HTML.
  - Interagir avec des formulaires ou gérer des actions spécifiques.

### 🧱 3. Rôle des modèles (`models.py`)

- Ils décrivent les **structures des données** stockées en base.
- Exemple : une pizza avec son nom, prix, description, etc.
- Django génère automatiquement les requêtes SQL grâce à son ORM.

### 🎨 4. Templates & Statics

- Les templates HTML (dans `templates/`) sont utilisés pour l'affichage dynamique des pages.
- Les fichiers statiques comme les `.css` et les images sont stockés dans `static/`.

### 🛠️ 5. Admin Django

- Le fichier `admin.py` configure l'affichage et l'administration des modèles dans l'interface d'administration Django (`/admin`).
- Super pratique pour insérer ou modifier les données sans interface frontale dédiée.

### 🧬 6. Migrations et BDD

- Les fichiers `migrations/` sont générés automatiquement pour refléter les changements des modèles dans la base de données.
- Ils permettent de **versionner et appliquer les schémas** de la base via ORM.

---

## ⚙️ Commandes utiles

```bash
# Créer un fichier de migration à partir des modèles
python manage.py makemigrations

# Appliquer les migrations à la base de données
python manage.py migrate

# Démarrer le serveur de développement
python manage.py runserver

# Lancer un shell interactif pour manipuler les modèles
python manage.py shell

# Créer un superutilisateur pour accéder à l’admin
python manage.py createsuperuser
```

---

## 📎 Résumé des responsabilités des dossiers

| Dossier / Fichier                          | Rôle principal                                      |
|-------------------------------------------|----------------------------------------------------|
| `manage.py`                                | Entrée principale pour les commandes Django        |
| `pizzamama/settings.py`                    | Configuration globale du projet                    |
| `pizzamama/urls.py`                        | Routeur principal                                  |
| `main/`, `menu/`                           | Applications Django (avec modèles, vues, etc.)     |
| `main/templates/`, `menu/templates/`       | Templates HTML spécifiques à chaque app            |
| `main/static/`, `menu/static/`             | Fichiers CSS/images liés aux templates             |
| `main/models.py`, `menu/models.py`         | Définition des modèles de données                 |
| `main/views.py`, `menu/views.py`           | Logique métier, traitement des requêtes           |
| `main/urls.py`, `menu/urls.py`             | Routage spécifique à chaque app                    |
| `main/admin.py`, `menu/admin.py`           | Enregistrement des modèles pour l’admin Django     |

---

## 💡 Tips de développement

- Utilise le site admin Django pour gérer rapidement tes données.
- Structure bien chaque app avec ses propres `static`, `templates`, `models`, etc.
- Utilise le shell Django pour tester ton code rapidement :

```python
from menu.models import Pizza
Pizza.objects.create(nom="4 Fromages", prix=12.5)
```

---

Tu peux copier/coller tout ce contenu dans ton `README.md` et voir le diagramme Mermaid directement dans un éditeur Markdown compatible Mermaid (comme VS Code avec une extension Markdown Preview Mermaid, ou sur GitHub).

Souhaite-tu que je t’aide aussi à générer ce diagramme **en image** ou t’ajouter un diagramme de la **base de données** aussi ?