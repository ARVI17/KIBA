# backend/app/config.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # ✅ Usa la conexión real a XAMPP
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/kiba'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-super-secreta-kiba')

    db.init_app(app)

    return app
