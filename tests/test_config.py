import os
from backend.app.config import create_app
import importlib
import logging

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


def test_log_message_masked(monkeypatch, caplog):
    url = "postgresql://user:pass@localhost/db"
    setup_env(url)
    with caplog.at_level(logging.INFO):
        importlib.reload(importlib.import_module("backend.app.config"))
    messages = "".join(record.getMessage() for record in caplog.records)
    assert "pass" not in messages
