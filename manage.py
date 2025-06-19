# CitaMatic/manage.py
import os
from dotenv import load_dotenv

load_dotenv()

from backend.app.main import app
from backend.app.config import db
from backend.app.cli import register_cli
from flask_migrate import Migrate


migrate = Migrate(app, db)
register_cli(app)


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['1', 'true', 't', 'yes']
    app.run(host='0.0.0.0', debug=debug_mode, port=5000)
