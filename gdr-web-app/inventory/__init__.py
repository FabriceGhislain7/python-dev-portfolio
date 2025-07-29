from flask import Blueprint
from gioco.inventario import Inventario

inventory_bp = Blueprint('inventory', __name__, template_folder='templates')
