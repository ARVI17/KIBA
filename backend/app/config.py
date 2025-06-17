# backend/app/config.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Database connection string
    db_uri = os.environ["DATABASE_URL"]
    if db_uri.startswith("postgres://"):
        db_uri = db_uri.replace("postgres://", "postgresql+pg8000://", 1)
    elif db_uri.startswith("postgresql://"):
        db_uri = db_uri.replace("postgresql://", "postgresql+pg8000://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Secret used to sign JWTs and sessions
    app.config['SECRET_KEY'] = os.environ['JWT_SECRET']

    db.init_app(app)

    return app
