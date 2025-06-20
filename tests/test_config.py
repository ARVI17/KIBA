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


def test_cors_frontend_url_used(monkeypatch):
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["JWT_SECRET"] = "secret"
    os.environ["FRONTEND_URL"] = "https://front.test"

    captured = {}

    def fake_cors(app, resources):
        captured["origins"] = resources[r"/api/*"]["origins"]

    monkeypatch.setattr("backend.app.config.CORS", fake_cors)
    importlib.reload(importlib.import_module("backend.app.config"))
    from backend.app.config import create_app
    create_app()
    assert captured["origins"] == "https://front.test"


def test_cors_default_wildcard_warning(monkeypatch, caplog):
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["JWT_SECRET"] = "secret"
    os.environ.pop("FRONTEND_URL", None)

    captured = {}

    def fake_cors(app, resources):
        captured["origins"] = resources[r"/api/*"]["origins"]

    monkeypatch.setattr("backend.app.config.CORS", fake_cors)
    with caplog.at_level(logging.WARNING):
        importlib.reload(importlib.import_module("backend.app.config"))
        from backend.app.config import create_app
        create_app()
    assert captured["origins"] == "*"
    assert any("FRONTEND_URL" in rec.getMessage() for rec in caplog.records)
