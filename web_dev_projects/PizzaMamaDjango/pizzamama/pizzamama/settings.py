"""
Django settings for pizzamama project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR pointe vers le dossier parent de settings.py (pizzamama/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Clé cryptographique pour les sessions (NE PAS PARTAGER EN PROD)
SECRET_KEY = '...'

# SECURITY WARNING: don't run with debug turned on in production!
# En développement = True, en production = False
DEBUG = True

# Liste des domaines autorisés à accéder à l'application (vide = localhost)
ALLOWED_HOSTS = []

# Application definition
# Apps installées (core Django + vos apps personnalisées)
INSTALLED_APPS = [
    'django.contrib.admin',       # Interface admin
    'django.contrib.auth',        # Système d'authentification
    'django.contrib.contenttypes',# Gestion des types de contenu
    'django.contrib.sessions',    # Gestion des sessions
    'django.contrib.messages',    # Système de messages
    'django.contrib.staticfiles', # Fichiers statiques (CSS/JS)
    'main.apps.MainConfig',       # Votre app principale
    'menu.apps.MenuConfig',       # Votre app menu
]

# Middleware = couches de traitement des requêtes (ordre IMPORTANT)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Sécurité
    'django.contrib.sessions.middleware.SessionMiddleware',  # Sessions
    'django.middleware.locale.LocaleMiddleware',     # Traductions
    'django.middleware.common.CommonMiddleware',     # URL standardisées
    'django.middleware.csrf.CsrfViewMiddleware',     # Protection CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Auth
    'django.contrib.messages.middleware.MessageMiddleware',     # Messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Anti-clickjacking
]

# Fichier racine des URLs
ROOT_URLCONF = 'pizzamama.urls'

# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Dossiers supplémentaires pour les templates
        'APP_DIRS': True,  # Chercher templates dans les apps
        'OPTIONS': {
            'context_processors': [  # Variables globales pour les templates
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Point d'entrée WSGI (pour serveurs production)
WSGI_APPLICATION = 'pizzamama.wsgi.application'

# Configuration base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Base SQLite par défaut
        'NAME': BASE_DIR / 'db.sqlite3',         # Emplacement du fichier
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalisation
LANGUAGE_CODE = 'fr'         # Langue par défaut
TIME_ZONE = 'Europe/Paris'   # Fuseau horaire
USE_I18N = True              # Activation traductions
USE_L10N = True              # Formats locaux (dates, nombres)
USE_TZ = True                # Utilisation timezone

# pizzamama/settings.py
LOCALE_PATHS = [
    BASE_DIR / 'locale',  # Pointe vers pizzamama/locale/
]

# Fichiers statiques (CSS, JS, images)
STATIC_URL = 'static/'       # URL de base pour les fichiers statiques

# Clé primaire par défaut pour les modèles
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'