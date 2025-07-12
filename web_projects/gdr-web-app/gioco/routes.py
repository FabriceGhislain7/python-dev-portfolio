from flask import Blueprint, render_template, request, session, redirect, url_for
from gioco.personaggio import Personaggio
from gioco.classi import Mago, Guerriero, Ladro
from flask_login import login_user, logout_user, login_required, current_user, UserMixin 
import os

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
gioco_bp = Blueprint('gioco', __name__, template_folder=template_dir)

# ----------------------HOME_PAGE------------------------------------
@gioco_bp.route('/')
def index():
    return render_template('index.html')

#-----------------------ABOUT---------------------------------------
@gioco_bp.route('/about')
def about():
    return render_template('about.html')

#-----------------------GUIDE_GAME----------------------------------
@gioco_bp.route('/guide_game')
def guide_game():
    return render_template('guide_game.html')

#-----------------------CREDITS--------------------------------------
@gioco_bp.route("/credits")
def credits():
    return render_template("credits.html")

#-----------------------MENU_PRINCIPALE------------------------------
@gioco_bp.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

