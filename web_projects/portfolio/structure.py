#!/usr/bin/env python3
"""
Portfolio Structure Generator - Base
Crea solo la struttura delle cartelle e i file vuoti
"""
import os

def create_directory_structure():
    """Crea la struttura delle cartelle"""
    directories = [
        "assets",
        "assets/css",
        "assets/js",
        "assets/js/modules",
        "assets/images",
        "assets/images/projects",
        "assets/images/icons",
        "assets/images/hero",
        "assets/fonts",
        "assets/videos",
        "components",
        "data",
        "docs"
    ]
   
    print("🚀 Creazione struttura cartelle...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Creata cartella: {directory}")

def create_empty_files():
    """Crea i file vuoti"""
    files = [
        # HTML
        "index.html",
        "404.html",
       
        # CSS
        "assets/css/reset.css",
        "assets/css/variables.css",
        "assets/css/main.css",
        "assets/css/components.css",
        "assets/css/animations.css",
        "assets/css/responsive.css",
        "assets/css/dark-theme.css",
       
        # JavaScript
        "assets/js/main.js",
        "assets/js/modules/navigation.js",
        "assets/js/modules/projects.js",
        "assets/js/modules/animations.js",
        "assets/js/modules/contact.js",
        "assets/js/modules/theme.js",
        "assets/js/modules/scroll.js",
        "assets/js/modules/filters.js",
        "assets/js/utils.js",
        "assets/js/config.js",
       
        # Data
        "data/projects.json",
        "data/skills.json",
        "data/experience.json",
        "data/testimonials.json",
       
        # Components
        "components/header.html",
        "components/footer.html",
        "components/hero.html",
        "components/about.html",
        "components/skills.html",
        "components/projects.html",
        "components/contact.html",
       
        # Configuration
        "manifest.json",
        "robots.txt",
        "sitemap.xml",
       
        # Documentation
        "README.md",
        "docs/setup.md",
        
        # Git
        ".gitignore"
    ]
   
    print("\n📄 Creazione file vuoti...")
    for file_path in files:
        # Crea le directory se non esistono
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        # Crea file vuoto
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("")
        print(f"✅ Creato file: {file_path}")

def main():
    """Funzione principale"""
    print("🎨 PORTFOLIO STRUCTURE GENERATOR")
    print("=" * 40)
   
    try:
        create_directory_structure()
        create_empty_files()
       
        print("\n🎉 Struttura portfolio creata con successo!")
        print("\nStruttura creata:")
        print("├── index.html")
        print("├── assets/")
        print("│   ├── css/")
        print("│   ├── js/")
        print("│   │   └── modules/")
        print("│   ├── images/")
        print("│   │   ├── projects/")
        print("│   │   ├── icons/")
        print("│   │   └── hero/")
        print("│   ├── fonts/")
        print("│   └── videos/")
        print("├── components/")
        print("├── data/")
        print("├── docs/")
        print("└── README.md")
       
    except Exception as e:
        print(f"❌ Errore durante la creazione: {e}")

if __name__ == "__main__":
    main()