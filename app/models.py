from app import db
from flask_login import UserMixin

class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    apartamento = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'Cliente({self.nombre}, {self.email}, {self.apartamento})'
