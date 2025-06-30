from database.db import db

class User(db.Model):
    id         = db.Column(db.Integer, primiry_key=True)
    username   = db.Column(db.String(60), unique=True, nullable=True)
    password   = db.Column(db.String(200), nullable=False)
    personaggi = db.relationship('Personaggio', backref='utente', lazy=True)

class Personaggio(db.Model):
    id = db.Column(db.Integer, primiry_key=True)
    nome = db.Column(db.String(50), nullable=False)
    classe = db.Column(db.String(50), nullable=False)
    salute = db.Column(db.Integer, default=100)
    attacco_min = db.Column(db.Integer, default=5)
    attacco_max = db.Column(db.Integer, default=15)
    livello = db.Column(db.Integer, default=1)
    user_id = bd.Column(db.Integer, db.ForeignKey('user.id', nullable=False))