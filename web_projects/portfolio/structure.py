#!/usr/bin/env python3
"""
Portfolio Structure Generator - Static Modular Approach
Portfolio statico con index.html unico ma CSS/JS/JSON separati
"""
import os

def create_directory_structure():
    """Crea la struttura delle cartelle per portfolio statico"""
    directories = [
        # Assets directory
        "assets",
        "assets/css",
        "assets/css/components",
        "assets/js",
        "assets/js/modules",
        "assets/images",
        "assets/images/projects",
        "assets/images/hero",
        "assets/images/about",
        "assets/images/icons",
        "assets/files",

        # Data directory
        "data",
    ]

    print("Creazione struttura portfolio statico...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Creata cartella: {directory}")

def create_static_files():
    """Crea i file per portfolio statico modulare"""
    files = [
        # ================================
        # HTML PRINCIPALE
        # ================================
        "index.html",                           # Unico file HTML principale

        # ================================
        # CSS MODULARE PER COMPONENTE
        # ================================
        "assets/css/reset.css",                 # CSS reset globale
        "assets/css/variables.css",             # Variabili design system
        "assets/css/layout.css",                # Layout generale e grid
        "assets/css/typography.css",            # Font e tipografia

        # CSS per singoli componenti
        "assets/css/components/header.css",     # Stili header
        "assets/css/components/hero.css",       # Stili hero section
        "assets/css/components/about.css",      # Stili about section
        "assets/css/components/skills.css",     # Stili skills section
        "assets/css/components/projects.css",   # Stili projects section
        "assets/css/components/education.css",  # Stili education section
        "assets/css/components/contact.css",    # Stili contact section
        "assets/css/components/footer.css",     # Stili footer
        "assets/css/components/buttons.css",    # Stili bottoni
        "assets/css/components/forms.css",      # Stili form
        "assets/css/components/loading.css",    # Stili loading screen

        # CSS per funzionalità
        "assets/css/animations.css",            # Animazioni globali
        "assets/css/responsive.css",            # Media queries responsive
        "assets/css/dark-theme.css",            # Dark theme overrides
        "assets/css/utilities.css",             # Classi utility

        # ================================
        # JAVASCRIPT MODULARE
        # ================================
        "assets/js/config.js",                  # Configurazioni globali
        "assets/js/utils.js",                   # Utility functions
        "assets/js/main.js",                    # Script principale

        # JS per singoli componenti/features
        "assets/js/modules/theme.js",           # Theme switcher
        "assets/js/modules/navigation.js",      # Navigation behavior
        "assets/js/modules/scroll.js",          # Scroll effects
        "assets/js/modules/animations.js",      # Animazioni e Intersection Observer
        "assets/js/modules/hero.js",            # Logica hero section (typewriter, etc)
        "assets/js/modules/skills.js",          # Caricamento e display skills da JSON
        "assets/js/modules/projects.js",        # Caricamento progetti da JSON
        "assets/js/modules/filters.js",         # Filtri progetti/skills
        "assets/js/modules/contact.js",         # Form validation e invio
        "assets/js/modules/loading.js",         # Loading screen management
        "assets/js/modules/counters.js",        # Contatori animati (about stats)

        # ================================
        # DATA FILES JSON
        # ================================
        "data/projects.json",                   # Dati progetti
        "data/skills.json",                     # Dati skills
        "data/education.json",                  # Dati formazione
        "data/personal.json",                   # Info personali e contatti

        # ================================
        # STATIC FILES
        # ================================
        "favicon.ico",                          # Favicon
        "manifest.json",                        # PWA manifest
        "robots.txt",                           # SEO robots
        "sitemap.xml",                          # SEO sitemap

        # ================================
        # PROJECT FILES
        # ================================
        ".gitignore",                           # Git ignore
        "README.md",                            # Documentazione progetto
    ]

    print("\nCreazione file modulari...")
    for file_path in files:
        # Crea le directory se non esistono
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        # Crea file vuoto
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("")
        print(f"Creato file: {file_path}")

def main():
    """Funzione principale"""
    print("PORTFOLIO STRUCTURE GENERATOR - STATIC MODULAR")
    print("=" * 50)
    print("Portfolio statico con index.html unico ma CSS/JS/JSON separati")
    print()

    try:
        create_directory_structure()
        create_static_files()

        print("\nStruttura portfolio statico creata con successo!")

    except Exception as e:
        print(f"Errore durante la creazione: {e}")

if __name__ == "__main__":
    main()