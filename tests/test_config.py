import os
from backend.app.config import create_app

def setup_env(url):
    os.environ["DATABASE_URL"] = url
    os.environ["JWT_SECRET"] = "testsecret"


def test_postgres_url_converted(monkeypatch):
    setup_env("postgres://user:pass@localhost/db")
    app = create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "postgresql+pg8000://user:pass@localhost/db"


def test_postgresql_url_converted(monkeypatch):
    setup_env("postgresql://user:pass@localhost/db")
    app = create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "postgresql+pg8000://user:pass@localhost/db"
