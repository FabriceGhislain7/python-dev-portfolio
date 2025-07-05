from flask import redirect, render_template, session, url_for, request, flash, jsonify
from . import battle_bp
from gioco.personaggio import Personaggio
from gioco.inventario import Inventario
from gioco.ambiente import Ambiente, Foresta
from gioco.missione import Missione, GestoreMissioni
from gioco.oggetto import Oggetto
from utils.messaggi import Messaggi
from utils.log import Log
import random
import json
import os

#---------------------------SHOW_INVENTORY--------------------------------
@battle_bp.route('/show_inventory', methods=['GET', 'POST'])
def show_inventory():
    pass

#---------------------------BEGIN THE BATTLE------------------------------
@battle_bp.route('/begin_battle', methods=['GET', 'POST'])
def begin_battle():
    pass

#---------------------------SELECT_CHAR-----------------------------------
@battle_bp.route('/select_char', methods=['GET', 'POST'])
def select_char():
    pass

#---------------------------TEST BATTLE-----------------------------------
@battle_bp.route('/test_battle', methods=['GET', 'POST'])
def test_battle():
    pass
