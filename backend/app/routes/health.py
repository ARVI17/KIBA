from flask import Blueprint, jsonify
from sqlalchemy import text

from backend.app.config import db

health_bp = Blueprint('health', __name__)


@health_bp.route('/v1/health/db', methods=['GET'])
def db_health():
    """Return OK when the database connection is alive.

    Endpoint available at ``/api/v1/health/db`` once the blueprint is
    registered with the ``/api`` prefix.
    """
    db.session.execute(text('SELECT 1'))
    return jsonify({'status': 'ok'})
