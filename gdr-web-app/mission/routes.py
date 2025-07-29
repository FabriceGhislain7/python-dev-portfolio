from collections import defaultdict

from environment import routes as environment_routes
from . import mission_bp
from flask import flash, render_template, request, session, \
    redirect, url_for
from gioco.missione import GestoreMissioni, Missione
from utils.messaggi import Messaggi
from utils.log import Log


@mission_bp.route('/select_mission', methods=['GET', 'POST'])
def select_mission():
    pass


@mission_bp.route('/show_mission')
def show_mission():
    pass

@mission_bp.route('/missioni')
def mostra_missioni():
    pass


@mission_bp.route('/missione/attiva')
def missione_attiva():
    pass


@mission_bp.route('/missioni/stato')
def stato_missioni():
    pass