from flask import Blueprint, render_template, request, session, redirect, url_for, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from auth.models import User
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from . import auth_bp
from app import db
from characters.routes import load_char
import os
import re

#----------------------------CONTROLLO EMAIL------------------------------------
def controllo_email():
    pass

#----------------------------PROTEZIONE DELLA PASSWORD--------------------------
def psw_proteggi_hash(psw):
    pass

#----------------------------SIGN_IN--------------------------------------------
@auth_bp.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    pass

#----------------------------LOGIN-----------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass

#----------------------------AREA PERSONALE----------------------------------------
@auth_bp.route('/area_personale', methods=['GET', 'POST'])
def area_personale():
    pass

#----------------------------CREAZIONE UTENTE--------------------------------------
@auth_bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    pass

#----------------------------ELIMINAZIONE UTENTE-------------------------------------
@auth_bp.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    pass

#----------------------------CREAZIONE DEI CREDITI----------------------------------
@auth_bp.route('/credit_refill', methods=['GET', 'POST'])
@login_required
def credit_refill():
    pass

#----------------------------LOGOUT-------------------------------------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Logout effettuato con successo", "info")
    return render_template('menu.html')
