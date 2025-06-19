import logging
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(e: HTTPException):
        return jsonify(error=e.description), e.code

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        logger.error("Unhandled exception", exc_info=True)
        return jsonify(error="Internal server error"), 500


__all__ = ["register_error_handlers"]
