# backend/app/config.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Database connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Secret used to sign JWTs and sessions
    app.config['SECRET_KEY'] = os.environ['JWT_SECRET']

    db.init_app(app)

    return app
