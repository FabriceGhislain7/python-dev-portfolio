from flask import request, render_template, redirect, url_for, flash, session
from . import environment_bp
from gioco.ambiente import AmbienteFactory, Ambiente
from utils.log import Log


@environment_bp.route('/select-environment', methods=['GET', 'POST'])
def select_environment():
    pass


@environment_bp.route('/show-environment')
def show_environment():
    pass 


@staticmethod
def descrizione():
  pass
