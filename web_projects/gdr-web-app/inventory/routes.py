from . import inventory_bp
from flask import render_template, request, session, redirect, url_for, flash
from gioco.oggetto import BombaAcida, Medaglione, Oggetto, PozioneCura
from gioco.personaggio import Personaggio
from gioco.classi import Ladro, Mago, Guerriero
from gioco.inventario import Inventario
from utils.messaggi import Messaggi
from utils.log import Log

@inventory_bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    pass


