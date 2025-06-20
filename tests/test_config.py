import os
import importlib
import logging

# Ensure a default DATABASE_URL so the module can be imported
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost/db")
os.environ.setdefault("JWT_SECRET", "testsecret")

import backend.app.config as config

def setup_env(url):
    os.environ["DATABASE_URL"] = url
    os.environ["JWT_SECRET"] = "testsecret"
    importlib.reload(config)


def test_postgres_url_usado(monkeypatch):
    url = "postgres://user:pass@localhost/db"
    setup_env(url)
    app = config.create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == url


def test_postgresql_url_usado(monkeypatch):
    url = "postgresql://user:pass@localhost/db"
    setup_env(url)
    app = config.create_app()
    assert app.config["SQLALCHEMY_DATABASE_URI"] == url


def test_log_message_masked(monkeypatch, caplog):
    url = "postgresql://user:pass@localhost/db"
    setup_env(url)
    with caplog.at_level(logging.INFO):
        importlib.reload(config)
    messages = "".join(record.getMessage() for record in caplog.records)
    assert "pass" not in messages
