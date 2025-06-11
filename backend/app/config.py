# backend/app/config.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Lee la cadena de conexión desde la variable de entorno DATABASE_URL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # SECRET_KEY is used to sign session and JWT tokens
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kiba-insecure-secret')

    db.init_app(app)

    return app
