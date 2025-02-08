import os

class Config:
    SECRET_KEY = os.environ.get('1998miguel') or 'clave_secreta_segura'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/menu.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
