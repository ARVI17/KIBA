import os
from backend.app.config import create_app

def setup_env(url):
    os.environ["DATABASE_URL"] = url
    os.environ["JWT_SECRET"] = "testsecret"


def test_postgres_url_usado(monkeypatch):
    url = "postgres://user:pass@localhost/db"
    setup_env(url)
    app = create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == url


def test_postgresql_url_usado(monkeypatch):
    url = "postgresql://user:pass@localhost/db"
    setup_env(url)
    app = create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == url
